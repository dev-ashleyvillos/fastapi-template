"""example.py - FastAPI Documentation Examples

This file contains examples of how to properly document FastAPI routes and endpoints.
It serves as a reference for implementing well-documented APIs and does not serve any
functional purpose in the actual application.

Use these examples as templates when creating real API endpoints
"""

from fastapi import APIRouter, Query, Path, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/example", tags=["examples"])

# Pydantic models for request/response documentation
class ChatMessage(BaseModel):
    message: str = Field(..., description="The user's message", example="Hello, how are you?")
    user_id: Optional[str] = Field(None, description="Optional user identifier", example="user123")

class ChatResponse(BaseModel):
    response: str = Field(..., description="The chatbot's response")
    timestamp: datetime = Field(..., description="When the response was generated")
    message_id: str = Field(..., description="Unique identifier for this response")

class UserProfile(BaseModel):
    name: str = Field(..., description="User's full name", example="John Doe")
    email: str = Field(..., description="User's email address", example="john@example.com")
    age: Optional[int] = Field(None, ge=1, le=120, description="User's age", example=25)

@router.get("/simple")
async def simple_example():
    """
    Simple GET endpoint example.
    
    This is the most basic endpoint with no parameters.
    """
    return {"message": "This is a simple example endpoint"}

@router.get("/query-params")
async def query_params_example(
    name: str = Query(..., description="Your name", example="John"),
    age: int = Query(
        default=25,
        ge=1,
        le=120,
        description="Your age (must be between 1-120)",
        example=25
    ),
    city: Optional[str] = Query(
        None,
        description="Your city (optional)",
        example="New York"
    )
):
    """
    Example endpoint demonstrating query parameters.
    
    Shows different types of query parameters:
    - **name**: Required string parameter
    - **age**: Integer with validation (1-120)
    - **city**: Optional string parameter
    """
    response = {"name": name, "age": age}
    if city:
        response["city"] = city
    return response

@router.get("/users/{user_id}")
async def path_params_example(
    user_id: int = Path(
        ...,
        ge=1,
        description="The ID of the user to retrieve",
        example=123
    ),
    include_profile: bool = Query(
        default=False,
        description="Whether to include full profile information"
    )
):
    """
    Example endpoint demonstrating path parameters.
    
    Shows how to use path parameters with validation:
    - **user_id**: Required integer path parameter (must be >= 1)
    - **include_profile**: Optional query parameter to modify response
    """
    if user_id == 404:
        raise HTTPException(status_code=404, detail="User not found")
    
    user_data = {"id": user_id, "username": f"user_{user_id}"}
    
    if include_profile:
        user_data.update({
            "email": f"user_{user_id}@example.com",
            "created_at": datetime.now(),
            "is_active": True
        })
    
    return user_data

@router.post("/chat", response_model=ChatResponse)
async def chat_example(
    request: ChatMessage,
    model: str = Query(
        default="gpt-3.5-turbo", 
        description="The AI model to use for the response",
        example="gpt-3.5-turbo"
    ),
    max_tokens: int = Query(
        default=150,
        ge=1,
        le=2000,
        description="Maximum number of tokens in the response",
        example=150
    ),
    temperature: float = Query(
        default=0.7,
        ge=0.0,
        le=2.0,
        description="Controls randomness in the response (0.0 = deterministic, 2.0 = very random)",
        example=0.7
    )
):
    """
    Example POST endpoint with request body and query parameters.
    
    This demonstrates a typical chat API endpoint that would be used in a RAG chatbot:
    
    **Request Body:**
    - **message**: The user's input message
    - **user_id**: Optional identifier for the user
    
    **Query Parameters:**
    - **model**: AI model to use
    - **max_tokens**: Maximum response length
    - **temperature**: Controls response randomness
    """
    
    # Simulate a chatbot response
    response_text = f"You said: '{request.message}'. This is a simulated response using {model} model with {max_tokens} max tokens and {temperature} temperature."
    
    return ChatResponse(
        response=response_text,
        timestamp=datetime.now(),
        message_id=f"msg_{hash(request.message)}_{int(datetime.now().timestamp())}"
    )

@router.post("/users", response_model=UserProfile)
async def create_user_example(user: UserProfile):
    """
    Example POST endpoint with Pydantic model validation.
    
    Shows how to accept and validate JSON request bodies:
    - **name**: Required string field
    - **email**: Required email field  
    - **age**: Optional integer with validation (1-120)
    
    The response will echo back the created user with validation applied.
    """
    return user

@router.get("/conversations/{conversation_id}/messages")
async def pagination_example(
    conversation_id: str = Path(
        ...,
        description="Unique identifier for the conversation",
        example="conv_123"
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Number of messages to retrieve (1-100)",
        example=10
    ),
    offset: int = Query(
        default=0,
        ge=0,
        description="Number of messages to skip for pagination",
        example=0
    ),
    search: Optional[str] = Query(
        None,
        description="Optional search term to filter messages",
        example="hello"
    )
):
    """
    Example endpoint demonstrating pagination and search.
    
    Shows common patterns for list endpoints:
    - **conversation_id**: Required path parameter
    - **limit**: How many items to return (with validation)
    - **offset**: How many items to skip (for pagination)
    - **search**: Optional search/filter parameter
    
    Try these examples:
    - `/example/conversations/conv_123/messages` - Basic usage
    - `/example/conversations/conv_123/messages?limit=5&offset=10` - Pagination
    - `/example/conversations/conv_404/messages` - Error example
    """
    
    # Simulate error for demonstration
    if conversation_id == "conv_404":
        raise HTTPException(
            status_code=404, 
            detail={
                "error": "Conversation not found",
                "conversation_id": conversation_id,
                "suggestion": "Try using 'conv_123' for a working example"
            }
        )
    
    # Generate mock messages
    all_messages = [
        {"id": f"msg_{i}", "content": f"Message {i} content", "timestamp": datetime.now()}
        for i in range(100)
    ]
    
    # Apply search filter if provided
    if search:
        all_messages = [msg for msg in all_messages if search.lower() in msg["content"].lower()]
    
    # Apply pagination
    paginated_messages = all_messages[offset:offset + limit]
    
    return {
        "conversation_id": conversation_id,
        "messages": paginated_messages,
        "pagination": {
            "total_messages": len(all_messages),
            "limit": limit,
            "offset": offset,
            "has_more": offset + limit < len(all_messages)
        },
        "search": search
    }

@router.get("/error-examples/{error_code}")
async def error_examples(
    error_code: int = Path(
        ...,
        description="Error code to simulate (400, 401, 403, 404, 500)",
        example=404
    )
):
    """
    Example endpoint demonstrating different HTTP error responses.
    
    Try different error codes:
    - **400**: Bad Request
    - **401**: Unauthorized  
    - **403**: Forbidden
    - **404**: Not Found
    - **500**: Internal Server Error
    - **Any other**: Returns success message
    """
    
    error_messages = {
        400: "Bad Request - Invalid input provided",
        401: "Unauthorized - Please provide valid authentication",
        403: "Forbidden - You don't have permission to access this resource",
        404: "Not Found - The requested resource was not found",
        500: "Internal Server Error - Something went wrong on our end"
    }
    
    if error_code in error_messages:
        raise HTTPException(
            status_code=error_code,
            detail={
                "error": error_messages[error_code],
                "code": error_code,
                "timestamp": datetime.now().isoformat()
            }
        )
    
    return {
        "message": f"No error simulation for code {error_code}",
        "available_codes": list(error_messages.keys())
    }
