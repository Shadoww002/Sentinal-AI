FROM python:3.10-slim
WORKDIR /app

# Install dependencies (CPU versions for cost-effective deployment)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu
RUN python -m spacy download en_core_web_sm

COPY ./backend /app/backend
EXPOSE 8000

# Run FastAPI via Uvicorn
CMD ["uvicorn", "backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]