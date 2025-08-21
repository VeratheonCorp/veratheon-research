"""
Prefect task for emitting research events.
"""

from prefect import task
from typing import Any, Optional
from src.lib.events import emit_research_event

@task(name="emit-research-event")
def emit_event_task(symbol: str, event_type: str, stage: Optional[str] = None, 
                   message: Optional[str] = None, data: Optional[Any] = None):
    """
    Prefect task to emit research events for WebSocket broadcasting.
    
    This task is designed to never fail - if event emission fails, it logs a warning
    but does not interrupt the research flow.
    
    Args:
        symbol: Stock symbol
        event_type: Type of event (stage_start, stage_complete, research_started, etc.)
        stage: Research stage name (optional)
        message: Human-readable message (optional)
        data: Additional data payload (optional)
    """
    try:
        emit_research_event(symbol, event_type, stage, message, data)
    except Exception as e:
        # Event emission should never crash the research flow
        print(f"Warning: Event emission failed for {symbol} {event_type}: {e}")
        print("Research will continue normally - only WebSocket updates are affected")