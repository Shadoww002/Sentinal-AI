import spacy

class ClaimExtractor:
    def __init__(self):
        # Load optimized pipeline
        self.nlp = spacy.load("en_core_web_sm", disable=["textcat", "lemmatizer"])

    def extract(self, text: str, max_claims: int = 3) -> list[str]:
        doc = self.nlp(text)
        claims = []
        
        for sent in doc.sents:
            # Look for objective entities
            verifiable_entities = {'ORG', 'GPE', 'MONEY', 'DATE', 'PERCENT', 'QUANTITY'}
            has_entity = any(ent.label_ in verifiable_entities for ent in sent.ents)
            has_root_verb = any(token.dep_ == "ROOT" and token.pos_ == "VERB" for token in sent)
            
            if has_entity and has_root_verb and 20 < len(sent.text) < 200:
                claims.append(sent.text.strip())
                
        return claims[:max_claims] # Prevent bottlenecking downstream processes