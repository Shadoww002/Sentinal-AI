from duckduckgo_search import DDGS
import logging

logger = logging.getLogger(__name__)

class NewsFetcher:
    def __init__(self):
        self.ddgs = DDGS()

    def search(self, claim: str, max_results: int = 3) -> list[dict]:
        sources = []
        try:
            results = self.ddgs.text(claim, max_results=max_results)
            
            for r in results:
                if 'body' in r and 'href' in r:
                    sources.append({
                        "title": r.get('title', 'Web Article'),
                        "body": r['body'],
                        "href": r['href']
                    })
        except Exception as e:
            logger.error(f"Search API failed: {e}")
            
        # Fallback if no internet results
        if not sources:
            return [{
                "title": "No Sources Found", 
                "body": "There is no currently available news or evidence regarding this claim.", 
                "href": "#"
            }]
            
        return sources