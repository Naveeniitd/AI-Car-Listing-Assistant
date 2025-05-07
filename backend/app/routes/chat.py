from fastapi import APIRouter, Depends
from app.schemas.chat import ChatMessage
from app.agents.main_agent import create_agent_executor
import redis
from app.core.config import settings
redis_client = redis.Redis.from_url(settings.REDIS_URL)
router = APIRouter()

@router.post("/chat")
async def handle_chat(request: ChatMessage):
    # Get chat history
    history = redis_client.lrange(f"chat:{request.session_id}", 0, -1) or []
    
    # Initialize agent
    agent = create_agent_executor()
    
    # Run conversation
    response = agent.invoke({
        "input": request.message,
        "chat_history": [h.decode() for h in history]
    })
    
    # Update history
    redis_client.rpush(f"chat:{request.session_id}", request.message, response["output"])
    
    return {"response": response["output"]}