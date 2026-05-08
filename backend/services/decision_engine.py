from backend.services.claim_extractor import ClaimExtractor
from backend.verification.nli_verifier import NLIVerifier
# ... imports for Fetcher and EvidenceStore     
from backend.retrieval.news_fetcher import NewsFetcher      
from backend.retrieval.vector_store import EvidenceStore

class FactCheckingPipeline:
    def __init__(self):
        self.extractor = ClaimExtractor()
        self.verifier = NLIVerifier()
        self.fetcher = NewsFetcher()
        self.store = EvidenceStore()
        
    def process(self, text: str) -> dict:
        claims = self.extractor.extract(text)
        results = []
        
        for claim in claims:
            # 1. Fetch live news (Now returns a list of dicts with URLs)
            raw_sources = self.fetcher.search(claim)
            
            # 2. Extract ONLY the text bodies to pass into FAISS for vector math
            snippets = [source['body'] for source in raw_sources]
            best_evidence_list = self.store.get_top_evidence(claim, snippets)
            best_evidence = best_evidence_list[0] if best_evidence_list else "No evidence."
            
            # 3. Verify
            verification = self.verifier.verify(claim, best_evidence)
            
            # 4. Explain
            explanation = f"We found this claim to be {verification['verdict']} with {verification['confidence']:.0%} confidence because real-time evidence states: '{best_evidence}'"
            
            results.append({
                "claim": claim,
                "verdict": verification['verdict'],
                "explanation": explanation,
                "sources": raw_sources  # 
            })
            
        return self._aggregate(results)

    def _aggregate(self, results: list) -> dict:
        if not results:
            return {"overall_verdict": "No verifiable claims found", "analysis": []}

        # Extract all the individual verdicts into a simple list
        verdicts = [r['verdict'] for r in results]
        
        # Strict logic hierarchy: False overrides everything. 
        # Unverified overrides True. 
        # It is only "True" if EVERY extracted claim is proven True.
        
        if 'False' in verdicts:
            final_verdict = "Misleading/False"
        elif 'Unverified' in verdicts:
            final_verdict = "Unverified (Insufficient Evidence)"
        elif 'True' in verdicts:
            final_verdict = "Likely True"
        else:
            final_verdict = "Unknown"
            
        return {"overall_verdict": final_verdict, "analysis": results}