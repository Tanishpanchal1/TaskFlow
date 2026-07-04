from fastapi import FastAPI

app = FastAPI(
    title="TaskFlow API",
    version="0.1.0",
    description="Production Ready Task Management Backend"
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to TaskFlow API"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }
