# server/api.py
import sys
import logging
from pathlib import Path
from typing import Optional

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


class ResearchRequest(BaseModel):
    symbol: str = "PG"
    force_recompute: bool = False


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/research")
async def run_research(req: ResearchRequest, request: Request):
    try:
        logger.info(f"Starting market research via API for symbol={req.symbol}")
        
        # Check if client disconnected
        if await request.is_disconnected():
            logger.warning("Client disconnected before starting research")
            raise HTTPException(status_code=408, detail="Client disconnected")
        
        # Run the research flow with periodic disconnect checks
        result = await main_research_flow(symbol=req.symbol, force_recompute=req.force_recompute)
        
        # Final disconnect check before returning
        if await request.is_disconnected():
            logger.warning("Client disconnected during research")
            raise HTTPException(status_code=408, detail="Client disconnected")
            
        # result is now already a dict with all analysis models
        return result
    except asyncio.CancelledError:
        logger.warning("Research request was cancelled")
        raise HTTPException(status_code=408, detail="Request cancelled")
    except Exception as e:
        logger.exception("Error running market research")
        raise HTTPException(status_code=500, detail=str(e))