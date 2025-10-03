import logging
from typing import Optional
from src.lib.supabase_job_tracker import get_job_tracker, JobStatus

logger = logging.getLogger(__name__)

async def update_job_status_task(
    job_id: Optional[str], 
    status: JobStatus, 
    step: str,
    flow: Optional[str] = None
) -> bool:
    """
    Task to update job status in Supabase.
    
    Args:
        job_id: Job UUID (if None, this is a no-op for backward compatibility)
        status: Job status to update to
        step: Description of the current step
        flow: Optional flow name for context
    
    Returns:
        bool: True if successful, False otherwise
    """
    if not job_id:
        # For backward compatibility when job_id is not provided
        logger.debug(f"No job_id provided, skipping status update: {step}")
        return True
        
    try:
        job_tracker = get_job_tracker()
        
        # Add flow context to step if provided
        full_step = f"{flow}: {step}" if flow else step
        
        result = job_tracker.update_job_status(job_id, status, step=full_step)
        
        if result:
            logger.info(f"Updated job {job_id} status to {status}: {full_step}")
        else:
            logger.warning(f"Failed to update job {job_id} status")
            
        return result
        
    except Exception as e:
        logger.error(f"Failed to update job status for {job_id}: {str(e)}")
        return False