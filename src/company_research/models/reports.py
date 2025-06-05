from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class EconomicCycle(str, Enum):
    EXPANSION = "expansion"
    PEAK = "peak"
    DOWNTURN = "downturn"
    RECOVERY = "recovery"

class IndustryLifeCycle(str, Enum):
    GROWTH = "growth"
    MATURITY = "maturity"
    DECLINE = "decline"

class ScenarioType(str, Enum):
    BEST_CASE = "best_case"
    BASE_CASE = "base_case"
    WORST_CASE = "worst_case"

class ParametersReport(BaseModel):
    """Report for clarifying analysis parameters"""
    ticker: str
    current_price: float = Field(..., description="Current market price (P₀)")
    target_price: float = Field(..., description="Proposed target price (Pₜ)")
    time_horizon_years: float = Field(..., description="Analysis horizon in years")
    upside_downside_pct: float = Field(..., description="Implied upside/downside percentage")
    conservative_aggressive: str = Field(default="balanced", description="Forecast approach")
    include_dividends: bool = Field(default=True)
    expected_share_count_change: Optional[float] = Field(None, description="Expected change in share count")

class MacroEconomicReport(BaseModel):
    """Report for macro context analysis"""
    economic_cycle: EconomicCycle
    economic_outlook: str
    interest_rate_forecast: Dict[str, str]
    inflation_forecast: Dict[str, str]
    unemployment_forecast: Dict[str, str]
    unemployment_outlook: str
    reasoning_summary: str = Field(..., description="Summary of macro and industry analysis")

class FundamentalAnalysisReport(BaseModel):
    """Report for fundamental analysis"""
    historical_financials: Dict[str, List[float]]  # 3-5 years of key metrics
    revenue_growth_drivers: List[str]
    growth_sustainability_analysis: str
    historical_margins: Dict[str, float]
    forecasted_margins: Dict[str, float]
    roic_vs_wacc: Dict[str, float]
    working_capital_trends: Dict[str, float]
    leverage_ratios: Dict[str, float]
    liquidity_metrics: Dict[str, float]
    covenant_analysis: Optional[str]

class DCFValuationReport(BaseModel):
    """Report for DCF valuation model"""
    forecasted_fcf: List[float]  # 5-10 year forecast
    terminal_value_method: str
    terminal_growth_rate: float
    wacc: float
    risk_free_rate: float
    equity_risk_premium: float
    beta: float
    cost_of_debt: float
    enterprise_value: float
    equity_value: float
    intrinsic_price_per_share: float

class MultiplesValuationReport(BaseModel):
    """Report for relative valuation using multiples"""
    peer_companies: List[str]
    current_multiples: Dict[str, float]  # P/E, EV/EBITDA, P/S, P/FCF
    peer_multiples: Dict[str, List[float]]
    projected_multiples: Dict[str, float]
    implied_prices: Dict[str, float]  # Price from each multiple

class ValuationReport(BaseModel):
    """Comprehensive valuation report"""
    dcf_valuation: DCFValuationReport
    multiples_valuation: MultiplesValuationReport
    sum_of_parts: Optional[Dict[str, float]]
    weighted_average_price: float

class ScenarioAnalysisReport(BaseModel):
    """Report for scenario and sensitivity analysis"""
    scenarios: Dict[ScenarioType, Dict[str, Any]]
    scenario_probabilities: Dict[ScenarioType, float]
    sensitivity_analysis: Dict[str, Dict[str, float]]  # Variable -> sensitivity results
    weighted_average_target: float
    confidence_intervals: Dict[str, float]

class QualitativeReport(BaseModel):
    """Report for qualitative factors and catalysts"""
    management_quality_score: float = Field(..., ge=1, le=10)
    governance_assessment: str
    capital_allocation_track_record: str
    competitive_moat_strength: str = Field(..., description="Network effects, patents, brands, etc.")
    upcoming_catalysts: List[str]
    execution_risks: List[str]
    regulatory_risks: List[str]
    industry_lifecycle: IndustryLifeCycle
    technological_disruption_risks: List[str]
    financial_covenant_risks: List[str]
    competitive_intensity: str
    porter_five_forces: Dict[str, str]

class TechnicalMarketSentimentReport(BaseModel):
    """Report for technical analysis and market sentiment"""
    price_trend_analysis: str
    moving_averages: Dict[str, float]
    volume_trends: str
    analyst_consensus: Dict[str, Any]
    price_target_distribution: List[float]
    options_positioning: Dict[str, float]
    insider_transactions: List[Dict[str, Any]]
    institutional_ownership_changes: Optional[float]

class BenchmarkReviewReport(BaseModel):
    """Report for benchmarking and review"""
    historical_accuracy_metrics: Dict[str, float]
    peer_review_feedback: List[str]
    methodology_validation: str
    assumption_stress_tests: Dict[str, Any]

class FinalSynthesisReport(BaseModel):
    """Final synthesis and recommendation report"""
    implied_annualized_return: float
    benchmark_comparison: Dict[str, float]  # vs index, bonds, etc.
    margin_of_safety: float
    confidence_level: str
    investment_thesis_summary: str
    key_assumptions: List[str]
    primary_risks: List[str]
    recommendation: str  # Buy/Hold/Sell
    target_price_justification: str

class MonitoringReport(BaseModel):
    """Report for ongoing monitoring setup"""
    key_triggers: List[str]
    monitoring_schedule: str
    performance_metrics: List[str]
    review_checkpoints: List[datetime]

class ComprehensiveEquityResearchReport(BaseModel):
    """Master report containing all analysis components"""
    report_id: str = Field(default_factory=lambda: f"research_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    created_at: datetime = Field(default_factory=datetime.now)
    analyst_name: Optional[str] = None
    
    # Core report sections
    parameters: ParametersReport
    macro_industry: MacroEconomicReport
    fundamental_analysis: FundamentalAnalysisReport
    valuation: ValuationReport
    scenario_analysis: ScenarioAnalysisReport
    qualitative: QualitativeReport
    technical_sentiment: TechnicalMarketSentimentReport
    benchmark_review: BenchmarkReviewReport
    final_synthesis: FinalSynthesisReport
    monitoring: MonitoringReport
    
    # Metadata
    last_updated: datetime = Field(default_factory=datetime.now)
    version: str = Field(default="1.0")
    notes: Optional[str] = None

    def update_timestamp(self):
        """Update the last_updated timestamp"""
        self.last_updated = datetime.now()
    
    def get_price_differential_analysis(self) -> Dict[str, Any]:
        """Analyze price differential as per main strategy"""
        current = self.parameters.current_price
        target = self.parameters.target_price
        
        differential_pct = ((target - current) / current) * 100
        differential_abs = abs(differential_pct)
        
        return {
            "price_differential_pct": differential_pct,
            "price_differential_abs": differential_abs,
            "is_high_differential": differential_abs >= 20.0,
            "requires_historical_analysis": differential_abs >= 20.0,
            "direction": "upside" if differential_pct > 0 else "downside"
        }
