from typing import List, Dict, Any
from pydantic import BaseModel
import enum

class ForwardPEEarningsSummary(BaseModel):
    symbol: str
    overview: Dict[str, Any]
    current_price: str
    quarterly_earnings: List
    next_quarter_consensus_eps: str

class ForwardPeValuation(BaseModel):
    analysis: str
    analysis_confidence_score: int

class ForwardPeSanityCheckRealistic(str, enum.Enum):
    REALISTIC = "REALISTIC"
    PLAUSIBLE = "PLAUSIBLE"
    NOT_REALISTIC = "NOT_REALISTIC"

class ForwardPeSanityCheck(BaseModel):
    analysis: str
    realistic: ForwardPeSanityCheckRealistic