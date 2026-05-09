import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import Optional
from backend.services.decision_engine import FactCheckingPipeline
from backend.utils.preprocessing import extract_text_from_url

app = FastAPI(title="FactCheck API")
pipeline = FactCheckingPipeline()

class CheckRequest(BaseModel):
    text: Optional[str] = None
    url: Optional[HttpUrl] = None

@app.post("/api/v1/verify")
async def verify_content(request: CheckRequest):
    if not request.text and not request.url:
        raise HTTPException(status_code=400, detail="Provide text or a URL.")
        
    content = request.text
    if request.url:
        try:
            content = extract_text_from_url(str(request.url))
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
            
    return await pipeline.process(content)