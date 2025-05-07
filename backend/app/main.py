from fastapi import FastAPI
from app.routes import upload, chat

app = FastAPI(title="AI Car Listing Assistant")

# Include routers
app.include_router(upload.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "healthy"}