from fastapi import FastAPI

app = FastAPI(
    title="Q&A PDF Splitter API",
    description="API for separating questions and answers from a PDF.",
    version="0.1.0",
)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {
        "status": "ok",
        "message": "Q&A PDF Splitter API is running",
    }