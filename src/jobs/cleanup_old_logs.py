"""
Cleanup job for old system logs.

This job runs weekly to delete logs older than 30 days.
"""

from src.lib.supabase_client import get_supabase_client
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


def cleanup_old_logs(retention_days: int = 30) -> dict:
    """
    Delete system logs older than retention_days.

    Args:
        retention_days: Number of days to retain logs (default: 30)

    Returns:
        dict: Summary of cleanup operation with deleted_count
    """
    try:
        client = get_supabase_client()
        cutoff_date = (datetime.now() - timedelta(days=retention_days)).isoformat()

        # Delete logs older than cutoff date
        response = client.table("system_logs") \
            .delete() \
            .lt("created_at", cutoff_date) \
            .execute()

        deleted_count = len(response.data) if response.data else 0

        logger.info(f"Cleanup completed: Deleted {deleted_count} old logs (older than {retention_days} days)")

        return {
            "status": "success",
            "deleted_count": deleted_count,
            "retention_days": retention_days,
            "cutoff_date": cutoff_date,
            "timestamp": datetime.now().isoformat()
        }

    except Exception as e:
        logger.error(f"Error during logs cleanup: {str(e)}")
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

    result = cleanup_old_logs()
    print(f"Cleanup result: {result}")
