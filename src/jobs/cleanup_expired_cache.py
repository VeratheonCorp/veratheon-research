"""
Cleanup job for expired cache entries.

This job runs daily to delete expired cache entries from the research_cache table.
"""

from src.lib.supabase_client import get_supabase_client
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def cleanup_expired_cache() -> dict:
    """
    Delete expired cache entries from research_cache table.

    Returns:
        dict: Summary of cleanup operation with deleted_count
    """
    try:
        client = get_supabase_client()
        now = datetime.now().isoformat()

        # Delete all entries where expires_at is in the past
        response = client.table("research_cache") \
            .delete() \
            .lt("expires_at", now) \
            .execute()

        deleted_count = len(response.data) if response.data else 0

        logger.info(f"Cleanup completed: Deleted {deleted_count} expired cache entries")

        return {
            "status": "success",
            "deleted_count": deleted_count,
            "timestamp": now
        }

    except Exception as e:
        logger.error(f"Error during cache cleanup: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }


if __name__ == "__main__":
    # Configure logging for standalone execution
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    result = cleanup_expired_cache()
    print(f"Cleanup result: {result}")
