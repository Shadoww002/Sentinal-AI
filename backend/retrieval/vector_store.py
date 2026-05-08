import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class EvidenceStore:
    def __init__(self):
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self.dimension = self.encoder.get_sentence_embedding_dimension()
        
    def get_top_evidence(self, claim: str, snippets: list[str], top_k: int = 2) -> list[str]:
        if not snippets or snippets[0].startswith("There is no"):
            return snippets
            
        index = faiss.IndexFlatIP(self.dimension)
        
        snippet_embeddings = self.encoder.encode(snippets, normalize_embeddings=True)
        index.add(np.array(snippet_embeddings, dtype=np.float32))
        
        claim_embedding = self.encoder.encode([claim], normalize_embeddings=True)
        distances, indices = index.search(np.array(claim_embedding, dtype=np.float32), min(top_k, len(snippets)))
        
        return [snippets[idx] for idx in indices[0] if idx != -1]