import enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class EpsValidationVerdict(str, enum.Enum):
    CONSENSUS_VALIDATED = "CONSENSUS_VALIDATED"
    CONSENSUS_TOO_HIGH = "CONSENSUS_TOO_HIGH"
    CONSENSUS_TOO_LOW = "CONSENSUS_TOO_LOW"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class RevisionMomentum(str, enum.Enum):
    UPWARD = "UPWARD"
    DOWNWARD = "DOWNWARD"
    STABLE = "STABLE"
    VOLATILE = "VOLATILE"
    INSUFFICIENT_DATA = "INSUFFICIENT_DATA"


class ConfidenceLevel(str, enum.Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class SentimentAlignment(str, enum.Enum):
    BULLISH = "BULLISH"
    BEARISH = "BEARISH"
    NEUTRAL = "NEUTRAL"
    CONFLICTED = "CONFLICTED"


class PeerRelativeEpsValidation(BaseModel):
    symbol: str
    peer_group_avg_forward_pe: float
    current_stock_price: float
    peer_implied_eps_estimate: float
    consensus_eps: float
    relative_variance: float
    peer_comparison_verdict: EpsValidationVerdict
    peer_analysis: str
    industry_context: str


class MarketSentimentEpsCheck(BaseModel):
    symbol: str
    revision_momentum: RevisionMomentum
    sentiment_eps_alignment: SentimentAlignment
    whisper_vs_consensus: Optional[float] = None
    sentiment_validation_verdict: EpsValidationVerdict
    revision_analysis: str
    sentiment_insights: List[str] = []
    market_expectation_summary: str


class TechnicalEpsValidation(BaseModel):
    symbol: str
    price_momentum_score: float
    volume_trend_indicator: str
    consensus_eps: float
    technical_implied_eps_estimate: float
    technical_variance_percentage: float
    validation_verdict: EpsValidationVerdict
    confidence_level: ConfidenceLevel
    technical_indicators: List[str] = []
    support_resistance_analysis: str
    risk_factors: List[str] = []


class EpsValidationSynthesis(BaseModel):
    symbol: str
    overall_verdict: EpsValidationVerdict
    confidence_score: float
    method_agreement: Dict[str, EpsValidationVerdict]
    key_risks: List[str]
    supporting_evidence: List[str]
    consensus_adjustment_recommendation: Optional[str] = None
    synthesis_analysis: str
    investment_implications: str
