from fastapi import FastAPI

app = FastAPI(
    title="JobPilot AI",
    description="AI-powered job discovery, matching, and application assistant.",
    version="0.1.0",
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to JobPilot AI"
    }