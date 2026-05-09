from backend.services.claim_extractor import ClaimExtractor
from backend.verification.nli_verifier import LLMVerifier
from backend.retrieval.news_fetcher import NewsFetcher      
from backend.retrieval.vector_store import EvidenceStore
import asyncio
import logging

logger = logging.getLogger(__name__)

class FactCheckingPipeline:
    def __init__(self):
        self.extractor = ClaimExtractor()
        self.verifier = LLMVerifier()
        self.fetcher = NewsFetcher()
        self.store = EvidenceStore()
    
    async def _process_single_claim(self, claim: str) -> dict:
        """Helper to process a single claim in a background thread."""
        def run_sync_pipeline():
            try:
                # 1. Fetch live news
                raw_sources = self.fetcher.search(claim)
                
                # 2. Extract text bodies for FAISS vector math
                snippets = [source['body'] for source in raw_sources]
                best_evidence_list = self.store.get_top_evidence(claim, snippets)
                
                # 3. Handle the short-circuit fallback
                best_evidence = (
                    best_evidence_list[0] 
                    if best_evidence_list 
                    else "There is no currently available news or evidence regarding this claim."
                )
                
                # 4. Verify
                verification = self.verifier.verify(claim, best_evidence)
                
                return {
                    "claim": claim,
                    "verdict": verification['verdict'],
                    "explanation": verification['explanation'], 
                    "confidence": verification.get('confidence', 0.0), 
                    "sources": raw_sources
                }
            except Exception as e:
                logger.error(f"Error processing claim '{claim}': {e}")
                return {
                    "claim": claim, 
                    "verdict": "Unverified", 
                    "explanation": "System error during processing.", 
                    "confidence": 0.0, 
                    "sources": []
                }
        
        # Offload blocking CPU/Network tasks to a background thread
        return await asyncio.to_thread(run_sync_pipeline)
        
    async def process(self, text: str) -> dict:
        """Main entry point: Parallelizes verification of all extracted claims."""
        # Extraction is usually fast enough to keep sync, 
        # but if it becomes a bottleneck, wrap it in to_thread as well.
        claims = self.extractor.extract(text)
        
        if not claims:
            return self._aggregate([])

        # 🚨 THE UPGRADE: Fire off all verification tasks simultaneously
        tasks = [self._process_single_claim(claim) for claim in claims]
        
        # Gather all results in parallel
        results = await asyncio.gather(*tasks)
            
        return self._aggregate(results)

    def _aggregate(self, results: list) -> dict:
        if not results:
            return {"overall_verdict": "No verifiable claims found", "analysis": []}

        verdicts = [r['verdict'] for r in results]
        
        # Logic hierarchy logic
        if 'False' in verdicts:
            final_verdict = "Misleading/False"
        elif 'Unverified' in verdicts:
            final_verdict = "Unverified (Insufficient Evidence)"
        elif 'True' in verdicts:
            final_verdict = "Likely True"
        else:
            final_verdict = "Unknown"
            
        return {"overall_verdict": final_verdict, "analysis": results}