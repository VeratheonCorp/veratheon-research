from typing import List
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