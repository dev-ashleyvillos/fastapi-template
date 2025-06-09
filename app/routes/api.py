from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["api"])

@router.get("/test")
async def test_endpoint():
    """Test endpoint"""
    return {"message": "API is working!", "endpoint": "/api/test"}
