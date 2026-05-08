from backend.services.claim_extractor import ClaimExtractor
from backend.verification.nli_verifier import LLMVerifier
# ... imports for Fetcher and EvidenceStore     
from backend.retrieval.news_fetcher import NewsFetcher      
from backend.retrieval.vector_store import EvidenceStore

class FactCheckingPipeline:
    def __init__(self):
        self.extractor = ClaimExtractor()
        self.verifier = LLMVerifier()
        self.fetcher = NewsFetcher()
        self.store = EvidenceStore()
        
    def process(self, text: str) -> dict:
        claims = self.extractor.extract(text)
        results = []
        
        for claim in claims:
            # 1. Fetch live news
            raw_sources = self.fetcher.search(claim)
            
            # 2. Extract text bodies for FAISS vector math
            snippets = [source['body'] for source in raw_sources]
            best_evidence_list = self.store.get_top_evidence(claim, snippets)
            
            # 🚨 FIX: Pass the exact string the Verifier needs to short-circuit!
            best_evidence = best_evidence_list[0] if best_evidence_list else "There is no currently available news or evidence regarding this claim."
            
            # 3. Verify (LLM generates its own explanation)
            verification = self.verifier.verify(claim, best_evidence)
            
            results.append({
                "claim": claim,
                "verdict": verification['verdict'],
                "explanation": verification['explanation'], # Pulled directly from Llama 3
                "confidence": verification.get('confidence', 0.0), 
                "sources": raw_sources
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