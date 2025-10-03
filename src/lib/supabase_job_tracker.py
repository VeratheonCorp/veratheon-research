"""Supabase-based job tracking system."""
import logging
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum
from src.lib.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

class JobStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


def get_user_friendly_status_message(status: JobStatus) -> str:
    """
    Get user-friendly status message for job statuses.

    Args:
        status: JobStatus enum value

    Returns:
        User-friendly message string, or the status value if no mapping exists
    """
    return str(status)

class JobTracker:
    """Supabase-based job tracking system."""

    def __init__(self):
        """Initialize job tracker with Supabase client."""
        self._client = None

    @property
    def client(self):
        """Get Supabase client connection."""
        if self._client is None:
            self._client = get_supabase_client()
        return self._client

    def close(self):
        """Close connection (no-op for Supabase compatibility with Redis interface)."""
        self._client = None

    def create_job(self, job_type: str, symbol: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a new job and return its ID.

        Args:
            job_type: Type of job (e.g., 'research')
            symbol: Stock symbol being analyzed
            metadata: Optional additional metadata

        Returns:
            Job ID as string
        """
        try:
            # Prepare metadata with job_type and other info
            job_metadata = metadata or {}
            job_metadata["job_type"] = job_type
            job_metadata["steps"] = []
            job_metadata["result"] = None

            # Insert job into Supabase
            response = self.client.table("research_jobs").insert({
                "symbol": symbol.upper(),
                "status": JobStatus.PENDING,
                "metadata": job_metadata
            }).execute()

            if response.data and len(response.data) > 0:
                job_id = str(response.data[0]["id"])
                logger.info(f"Created job {job_id} for {job_type} of {symbol}")
                return job_id
            else:
                raise Exception("Failed to create job - no data returned")

        except Exception as e:
            logger.error(f"Failed to create job: {str(e)}")
            raise

    def update_job_status(self, job_id: str, status: JobStatus, step: Optional[str] = None,
                         result: Optional[Dict[str, Any]] = None, error: Optional[str] = None) -> bool:
        """
        Update job status and add step information.

        Args:
            job_id: Job ID
            status: New job status
            step: Optional step description
            result: Optional result data (for completed jobs)
            error: Optional error message (for failed jobs)

        Returns:
            True if successful, False otherwise
        """
        try:
            # Get current job data to preserve metadata
            current_job = self.client.table("research_jobs").select("*").eq("id", job_id).execute()

            if not current_job.data or len(current_job.data) == 0:
                logger.error(f"Job {job_id} not found")
                return False

            current_metadata = current_job.data[0].get("metadata", {})

            # Add step if provided
            if step:
                steps = current_metadata.get("steps", [])
                steps.append({
                    "step": step,
                    "timestamp": datetime.now().isoformat(),
                    "status": status
                })
                current_metadata["steps"] = steps

            # Set result for completed jobs
            if result and status == JobStatus.COMPLETED:
                current_metadata["result"] = result

            # Prepare update data
            update_data = {
                "status": status,
                "updated_at": datetime.now().isoformat(),
                "metadata": current_metadata
            }

            # Set timestamps based on status
            if status == JobStatus.COMPLETED:
                update_data["completed_at"] = datetime.now().isoformat()
            elif status == JobStatus.FAILED:
                update_data["failed_at"] = datetime.now().isoformat()
                update_data["error"] = error

            # Update job in Supabase
            self.client.table("research_jobs").update(update_data).eq("id", job_id).execute()

            logger.info(f"Updated job {job_id} status to {status}" + (f" with step: {step}" if step else ""))
            return True

        except Exception as e:
            logger.error(f"Failed to update job {job_id}: {str(e)}")
            return False

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get job status and information.

        Args:
            job_id: Job ID

        Returns:
            Job data dict or None if not found
        """
        try:
            response = self.client.table("research_jobs").select("*").eq("id", job_id).execute()

            if not response.data or len(response.data) == 0:
                return None

            job_data = response.data[0]
            metadata = job_data.get("metadata", {})

            # Format response to match Redis interface
            return {
                "job_id": str(job_data["id"]),
                "job_type": metadata.get("job_type", "research"),
                "symbol": job_data["symbol"],
                "status": job_data["status"],
                "created_at": job_data["created_at"],
                "updated_at": job_data["updated_at"],
                "completed_at": job_data.get("completed_at"),
                "failed_at": job_data.get("failed_at"),
                "metadata": metadata,
                "steps": metadata.get("steps", []),
                "result": metadata.get("result"),
                "error": job_data.get("error")
            }

        except Exception as e:
            logger.error(f"Failed to get job status for {job_id}: {str(e)}")
            return None

    def get_job_by_symbol(self, symbol: str) -> Optional[str]:
        """
        Get the most recent job ID for a symbol.

        Args:
            symbol: Stock symbol

        Returns:
            Job ID or None if not found
        """
        try:
            response = self.client.table("research_jobs")\
                .select("id")\
                .eq("symbol", symbol.upper())\
                .order("created_at", desc=True)\
                .limit(1)\
                .execute()

            if response.data and len(response.data) > 0:
                return str(response.data[0]["id"])
            return None

        except Exception as e:
            logger.error(f"Failed to get job by symbol {symbol}: {str(e)}")
            return None

    def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a job.

        Args:
            job_id: Job ID

        Returns:
            True if successful, False otherwise
        """
        return self.update_job_status(job_id, JobStatus.CANCELLED)

    def list_jobs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """
        List recent jobs.

        Args:
            limit: Maximum number of jobs to return

        Returns:
            List of job data dicts
        """
        try:
            response = self.client.table("research_jobs")\
                .select("*")\
                .order("created_at", desc=True)\
                .limit(limit)\
                .execute()

            jobs = []
            for job_data in response.data:
                metadata = job_data.get("metadata", {})
                jobs.append({
                    "job_id": str(job_data["id"]),
                    "job_type": metadata.get("job_type", "research"),
                    "symbol": job_data["symbol"],
                    "status": job_data["status"],
                    "created_at": job_data["created_at"],
                    "updated_at": job_data["updated_at"],
                    "completed_at": job_data.get("completed_at"),
                    "failed_at": job_data.get("failed_at"),
                    "metadata": metadata,
                    "steps": metadata.get("steps", []),
                    "result": metadata.get("result"),
                    "error": job_data.get("error")
                })

            return jobs

        except Exception as e:
            logger.error(f"Failed to list jobs: {str(e)}")
            return []

# Global job tracker instance
_job_tracker_instance = None

def get_job_tracker() -> JobTracker:
    """Get or create global job tracker instance."""
    global _job_tracker_instance
    if _job_tracker_instance is None:
        _job_tracker_instance = JobTracker()
    return _job_tracker_instance

def close_job_tracker():
    """Close global job tracker connection."""
    global _job_tracker_instance
    if _job_tracker_instance:
        _job_tracker_instance.close()
        _job_tracker_instance = None
