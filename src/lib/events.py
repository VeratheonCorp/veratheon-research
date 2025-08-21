"""
Event emission utilities for research flow progress tracking.
This is the single source of truth for event emissions.
"""

import json
import redis
import asyncio
from typing import Any, Optional
from dotenv import load_dotenv
import os

load_dotenv()

# Redis configuration
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
REDIS_CHANNEL_PREFIX = "research_events"

class EventEmitter:
    """Handles event emission to Redis for real-time updates."""
    
    def __init__(self):
        self._redis_client = None
    
    @property
    def redis_client(self):
        """Lazy initialization of Redis client."""
        if self._redis_client is None:
            try:
                self._redis_client = redis.from_url(REDIS_URL, decode_responses=True)
                # Test connection
                self._redis_client.ping()
            except Exception as e:
                print(f"Warning: Redis connection failed: {e}")
                print("Events will not be broadcast to WebSocket clients")
                self._redis_client = None
        return self._redis_client
    
    def emit_event(self, symbol: str, event_type: str, stage: Optional[str] = None, 
                   message: Optional[str] = None, data: Optional[Any] = None):
        """Emit a research event to Redis pub/sub."""
        if not self.redis_client:
            return
        
        try:
            event = {
                "type": event_type,
                "symbol": symbol.upper(),
                "stage": stage,
                "message": message,
                "data": data,
                "timestamp": asyncio.get_event_loop().time() if asyncio._get_running_loop() else None
            }
            
            channel = f"{REDIS_CHANNEL_PREFIX}:{symbol.upper()}"
            self.redis_client.publish(channel, json.dumps(event))
            
        except Exception as e:
            print(f"Warning: Failed to emit event: {e}")

# Global event emitter instance
event_emitter = EventEmitter()

def emit_research_event(symbol: str, event_type: str, stage: Optional[str] = None, 
                       message: Optional[str] = None, data: Optional[Any] = None):
    """
    Emit a research event.
    
    Args:
        symbol: Stock symbol
        event_type: Type of event (stage_start, stage_complete, research_started, etc.)
        stage: Research stage name (optional)
        message: Human-readable message (optional)
        data: Additional data payload (optional)
    """
    event_emitter.emit_event(symbol, event_type, stage, message, data)