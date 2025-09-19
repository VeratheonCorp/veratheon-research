import logging
import json
import os
from datetime import datetime
from typing import Dict, Any, Optional
import redis

logger = logging.getLogger(__name__)


async def publish_status_update_task(
    status: str,
    details: Optional[Dict[str, Any]] = None
) -> bool:
    """
    Publish status update to Redis pub/sub channel.

    Args:
        status: Status string (e.g., "starting", "completed", "error")
        details: Optional dictionary with additional details

    Returns:
        bool: True if there are subscribers, False otherwise
    """
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    try:
        # Create Redis client for pub/sub
        redis_client = redis.from_url(redis_url, decode_responses=True)

        # Prepare message
        message = {
            "status": status,
            "details": details or {},
            "timestamp": datetime.now().isoformat()
        }

        # Publish to channel
        channel = "research_status_updates"
        subscriber_count = redis_client.publish(channel, json.dumps(message))

        # Close connection
        redis_client.close()

        # Return True if there are subscribers, False otherwise
        return subscriber_count > 0

    except Exception as e:
        logger.error(f"Failed to publish status update: {str(e)}")
        return False
