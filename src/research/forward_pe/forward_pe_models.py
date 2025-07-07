from typing import List
from enum import Enum, auto
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
    closing_price: str
    annual_earnings: List
    quarterly_earnings: List
    next_quarter_consensus_eps: str


class ValuationBucket(Enum):
    """
    How the P/E stacks up vs. peers and history.
    Thresholds can be, for example, ±1σ or ±X% relative to both peer & historical means.
    """

    VERY_CHEAP = auto()  # well below both peer & historical average
    CHEAP = auto()  # below peer OR historical average
    FAIR_VALUE = auto()  # roughly in line with both averages
    EXPENSIVE = auto()  # above peer OR historical average
    VERY_EXPENSIVE = auto()  # well above both averages

class ForwardPeValuation(BaseModel):
    valuation_bucket: ValuationBucket
    analysis: str
    advice: str

class PeerGroup(BaseModel):
    original_symbol: str
    peer_group: List[str]
    errors: List[str]