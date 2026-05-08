import ollama
import logging

logger = logging.getLogger(__name__)

class ClaimExtractor:
    def __init__(self):
        self.model = "llama3"

    def extract(self, text: str, max_claims: int = 1) -> list[str]:
        # 🚨 THE FIX: Force a complete factual sentence (Subject + Verb + Object)
        prompt = f"""
        You are a robotic fact-checker. Rewrite the following headline into a single, simple, verifiable sentence.
        You MUST include the Subject, the Verb, and the Object. 
        Strip out all opinions, questions, and adjectives. 
        
        Example Input: "Decisive leader with street cred: Why BJP chose Suvendu Adhikari as Bengal CM"
        Example Output: BJP chose Suvendu Adhikari as Bengal CM.
        
        Example Input: "The company's amazing revenue tragically dropped by 20% in Q3."
        Example Output: The company revenue dropped by 20% in Q3.
        
        Headline: "{text}"
        Output ONLY the clean sentence. No quotes, no lists, no explanations.
        """
        
        try:
            response = ollama.chat(model=self.model, messages=[
                {"role": "user", "content": prompt}
            ])
            
            # Clean up the output
            query = response['message']['content'].strip(' "\'\n')
            
            if query:
                return [query]
            return [text]
                
        except Exception as e:
            logger.error(f"LLM Extraction failed: {e}")
            return [text]