from fastapi import APIRouter

utils_router = APIRouter()


@utils_router.get("/health-check/")
async def health_check():
    """Simple health check endpoint"""
    return {"status": "healthy"}
