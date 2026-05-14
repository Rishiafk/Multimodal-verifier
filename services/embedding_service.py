import os
import uuid
import datetime
import math
from typing import List, Dict, Any

# We use sentence_transformers for local, fast semantic embeddings
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

try:
    import nltk
    # Auto-download punkt if missing
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        print("Downloading NLTK punkt tokenizer...")
        nltk.download('punkt', quiet=True)
        nltk.download('punkt_tab', quiet=True)
except ImportError:
    nltk = None

class EmbeddingService:
    _model_cache = {}

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initializes the EmbeddingService. 
        Loads a pre-trained sentence transformer model for semantic embeddings.
        This foundation prepares the system for future RAG (Retrieval-Augmented Generation).
        """
        self.model_name = model_name
        self.model = self._get_model(model_name)
    
    @classmethod
    def _get_model(cls, model_name: str):
        if not SentenceTransformer:
            print("Warning: sentence_transformers not installed. Embedding features disabled.")
            return None
        if model_name not in cls._model_cache:
            cls._model_cache[model_name] = SentenceTransformer(model_name)
        return cls._model_cache[model_name]
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generates a semantic vector embedding for a given text.
        """
        if not self.model:
            return []
        
        # Encode the text into a vector (returns a numpy array, we convert to list)
        embedding = self.model.encode(text)
        return embedding.tolist()
    
    def _split_into_sentences(self, text: str) -> List[str]:
        if nltk:
            return nltk.sent_tokenize(text)
        else:
            # Graceful fallback to basic regex splitting if nltk is not available
            import re
            sentences = re.split(r'(?<=[.!?]) +', text.strip())
            return [s.strip() for s in sentences if s.strip()]

    def chunk_evidence(self, evidence: str, target_chunk_size: int = 150, overlap: int = 30) -> List[str]:
        """
        Splits large evidence text into smaller overlapping chunks, respecting sentence boundaries.
        """
        sentences = self._split_into_sentences(evidence)
        chunks = []
        
        if not sentences:
            return chunks
            
        current_chunk = []
        current_length = 0
        
        i = 0
        while i < len(sentences):
            sentence = sentences[i]
            sentence_len = len(sentence.split())
            
            # Allow slight overfill (e.g. up to 20%) to avoid stranding single sentences,
            # unless the chunk is empty.
            if not current_chunk or (current_length + sentence_len <= target_chunk_size * 1.2):
                current_chunk.append(sentence)
                current_length += sentence_len
                i += 1
            else:
                chunks.append(" ".join(current_chunk))
                
                # Compute overlap
                overlap_chunk = []
                overlap_len = 0
                for s in reversed(current_chunk):
                    s_len = len(s.split())
                    # Ensure we don't just take the whole chunk again if target size is small
                    if overlap_len + s_len <= overlap and len(overlap_chunk) < len(current_chunk) - 1:
                        overlap_chunk.insert(0, s)
                        overlap_len += s_len
                    else:
                        break
                
                # Fallback if no overlap could be formed (e.g., chunk was a single huge sentence)
                if not overlap_chunk and len(current_chunk) > 1:
                    overlap_chunk = [current_chunk[-1]]
                    overlap_len = len(overlap_chunk[0].split())
                    
                current_chunk = overlap_chunk
                current_length = overlap_len

        if current_chunk:
            chunks.append(" ".join(current_chunk))
            
        return chunks
    
    def process_and_embed_evidence(self, evidence: str, source_id: str = None, source_type: str = "text") -> List[Dict[str, Any]]:
        """
        Full pipeline to chunk evidence and generate embeddings for each chunk.
        Returns a list of dictionaries containing the chunk metadata and its embedding.
        """
        chunks = self.chunk_evidence(evidence)
        embedded_chunks = []
        
        if not source_id:
            source_id = str(uuid.uuid4())
            
        for index, chunk in enumerate(chunks):
            embedding = self.generate_embedding(chunk)
            token_count = len(chunk.split())  # Rough word-based estimate
            
            chunk_metadata = {
                "chunk_id": str(uuid.uuid4()),
                "chunk_index": index,
                "source_id": source_id,
                "source_type": source_type,
                "token_count": token_count,
                "embedding_model": self.model_name,
                "modality": "text",
                "created_at": datetime.datetime.utcnow().isoformat() + "Z",
                "text": chunk,
                "embedding": embedding
            }
            embedded_chunks.append(chunk_metadata)
            
        return embedded_chunks

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity without strictly requiring numpy."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm_a = math.sqrt(sum(a * a for a in vec1))
        norm_b = math.sqrt(sum(b * b for b in vec2))
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return dot_product / (norm_a * norm_b)

    def retrieve_similar_chunks(self, query_embedding: List[float], stored_embeddings: List[Dict[str, Any]], top_k: int = 3, threshold: float = 0.5) -> List[Dict[str, Any]]:
        """
        Compares the query_embedding against stored_embeddings using cosine similarity
        and returns the top_k most relevant chunks.
        """
        results = []
        for chunk_data in stored_embeddings:
            chunk_emb = chunk_data.get('embedding')
            if not chunk_emb:
                continue
                
            score = self._cosine_similarity(query_embedding, chunk_emb)
            if score >= threshold:
                results.append((score, chunk_data))
                
        # Sort by score descending
        results.sort(key=lambda x: x[0], reverse=True)
        
        # Return top_k chunks, including the similarity score in the returned dict
        top_results = []
        for score, data in results[:top_k]:
            result_data = data.copy()
            result_data['similarity_score'] = score
            top_results.append(result_data)
            
        return top_results
