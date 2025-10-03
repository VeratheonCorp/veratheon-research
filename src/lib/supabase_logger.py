"""Centralized logging to Supabase system_logs table."""
import logging
import traceback
from typing import Optional, Dict, Any
from src.lib.supabase_client import get_supabase_client

logger = logging.getLogger(__name__)

class SupabaseLogger:
    """Centralized error tracking and logging to Supabase."""

    def __init__(self):
        """Initialize Supabase logger."""
        self._client = None

    @property
    def client(self):
        """Get Supabase client connection."""
        if self._client is None:
            self._client = get_supabase_client()
        return self._client

    def log(
        self,
        log_level: str,
        component: str,
        message: str,
        job_id: Optional[str] = None,
        symbol: Optional[str] = None,
        stack_trace: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Log a message to Supabase system_logs table.

        Args:
            log_level: Log level ('error', 'warning', 'info', 'debug')
            component: Component name (e.g., 'job_tracker', 'supabase_cache', 'historical_earnings_flow')
            message: Log message
            job_id: Optional job ID
            symbol: Optional stock symbol
            stack_trace: Optional stack trace (for errors)
            metadata: Optional additional metadata

        Returns:
            True if successful, False otherwise
        """
        try:
            log_entry = {
                "log_level": log_level,
                "component": component,
                "message": message,
                "job_id": str(job_id) if job_id else None,
                "symbol": symbol.upper() if symbol else None,
                "stack_trace": stack_trace,
                "metadata": metadata or {}
            }

            self.client.table("system_logs").insert(log_entry).execute()
            return True

        except Exception as e:
            # Fall back to standard logging if Supabase fails
            logger.error(f"Failed to log to Supabase: {str(e)}")
            logger.error(f"Original log: {log_level} - {component} - {message}")
            return False

    def error(
        self,
        component: str,
        message: str,
        job_id: Optional[str] = None,
        symbol: Optional[str] = None,
        exception: Optional[Exception] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Log an error to Supabase.

        Args:
            component: Component name
            message: Error message
            job_id: Optional job ID
            symbol: Optional stock symbol
            exception: Optional exception object (stack trace will be extracted)
            metadata: Optional additional metadata

        Returns:
            True if successful, False otherwise
        """
        stack_trace = None
        if exception:
            stack_trace = "".join(traceback.format_exception(type(exception), exception, exception.__traceback__))

        return self.log(
            log_level="error",
            component=component,
            message=message,
            job_id=job_id,
            symbol=symbol,
            stack_trace=stack_trace,
            metadata=metadata
        )

    def warning(
        self,
        component: str,
        message: str,
        job_id: Optional[str] = None,
        symbol: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Log a warning to Supabase."""
        return self.log(
            log_level="warning",
            component=component,
            message=message,
            job_id=job_id,
            symbol=symbol,
            metadata=metadata
        )

    def info(
        self,
        component: str,
        message: str,
        job_id: Optional[str] = None,
        symbol: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Log an info message to Supabase."""
        return self.log(
            log_level="info",
            component=component,
            message=message,
            job_id=job_id,
            symbol=symbol,
            metadata=metadata
        )

    def debug(
        self,
        component: str,
        message: str,
        job_id: Optional[str] = None,
        symbol: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """Log a debug message to Supabase."""
        return self.log(
            log_level="debug",
            component=component,
            message=message,
            job_id=job_id,
            symbol=symbol,
            metadata=metadata
        )

# Global logger instance
_logger_instance = None

def get_supabase_logger() -> SupabaseLogger:
    """Get or create global Supabase logger instance."""
    global _logger_instance
    if _logger_instance is None:
        _logger_instance = SupabaseLogger()
    return _logger_instance

def log_error(component: str, message: str, **kwargs):
    """Convenience function to log an error."""
    get_supabase_logger().error(component, message, **kwargs)

def log_warning(component: str, message: str, **kwargs):
    """Convenience function to log a warning."""
    get_supabase_logger().warning(component, message, **kwargs)

def log_info(component: str, message: str, **kwargs):
    """Convenience function to log an info message."""
    get_supabase_logger().info(component, message, **kwargs)

def log_debug(component: str, message: str, **kwargs):
    """Convenience function to log a debug message."""
    get_supabase_logger().debug(component, message, **kwargs)
