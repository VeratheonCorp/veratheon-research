import enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


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


class BottomUpEpsValidation(BaseModel):
    symbol: str = Field(..., description="Stock symbol being validated")
    independent_eps_estimate: float = Field(
        ..., description="Bottom-up reconstructed EPS estimate"
    )
    consensus_eps: float = Field(..., description="Wall Street consensus EPS estimate")
    variance_percentage: float = Field(
        ...,
        description="Percentage difference between independent and consensus estimates",
    )
    confidence_level: ConfidenceLevel = Field(
        ..., description="Confidence in the bottom-up estimate"
    )
    key_assumptions: List[str] = Field(
        ..., description="Key assumptions used in bottom-up reconstruction"
    )
    validation_verdict: EpsValidationVerdict = Field(
        ..., description="Bottom-up validation verdict"
    )
    supporting_analysis: str = Field(
        ..., description="Detailed analysis supporting the validation verdict"
    )
    risk_factors: List[str] = Field(
        default_factory=list, description="Key risks to the bottom-up estimate"
    )


class PeerRelativeEpsValidation(BaseModel):
    symbol: str = Field(..., description="Stock symbol being validated")
    peer_group_avg_forward_pe: float = Field(
        ..., description="Average forward P/E ratio of peer group"
    )
    current_stock_price: float = Field(..., description="Current stock price")
    implied_eps_from_peers: float = Field(
        ..., description="Implied EPS using peer group forward P/E"
    )
    consensus_eps: float = Field(..., description="Wall Street consensus EPS estimate")
    relative_variance: float = Field(
        ..., description="Percentage difference between peer-implied and consensus EPS"
    )
    peer_comparison_verdict: EpsValidationVerdict = Field(
        ..., description="Peer-relative validation verdict"
    )
    peer_analysis: str = Field(
        ..., description="Analysis of company vs peer group expectations"
    )
    industry_context: str = Field(
        ..., description="Industry-specific context affecting EPS expectations"
    )


class MarketSentimentEpsCheck(BaseModel):
    symbol: str = Field(..., description="Stock symbol being validated")
    revision_momentum: RevisionMomentum = Field(
        ..., description="Recent analyst revision trends"
    )
    sentiment_eps_alignment: SentimentAlignment = Field(
        ..., description="Alignment between sentiment and EPS expectations"
    )
    whisper_vs_consensus: Optional[float] = Field(
        None, description="Whisper number vs consensus EPS difference"
    )
    sentiment_validation_verdict: EpsValidationVerdict = Field(
        ..., description="Sentiment-based validation verdict"
    )
    revision_analysis: str = Field(
        ..., description="Analysis of recent EPS revisions and trends"
    )
    sentiment_insights: List[str] = Field(
        default_factory=list,
        description="Key sentiment insights affecting EPS expectations",
    )
    market_expectation_summary: str = Field(
        ..., description="Summary of market expectations vs published consensus"
    )


# TEMPLATE: Example new validation method for demonstration
class TechnicalEpsValidation(BaseModel):
    """
    TEMPLATE: Technical analysis-based EPS validation model.

    This serves as a template for adding new validation methods.
    Replace 'Technical' with your validation method name.
    """
    symbol: str = Field(..., description="Stock symbol being validated")
    price_momentum_score: float = Field(
        ..., ge=-1.0, le=1.0, description="Price momentum score (-1 to 1)"
    )
    volume_trend_indicator: str = Field(
        ..., description="Volume trend analysis (INCREASING/DECREASING/STABLE)"
    )
    technical_consensus_eps: float = Field(
        ..., description="Consensus EPS estimate for comparison"
    )
    implied_eps_from_technicals: float = Field(
        ..., description="EPS estimate implied by technical indicators"
    )
    technical_variance_percentage: float = Field(
        ..., description="Variance between technical and consensus estimates"
    )
    validation_verdict: EpsValidationVerdict = Field(
        ..., description="Technical analysis validation verdict"
    )
    confidence_level: ConfidenceLevel = Field(
        ..., description="Confidence in technical analysis validation"
    )
    technical_indicators: List[str] = Field(
        default_factory=list, description="Key technical indicators analyzed"
    )
    support_resistance_analysis: str = Field(
        ..., description="Analysis of support/resistance levels affecting EPS expectations"
    )
    risk_factors: List[str] = Field(
        default_factory=list,
        description="Technical risk factors affecting validation reliability"
    )


class EpsValidationSynthesis(BaseModel):
    symbol: str = Field(..., description="Stock symbol being validated")
    overall_verdict: EpsValidationVerdict = Field(
        ..., description="Overall EPS validation verdict across all methods"
    )
    confidence_score: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence in overall verdict (0-1 scale)"
    )
    method_agreement: Dict[str, EpsValidationVerdict] = Field(
        ..., description="Individual verdicts from each validation method"
    )
    key_risks: List[str] = Field(..., description="Primary risks to EPS expectations")
    supporting_evidence: List[str] = Field(
        ..., description="Evidence supporting the overall verdict"
    )
    consensus_adjustment_recommendation: Optional[str] = Field(
        None, description="Recommended adjustment to consensus if applicable"
    )
    synthesis_analysis: str = Field(
        ..., description="Comprehensive analysis synthesizing all validation methods"
    )
    investment_implications: str = Field(
        ..., description="Investment implications based on EPS validation results"
    )
