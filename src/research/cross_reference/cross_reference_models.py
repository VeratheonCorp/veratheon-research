
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum
from src.research.forward_pe.forward_pe_models import ForwardPeValuation
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary
from src.research.historical_earnings.historical_earnings_models import HistoricalEarningsAnalysis
from src.research.financial_statements.financial_statements_models import FinancialStatementsAnalysis
from src.research.earnings_projections.earnings_projections_models import EarningsProjectionAnalysis
from src.research.management_guidance.management_guidance_models import ManagementGuidanceAnalysis
from src.research.eps_validation.eps_validation_models import (
    BottomUpEpsValidation, PeerRelativeEpsValidation, MarketSentimentEpsCheck, EpsValidationSynthesis
)

class Flows(str, Enum):
    HISTORICAL_EARNINGS = "historical_earnings"
    FINANCIAL_STATEMENTS = "financial_statements"
    EARNINGS_PROJECTIONS = "earnings_projections"
    MANAGEMENT_GUIDANCE = "management_guidance"
    FORWARD_PE = "forward_pe"
    NEWS_SENTIMENT = "news_sentiment"
    # EPS Validation flows
    BOTTOM_UP_EPS_VALIDATION = "bottom_up_eps_validation"
    PEER_RELATIVE_EPS_VALIDATION = "peer_relative_eps_validation"
    MARKET_SENTIMENT_EPS_CHECK = "market_sentiment_eps_check"
    EPS_VALIDATION_SYNTHESIS = "eps_validation_synthesis"

class MajorAdjustment(BaseModel):
    analysis_types_causing_discrepancy: List[Flows]
    adjustment_analysis: str
    adjustment_reasoning: str

class MinorAdjustment(BaseModel):
    analysis_types_causing_discrepancy: List[Flows]
    adjustment_analysis: str
    adjustment_reasoning: str

class CrossReferencedAnalysis(BaseModel):
    major_adjustments: Optional[List[MajorAdjustment]]
    minor_adjustments: Optional[List[MinorAdjustment]]

class CrossReferencedAnalysisCompletion(BaseModel):
    original_analysis_type: Flows
    cross_referenced_analysis: CrossReferencedAnalysis
