from pydantic import BaseModel

class HasPositionTradeIdea(BaseModel):
    high_level_trade_idea: str
    simple_equity_trade_specifics: str
    option_play: str
    simple_equity_trade_specifics_confidence_score: int
    option_play_confidence_score: int
    risk_hedge: str
    reasoning: str

class NoPositionTradeIdea(BaseModel):
    high_level_trade_idea: str
    simple_equity_trade_specifics: str
    option_play: str
    simple_equity_trade_specifics_confidence_score: int
    option_play_confidence_score: int
    risk_hedge: str
    reasoning: str

class TradeIdeas(BaseModel):
    no_position_trade_idea: NoPositionTradeIdea
    has_position_trade_idea: HasPositionTradeIdea
    