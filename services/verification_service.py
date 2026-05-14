import logging
from services.ai_service import AIService
from services.parser_service import ParserService
from services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)

class VerificationService:
    MAX_PROMPT_TOKENS = 4000  # Safe budget for command-r or similar

    def __init__(self, ai_service: AIService):
        self.ai_service = ai_service
        self.parser_service = ParserService()
        self.embedding_service = EmbeddingService()

    def _estimate_tokens(self, text: str) -> int:
        # Rough token estimation based on word count
        return int(len(text.split()) * 1.3)

    def _truncate_to_budget(self, text: str, max_tokens: int) -> str:
        """Truncates text to a token budget while preserving sentence boundaries."""
        if self._estimate_tokens(text) <= max_tokens:
            return text
            
        sentences = self.embedding_service._split_into_sentences(text)
        truncated_sentences = []
        current_tokens = 0
        
        for sentence in sentences:
            sentence_tokens = self._estimate_tokens(sentence)
            if current_tokens + sentence_tokens > max_tokens:
                break
            truncated_sentences.append(sentence)
            current_tokens += sentence_tokens
            
        return " ".join(truncated_sentences)

    def verify_claim(self, claim: str, evidence: str) -> tuple:
        """
        Takes a claim and evidence, queries the AI using RAG, and parses the response.
        Returns a tuple: (result, explanation, color, retrieval_trace)
        """
        try:
            # 1. Embed incoming claim
            claim_embedding = self.embedding_service.generate_embedding(claim)
            
            # 2. Process and embed incoming evidence
            evidence_chunks = self.embedding_service.process_and_embed_evidence(evidence)
            
            # 3. Retrieve top relevant chunks
            top_chunks = self.embedding_service.retrieve_similar_chunks(
                query_embedding=claim_embedding,
                stored_embeddings=evidence_chunks,
                top_k=3,
                threshold=0.3
            )
            
            logger.info(f"Retrieved {len(top_chunks)} chunks for claim.")
            
            # 4. Fallback behavior & Evidence Context Construction
            if not top_chunks:
                logger.warning("No chunks met the similarity threshold. Activating fallback behavior.")
                # Truncate evidence to budget (leaving room for the static prompt structure ~500 tokens)
                budgeted_evidence = self._truncate_to_budget(evidence, self.MAX_PROMPT_TOKENS - 500)
                
                if len(budgeted_evidence) < len(evidence):
                    logger.warning("Fallback evidence exceeded token budget. Truncated at sentence boundaries.")
                    
                context_text = budgeted_evidence
                retrieval_trace = []
            else:
                context_text = ""
                retrieval_trace = []
                for i, chunk in enumerate(top_chunks):
                    score = chunk.get("similarity_score", 0.0)
                    logger.info(f"Chunk {i+1} similarity score: {score:.4f}")
                    context_text += f"[Evidence Chunk {i+1} | Relevance Score: {score:.2f}]\n{chunk['text']}\n\n"
                    
                    retrieval_trace.append({
                        "chunk_id": chunk.get("chunk_id"),
                        "chunk_index": chunk.get("chunk_index"),
                        "similarity_score": score
                    })

            prompt = f"""
            Given the following claim and the related evidence context, determine whether the claim is:
            - Supported
            - Partially Supported
            - Not Supported

            Then provide a short explanation referencing the provided evidence chunks where applicable.

            Claim: "{claim}"
            
            Evidence Context:
            {context_text}

            Provide a response in valid JSON format with the following keys:
            - "verdict": <"Supported" | "Partially Supported" | "Not Supported">
            - "explanation": <brief explanation referencing evidence>
            - "confidence": <float between 0.0 and 1.0>
            
            Ensure your entire response is just the JSON object and nothing else.
            """

            estimated_tokens = self._estimate_tokens(prompt)
            logger.info(f"Estimated prompt token count: {estimated_tokens}")
            
            if estimated_tokens > self.MAX_PROMPT_TOKENS:
                logger.error(f"Prompt size {estimated_tokens} exceeds maximum allowed budget {self.MAX_PROMPT_TOKENS}.")
                return "Error", "Evidence retrieval exceeded safe context size.", "error", []

            answer = self.ai_service.generate_response(prompt)
            result, explanation, color = self.parser_service.parse_verdict_response(answer)
            return result, explanation, color, retrieval_trace

        except RuntimeError as re:
            # Custom sanitized exceptions from inner services
            logger.error(f"Verification stopped due to RuntimeError: {str(re)}")
            return "Error", str(re), "error", []
        except Exception as e:
            # Absolute top-level catch-all to prevent UI leaking
            logger.error(f"Verification pipeline failed: {str(e)}", exc_info=True)
            return "Error", "Verification temporarily unavailable.", "error", []
