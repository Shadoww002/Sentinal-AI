from gnews import GNews
import logging

logger = logging.getLogger(__name__)

class NewsFetcher:
    def __init__(self):
        # Initialize Google News. 
        # We set language to English and country to India to highly optimize for your queries.
        self.google_news = GNews(language='en', country='IN', max_results=4)

    def search(self, claim: str) -> list[dict]:
        sources = []
        try:
            # Query Google News directly
            results = self.google_news.get_news(claim)
            
            for r in results:
                # Google News returns a 'title' and a 'description' snippet.
                # We combine them so Llama 3 has maximum context to read.
                snippet = f"{r.get('title', '')}. {r.get('description', '')}"
                
                sources.append({
                    "title": r.get('title', 'Google News Article'),
                    "body": snippet,
                    "href": r.get('url', '#')
                })
                
        except Exception as e:
            logger.error(f"Google News API failed: {e}")
            
        # Fallback if no internet results
        if not sources:
            return [{
                "title": "No Sources Found", 
                "body": "There is no currently available news or evidence regarding this claim.", 
                "href": "#"
            }]
            
        return sources