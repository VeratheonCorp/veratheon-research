import redis
import json
import logging
import os
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

async def publish_status_update_task(status: str, details: Optional[Dict[str, Any]] = None) -> bool:
    """
    Task to publish status updates to Redis pub/sub channel.
    
    Args:
        status: Status message to publish
        details: Optional dictionary with additional details
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        redis_client = redis.from_url(redis_url, decode_responses=True)
        
        message = {
            "status": status,
            "timestamp": None,  # Will be set by Redis or consuming application
            "details": details or {}
        }
        
        channel = "research_status_updates"
        
        # Publish the message
        result = redis_client.publish(channel, json.dumps(message))
        
        logger.info(f"Published status update to Redis channel '{channel}': {status}")
        logger.debug(f"Status update details: {json.dumps(message, indent=2)}")
        
        redis_client.close()
        
        return result > 0  # Returns True if at least one subscriber received the message
        
    except Exception as e:
        logger.error(f"Failed to publish status update to Redis: {str(e)}")
        return False