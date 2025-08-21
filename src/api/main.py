from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import json
import redis
import os
from dotenv import load_dotenv
from src.prefect.flows.research_flow import main_research_flow
from src.research.trade_ideas.trade_idea_models import TradeIdea

load_dotenv()

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
REDIS_CHANNEL_PREFIX = "research_events"

app = FastAPI(
    title="Market Research Agent API",
    description="API for stock market research and analysis with WebSocket support",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Redis connection
redis_client = None

def get_redis_client():
    global redis_client
    if redis_client is None:
        try:
            redis_client = redis.from_url(REDIS_URL, decode_responses=True)
            redis_client.ping()
        except Exception as e:
            print(f"Warning: Redis connection failed: {e}")
            redis_client = None
    return redis_client

class ResearchRequest(BaseModel):
    symbol: str

class ResearchResponse(BaseModel):
    symbol: str
    status: str
    message: str

@app.get("/")
async def root():
    return {"message": "Market Research Agent API with WebSocket support"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.websocket("/ws/updates/{symbol}")
async def websocket_updates_endpoint(websocket: WebSocket, symbol: str):
    """
    WebSocket endpoint for receiving real-time research updates via Redis pub/sub.
    Clients connect here to listen for updates as research progresses.
    """
    if not symbol or len(symbol) > 10 or not symbol.isalpha():
        await websocket.close(code=1003, reason="Invalid stock symbol")
        return
    
    symbol = symbol.upper()
    await websocket.accept()
    
    # Get Redis client for pub/sub
    redis_client = get_redis_client()
    if not redis_client:
        await websocket.close(code=1011, reason="Redis unavailable")
        return
    
    # Subscribe to Redis channel for this symbol
    pubsub = redis_client.pubsub()
    channel = f"{REDIS_CHANNEL_PREFIX}:{symbol}"
    pubsub.subscribe(channel)
    
    try:
        # Send initial connection confirmation
        await websocket.send_text(json.dumps({
            "type": "connected",
            "symbol": symbol,
            "message": f"Connected to update stream for {symbol}"
        }))
        
        # Listen for Redis messages
        async def redis_listener():
            for message in pubsub.listen():
                if message['type'] == 'message':
                    try:
                        await websocket.send_text(message['data'])
                    except:
                        break
        
        # Start Redis listener task
        listener_task = asyncio.create_task(redis_listener())
        
        # Keep connection alive and handle client messages
        try:
            while True:
                data = await websocket.receive_text()
                # Echo back for heartbeat/testing
                await websocket.send_text(json.dumps({
                    "type": "heartbeat",
                    "message": f"Received: {data}"
                }))
        except WebSocketDisconnect:
            pass
            
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        pubsub.unsubscribe(channel)
        pubsub.close()

async def run_research_with_events(symbol: str):
    """Run the research flow - events are emitted from within the research flow itself."""
    try:
        # Run the original research flow which now emits events internally
        trade_idea: TradeIdea = await main_research_flow(symbol)
        return trade_idea
        
    except Exception as e:
        # Emit error event if research fails
        redis_client = get_redis_client()
        if redis_client:
            error_event = {
                "type": "research_error",
                "symbol": symbol.upper(),
                "message": f"Research failed for {symbol}: {str(e)}",
                "timestamp": asyncio.get_event_loop().time()
            }
            channel = f"{REDIS_CHANNEL_PREFIX}:{symbol.upper()}"
            redis_client.publish(channel, json.dumps(error_event))
        raise e

@app.post("/research/{symbol}", response_model=ResearchResponse)
async def trigger_research(symbol: str, background_tasks: BackgroundTasks):
    """
    REST endpoint to trigger research for a symbol.
    Research runs in background and pushes updates via WebSocket.
    """
    if not symbol or len(symbol) > 10 or not symbol.isalpha():
        raise HTTPException(status_code=400, detail="Invalid stock symbol")
    
    symbol = symbol.upper()
    
    # Start research in background
    background_tasks.add_task(run_research_with_events, symbol)
    
    return ResearchResponse(
        symbol=symbol,
        status="started",
        message=f"Research started for {symbol}. Connect to /ws/updates/{symbol} for real-time updates."
    )