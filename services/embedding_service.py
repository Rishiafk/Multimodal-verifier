import os
from typing import List, Dict, Any

# We use sentence_transformers for local, fast semantic embeddings
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

class EmbeddingService:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """
        Initializes the EmbeddingService. 
        Loads a pre-trained sentence transformer model for semantic embeddings.
        This foundation prepares the system for future RAG (Retrieval-Augmented Generation).
        """
        if SentenceTransformer:
            # This model is small and fast, perfect for a baseline RAG pipeline.
            self.model = SentenceTransformer(model_name)
        else:
            self.model = None
            print("Warning: sentence_transformers not installed. Embedding features disabled.")
    
    def generate_embedding(self, text: str) -> List[float]:
        """
        Generates a semantic vector embedding for a given text.
        Future use: This will be used to embed the user's claim and compare it against evidence chunks.
        """
        if not self.model:
            return []
        
        # Encode the text into a vector (returns a numpy array, we convert to list)
        embedding = self.model.encode(text)
        return embedding.tolist()
    
    def chunk_evidence(self, evidence: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """
        Splits large evidence text into smaller overlapping chunks.
        Future use: When users upload huge documents or long texts, we chunk them so we can embed
        each chunk individually and retrieve only the most relevant ones.
        """
        words = evidence.split()
        chunks = []
        
        if not words:
            return chunks

        # Basic sliding window chunking
        for i in range(0, len(words), chunk_size - overlap):
            chunk = " ".join(words[i:i + chunk_size])
            chunks.append(chunk)
            
        return chunks
    
    def process_and_embed_evidence(self, evidence: str) -> List[Dict[str, Any]]:
        """
        Full pipeline to chunk evidence and generate embeddings for each chunk.
        Returns a list of dictionaries containing the text chunk and its embedding.
        
        Future use: 
        1. These objects will be saved to the local vector_store/.
        2. When a claim comes in, we embed the claim, run a cosine similarity search 
           against these stored chunk embeddings, and retrieve the top-K chunks.
        3. The top-K chunks are then sent to the AIService for verification (RAG).
        """
        chunks = self.chunk_evidence(evidence)
        embedded_chunks = []
        
        for chunk in chunks:
            embedded_chunks.append({
                "text": chunk,
                "embedding": self.generate_embedding(chunk)
            })
            
        return embedded_chunks

    def retrieve_similar_chunks(self, query_embedding: List[float], stored_embeddings: List[Dict[str, Any]], top_k: int = 3):
        """
        Placeholder method for future semantic retrieval logic.
        Will compare the query_embedding against stored_embeddings (e.g., using cosine similarity)
        and return the top_k most relevant chunks for the VerificationService.
        """
        # TODO: Implement cosine similarity calculation here or integrate with a local 
        # vector database like FAISS/ChromaDB in the vector_store/ directory.
        pass
