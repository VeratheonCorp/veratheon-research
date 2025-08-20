"""Pydantic models for management guidance analysis."""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class ManagementGuidanceData(BaseModel):
    """Raw data needed for management guidance analysis."""
    
    symbol: str = Field(description="Stock symbol")
    earnings_estimates: Dict[str, Any] = Field(description="Earnings estimates data from Alpha Vantage")
    earnings_transcript: Optional[Dict[str, Any]] = Field(default=None, description="Latest earnings call transcript")
    quarter: Optional[str] = Field(default=None, description="Quarter for the transcript (YYYYQM format)")


class GuidanceIndicator(BaseModel):
    """Individual guidance indicator found in earnings call."""
    
    type: str = Field(description="Type of guidance (revenue, eps, margin, etc.)")
    direction: str = Field(description="Direction: positive, negative, neutral")
    confidence: str = Field(description="Confidence level: high, medium, low")
    context: str = Field(description="Context or quote from transcript")
    impact_assessment: str = Field(description="Assessment of potential impact on earnings")


class ManagementGuidanceAnalysis(BaseModel):
    """Results of management guidance analysis."""
    
    symbol: str = Field(description="Stock symbol")
    quarter_analyzed: Optional[str] = Field(description="Quarter of the transcript analyzed")
    transcript_available: bool = Field(description="Whether transcript was available for analysis")
    
    # Core guidance indicators
    guidance_indicators: List[GuidanceIndicator] = Field(default_factory=list, description="Specific guidance indicators found")
    
    # Overall assessment
    overall_guidance_tone: str = Field(description="Overall tone: optimistic, cautious, neutral")
    risk_factors_mentioned: List[str] = Field(default_factory=list, description="Key risk factors mentioned by management")
    opportunities_mentioned: List[str] = Field(default_factory=list, description="Key opportunities mentioned by management")
    
    # Forward-looking indicators
    revenue_guidance_direction: Optional[str] = Field(default=None, description="Revenue guidance direction if mentioned")
    margin_guidance_direction: Optional[str] = Field(default=None, description="Margin guidance direction if mentioned")
    eps_guidance_direction: Optional[str] = Field(default=None, description="EPS guidance direction if mentioned")
    
    # Confidence and validation
    guidance_confidence: str = Field(description="Overall confidence in guidance signals: high, medium, low")
    consensus_validation_signal: str = Field(description="Signal for consensus validation: bullish, bearish, neutral")
    key_guidance_summary: str = Field(description="Summary of key guidance points for next quarter")
    
    # Metadata
    analysis_notes: str = Field(description="Additional analysis notes and context")