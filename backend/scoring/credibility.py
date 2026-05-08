DOMAIN_WEIGHTS = {
    "reuters.com": 1.0,
    "apnews.com": 1.0,
    "theonion.com": 0.1,
    "naturalnews.com": 0.2
}

def calculate_final_score(nli_confidence: float, source_url: str) -> float:
    domain = source_url.split('/')[2].replace('www.', '')
    weight = DOMAIN_WEIGHTS.get(domain, 0.7) 
    return nli_confidence * weight