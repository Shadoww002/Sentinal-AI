import trafilatura
import re

def extract_text_from_url(url: str) -> str:
    """Safely extracts main content from a live URL."""
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        raise ValueError("Could not fetch the URL. It may be blocked or invalid.")
    
    text = trafilatura.extract(downloaded, include_comments=False, include_tables=False)
    if not text:
        return ""
        
    # Clean irregular whitespace
    return re.sub(r'\s+', ' ', text).strip()