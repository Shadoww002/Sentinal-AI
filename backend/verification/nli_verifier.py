from transformers import pipeline

class NLIVerifier:
    def __init__(self):
        # DeBERTa-v3 is the current state-of-the-art for NLI tasks
        self.classifier = pipeline(
            "zero-shot-classification", 
            model="cross-encoder/nli-deberta-v3-small",
            use_fast=False
        )

    def verify(self, claim: str, evidence: str) -> dict:
        labels = ["supports the claim", "contradicts the claim", "is unrelated"]
        result = self.classifier(evidence + f" </s> {claim}", candidate_labels=labels)
        
        top_label = result['labels'][0]
        confidence = result['scores'][0]
        
        if top_label == "supports the claim":
            return {"verdict": "True", "confidence": confidence}
        elif top_label == "contradicts the claim":
            return {"verdict": "False", "confidence": confidence}
        return {"verdict": "Unverified", "confidence": confidence}