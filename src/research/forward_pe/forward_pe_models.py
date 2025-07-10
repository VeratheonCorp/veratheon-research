from typing import List, Dict, Any
from pydantic import BaseModel

class RawEarnings(BaseModel):
    symbol: str
    annual_earnings: List
    quarterly_earnings: List

class RawEarningsCalendar(BaseModel):
    symbol: str
    earnings_calendar: List

class RawGlobalQuote(BaseModel):
    symbol: str
    open: str
    high: str
    low: str
    price: str
    volume: str
    latest_trading_day: str
    previous_close: str
    change: str
    change_percent: str


class EarningsSummary(BaseModel):
    symbol: str
    overview: Dict[str, Any]
    current_price: str
    quarterly_earnings: List
    next_quarter_consensus_eps: str

class ForwardPeValuation(BaseModel):
    analysis: str
    analysis_confidence_score: int

class PeerGroup(BaseModel):
    original_symbol: str
    peer_group: List[str]
    errors: List[str]