# server/api.py
import sys
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import time

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
import asyncio

# Ensure project root is on the Python path (so imports like src.flows... work)
project_root = Path(__file__).resolve().parents[1]
if str(project_root) not in sys.path:
    sys.path.append(str(project_root))

# Load environment variables
load_dotenv()

# Import after sys.path setup
from src.flows.research_flow import main_research_flow  # noqa: E402

logging.basicConfig(level=logging.INFO)
logging.getLogger("LiteLLM").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

app = FastAPI(title="Market Research Agent API", version="0.1.0")

# Simple in-memory tracking for research status
research_status: Dict[str, Dict[str, Any]] = {}

class ResearchRequest(BaseModel):
    symbol: str = "PG"
    force_recompute: bool = False


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/research")
async def run_research(req: ResearchRequest, request: Request):
    try:
        symbol_upper = req.symbol.upper()
        logger.info(f"Starting market research via API for symbol={symbol_upper}")
        
        # Track research start
        research_status[symbol_upper] = {
            "started_at": time.time(),
            "completed": False,
            "result": None,
            "error": None
        }
        
        # Check if client disconnected
        if await request.is_disconnected():
            logger.warning("Client disconnected before starting research")
            research_status[symbol_upper]["error"] = "Client disconnected"
            raise HTTPException(status_code=408, detail="Client disconnected")
        
        # Run the research flow with periodic disconnect checks
        result = await main_research_flow(symbol=req.symbol, force_recompute=req.force_recompute)
        
        # Final disconnect check before returning
        if await request.is_disconnected():
            logger.warning("Client disconnected during research")
            research_status[symbol_upper]["error"] = "Client disconnected"
            raise HTTPException(status_code=408, detail="Client disconnected")
        
        # Mark as completed
        research_status[symbol_upper].update({
            "completed": True,
            "result": result,
            "completed_at": time.time()
        })
            
        # result is now already a dict with all analysis models
        return result
    except asyncio.CancelledError:
        logger.warning("Research request was cancelled")
        research_status.get(req.symbol.upper(), {})["error"] = "Request cancelled"
        raise HTTPException(status_code=408, detail="Request cancelled")
    except Exception as e:
        logger.exception("Error running market research")
        research_status.get(req.symbol.upper(), {})["error"] = str(e)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/research/status/{symbol}")
async def get_research_status(symbol: str):
    """Get the status of research for a given symbol"""
    symbol_upper = symbol.upper()
    
    if symbol_upper not in research_status:
        raise HTTPException(status_code=404, detail=f"No research found for symbol {symbol_upper}")
    
    status = research_status[symbol_upper]
    
    return {
        "symbol": symbol_upper,
        "completed": status.get("completed", False),
        "started_at": status.get("started_at"),
        "completed_at": status.get("completed_at"),
        "result": status.get("result"),
        "error": status.get("error")
    }