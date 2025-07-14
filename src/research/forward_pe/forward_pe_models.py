from typing import List, Dict, Any
from pydantic import BaseModel

class ForwardPEEarningsSummary(BaseModel):
    symbol: str
    overview: Dict[str, Any]
    current_price: str
    quarterly_earnings: List
    next_quarter_consensus_eps: str

class ForwardPeValuation(BaseModel):
    analysis: str
    analysis_confidence_score: int

