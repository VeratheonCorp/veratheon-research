import uuid
import redis
import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from enum import Enum

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
    """Redis-based job tracking system using UUIDs."""
    
    def __init__(self, redis_url: Optional[str] = None):
        """
        Initialize job tracker.
        
        Args:
            redis_url: Redis connection URL (defaults to REDIS_URL env var)
        """
        self.redis_url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379/0")
        self._client = None
    
    @property
    def client(self) -> redis.Redis:
        """Get or create Redis client connection."""
        if self._client is None:
            self._client = redis.from_url(self.redis_url, decode_responses=True)
        return self._client
    
    def close(self):
        """Close Redis connection."""
        if self._client:
            self._client.close()
            self._client = None
    
    def create_job(self, job_type: str, symbol: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Create a new job and return its UUID.
        
        Args:
            job_type: Type of job (e.g., 'research')
            symbol: Stock symbol being analyzed
            metadata: Optional additional metadata
        
        Returns:
            Job UUID string
        """
        job_id = str(uuid.uuid4())
        
        job_data = {
            "job_id": job_id,
            "job_type": job_type,
            "symbol": symbol.upper(),
            "status": JobStatus.PENDING,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "metadata": metadata or {},
            "steps": [],
            "result": None,
            "error": None
        }
        
        try:
            key = f"job:{job_id}"
            self.client.setex(key, 86400, json.dumps(job_data))  # 24 hour TTL
            
            # Also store by symbol for lookup
            symbol_key = f"job_by_symbol:{symbol.upper()}"
            self.client.setex(symbol_key, 86400, job_id)
            
            logger.info(f"Created job {job_id} for {job_type} of {symbol}")
            return job_id
            
        except Exception as e:
            logger.error(f"Failed to create job: {str(e)}")
            raise
    
    def update_job_status(self, job_id: str, status: JobStatus, step: Optional[str] = None, 
                         result: Optional[Dict[str, Any]] = None, error: Optional[str] = None) -> bool:
        """
        Update job status and add step information.
        
        Args:
            job_id: Job UUID
            status: New job status
            step: Optional step description
            result: Optional result data (for completed jobs)
            error: Optional error message (for failed jobs)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            key = f"job:{job_id}"
            job_data_str = self.client.get(key)
            
            if not job_data_str:
                logger.error(f"Job {job_id} not found")
                return False
            
            job_data = json.loads(job_data_str)
            
            # Update basic status info
            job_data["status"] = status
            job_data["updated_at"] = datetime.now().isoformat()
            
            # Add step if provided
            if step:
                step_data = {
                    "step": step,
                    "timestamp": datetime.now().isoformat(),
                    "status": status
                }
                job_data["steps"].append(step_data)
            
            # Set result for completed jobs
            if result and status == JobStatus.COMPLETED:
                job_data["result"] = result
                job_data["completed_at"] = datetime.now().isoformat()
            
            # Set error for failed jobs
            if error and status == JobStatus.FAILED:
                job_data["error"] = error
                job_data["failed_at"] = datetime.now().isoformat()
            
            # Save back to Redis
            self.client.setex(key, 86400, json.dumps(job_data))
            
            logger.info(f"Updated job {job_id} status to {status}" + (f" with step: {step}" if step else ""))
            return True
            
        except Exception as e:
            logger.error(f"Failed to update job {job_id}: {str(e)}")
            return False
    
    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """
        Get job status and information.
        
        Args:
            job_id: Job UUID
        
        Returns:
            Job data dict or None if not found
        """
        try:
            key = f"job:{job_id}"
            job_data_str = self.client.get(key)
            
            if not job_data_str:
                return None
            
            return json.loads(job_data_str)
            
        except Exception as e:
            logger.error(f"Failed to get job status for {job_id}: {str(e)}")
            return None
    
    def get_job_by_symbol(self, symbol: str) -> Optional[str]:
        """
        Get the most recent job ID for a symbol.
        
        Args:
            symbol: Stock symbol
        
        Returns:
            Job UUID or None if not found
        """
        try:
            symbol_key = f"job_by_symbol:{symbol.upper()}"
            job_id = self.client.get(symbol_key)
            return job_id
            
        except Exception as e:
            logger.error(f"Failed to get job by symbol {symbol}: {str(e)}")
            return None
    
    def cancel_job(self, job_id: str) -> bool:
        """
        Cancel a job.
        
        Args:
            job_id: Job UUID
        
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
            pattern = "job:*"
            keys = self.client.keys(pattern)
            
            jobs = []
            for key in keys[:limit]:
                if key.startswith("job:") and len(key.split(":")) == 2:  # Avoid job_by_symbol keys
                    job_data_str = self.client.get(key)
                    if job_data_str:
                        jobs.append(json.loads(job_data_str))
            
            # Sort by creation time (newest first)
            jobs.sort(key=lambda x: x.get("created_at", ""), reverse=True)
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