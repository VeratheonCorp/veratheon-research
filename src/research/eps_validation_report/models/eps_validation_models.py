from typing import List, Optional
from pydantic import BaseModel
import enum


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


class ConsensusEpsContext(BaseModel):
    symbol: str
    consensus_eps: float
    analyst_count: int
    revision_momentum: RevisionMomentum
    eps_estimate_high: Optional[float] = None
    eps_estimate_low: Optional[float] = None
    revision_up_7_days: Optional[int] = None
    revision_down_7_days: Optional[int] = None
    revision_up_30_days: Optional[int] = None
    revision_down_30_days: Optional[int] = None


class HistoricalEpsPattern(BaseModel):
    symbol: str
    growth_trend: str
    volatility_level: str
    seasonal_patterns: str
    quality_metrics: str
    average_growth_rate: Optional[float] = None
    earnings_consistency_score: Optional[float] = None
    beat_miss_ratio: Optional[float] = None


class BottomUpEpsValidation(BaseModel):
    symbol: str
    independent_estimate: float
    variance_from_consensus: float
    variance_percentage: float
    methodology_summary: str
    confidence_level: str
    key_assumptions: List[str]


class PeerRelativeEpsValidation(BaseModel):
    symbol: str
    peer_symbols: List[str]
    relative_growth_expectation: str
    industry_context: str
    peer_comparison_summary: str
    relative_valuation_metrics: str
    industry_growth_rate: Optional[float] = None


class MarketSentimentEpsCheck(BaseModel):
    symbol: str
    sentiment_earnings_alignment: str
    revision_momentum_analysis: str
    guidance_consistency: str
    market_expectation_summary: str
    sentiment_score: Optional[float] = None
    alignment_confidence: str


class EpsValidationSynthesis(BaseModel):
    symbol: str
    validation_verdict: EpsValidationVerdict
    key_risks: List[str]
    supporting_evidence: List[str]
    conflicting_signals: List[str]
    confidence_level: str
    synthesis_summary: str


class InvestmentImplications(BaseModel):
    symbol: str
    price_target_range: str
    risk_reward_analysis: str
    position_sizing_guidance: str
    time_horizon: str
    key_catalysts: List[str]
    risk_factors: List[str]


class SpeculativeAnalysis(BaseModel):
    symbol: str
    upside_scenarios: List[str]
    black_swan_risks: List[str]
    catalyst_speculation: List[str]
    extreme_case_outcomes: str
    probability_assessments: str


class EpsValidationReport(BaseModel):
    symbol: str
    validation_verdict: EpsValidationVerdict
    consensus_eps_context: ConsensusEpsContext
    historical_eps_pattern: HistoricalEpsPattern
    bottom_up_validation: BottomUpEpsValidation
    peer_relative_validation: PeerRelativeEpsValidation
    market_sentiment_check: MarketSentimentEpsCheck
    validation_synthesis: EpsValidationSynthesis
    investment_implications: InvestmentImplications
    speculative_analysis: SpeculativeAnalysis
    investment_thesis: str
    action_items: List[str]
    report_timestamp: str