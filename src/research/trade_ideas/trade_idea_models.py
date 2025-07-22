from pydantic import BaseModel

class TradeIdea(BaseModel):
    high_level_trade_idea: str
    reasoning: str
    simple_equity_trade_specifics: str
    option_play: str
    simple_equity_trade_specifics_confidence_score: int
    option_play_confidence_score: int
    risk_hedge: str
    