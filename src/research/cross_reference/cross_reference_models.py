
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum

class Flows(str, Enum):
    HISTORICAL_EARNINGS = "historical_earnings"
    FINANCIAL_STATEMENTS = "financial_statements"
    EARNINGS_PROJECTIONS = "earnings_projections"
    MANAGEMENT_GUIDANCE = "management_guidance"
    FORWARD_PE = "forward_pe"
    NEWS_SENTIMENT = "news_sentiment"

class MajorAdjustment(BaseModel):
    impetus_flow: List[Flows]
    adjustment_analysis: str
    adjustment_reasoning: str

class MinorAdjustment(BaseModel):
    impetus_flow: List[Flows]
    adjustment_analysis: str
    adjustment_reasoning: str

class CrossReferencedAnalysis(BaseModel):
    major_adjustments: Optional[List[MajorAdjustment]]
    minor_adjustments: Optional[List[MinorAdjustment]]

class CrossReferencedAnalysisSummary(BaseModel):
    flow: Flows
    analysis: CrossReferencedAnalysis