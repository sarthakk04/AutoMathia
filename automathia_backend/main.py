from fastapi import FastAPI
from routes import auth
from utils.api_response import success_response

# Initialize FastAPI app
app = FastAPI(
    title="Automathia Backend",
    version="1.0.0",
    description="Backend API for Automathia platform 🚀"
)

# Include Auth routes
app.include_router(auth.router)

# Root route
@app.get("/")
async def root():
    return success_response(message="Automathia Backend Running ✅")
