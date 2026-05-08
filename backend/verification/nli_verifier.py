import ollama
import json
import logging

logger = logging.getLogger(__name__)

class LLMVerifier:
    def __init__(self):
        self.model = "llama3"

    def verify(self, claim: str, evidence: str) -> dict:
        # Short-circuit for empty evidence
        if "No internet evidence available" in evidence or "There is no currently available news" in evidence:
            return {
                "verdict": "Unverified",
                "confidence": 0.0,
                "explanation": "No live sources could be found on the internet to support or refute this claim."
            }

        # 🚨 THE FIX: Upgraded prompt with Temporal (Time) constraints
        prompt = f"""
        You are a strict, hyper-logical fact-checking AI. Compare the CLAIM against the EVIDENCE.
        
        CRITICAL RULES:
        1. TEMPORAL ACCURACY: Pay strict attention to verb tense. If the CLAIM states an event has already happened (past tense), but the EVIDENCE states it is pending, delayed, expected tomorrow, or still being discussed, you MUST rate the claim as "False" or "Misleading". 
        2. NO ASSUMPTIONS: Do not assume an outcome just because a process has started.
        
        CLAIM: "{claim}"
        EVIDENCE: "{evidence}"
        
        You MUST respond in this exact JSON format:
        {{
            "verdict": "True" | "False" | "Unverified",
            "confidence": 0.0 to 1.0,
            "reasoning": "A 1-2 sentence explanation of your logic, explicitly mentioning if timelines do not match."
        }}
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {"role": "user", "content": prompt}
            ], format='json')
            
            result = json.loads(response['message']['content'])
            
            return {
                "verdict": result.get("verdict", "Unverified"),
                "confidence": float(result.get("confidence", 0.5)),
                "explanation": result.get("reasoning", "The AI provided no reasoning.")
            }
            
        except Exception as e:
            logger.error(f"LLM Verification failed: {e}")
            return {"verdict": "Unverified", "confidence": 0.0, "explanation": "Verification engine error."}