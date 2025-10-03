"""
Cleanup job for old research jobs.

This job runs daily to delete completed/failed jobs older than 7 days.
"""

from src.lib.supabase_client import get_supabase_client
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def cleanup_old_jobs(retention_days: int = 7) -> dict:
    """
    Delete completed/failed jobs older than retention_days.

    Args:
        retention_days: Number of days to retain jobs (default: 7)

    Returns:
        dict: Summary of cleanup operation with deleted_count
    """
    try:
        client = get_supabase_client()
        cutoff_date = (datetime.now() - timedelta(days=retention_days)).isoformat()

        # Delete jobs that are completed or failed and older than cutoff date
        response = client.table("research_jobs") \
            .delete() \
            .in_("status", ["completed", "failed"]) \
            .lt("updated_at", cutoff_date) \
            .execute()

        deleted_count = len(response.data) if response.data else 0

        logger.info(f"Cleanup completed: Deleted {deleted_count} old jobs (older than {retention_days} days)")

        return {
            "status": "success",
            "deleted_count": deleted_count,
            "retention_days": retention_days,
            "cutoff_date": cutoff_date,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error during jobs cleanup: {str(e)}")
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

    result = cleanup_old_jobs()
    print(f"Cleanup result: {result}")
