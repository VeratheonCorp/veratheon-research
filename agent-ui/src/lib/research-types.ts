// TypeScript interfaces matching Python Pydantic models

export enum EarningsPattern {
  CONSISTENT_BEATS = "CONSISTENT_BEATS",
  CONSISTENT_MISSES = "CONSISTENT_MISSES", 
  MIXED_PATTERN = "MIXED_PATTERN",
  VOLATILE = "VOLATILE",
  INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
}

export enum RevenueGrowthTrend {
  ACCELERATING = "ACCELERATING",
  DECELERATING = "DECELERATING",
  STABLE = "STABLE",
  DECLINING = "DECLINING",
  VOLATILE = "VOLATILE",
  INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
}

export enum MarginTrend {
  IMPROVING = "IMPROVING",
  DETERIORATING = "DETERIORATING",
  STABLE = "STABLE",
  VOLATILE = "VOLATILE",
  INSUFFICIENT_DATA = "INSUFFICIENT_DATA"
}

export interface HistoricalEarningsAnalysis {
  symbol: string;
  earnings_pattern: EarningsPattern;
  earnings_pattern_details: string;
  revenue_growth_trend: RevenueGrowthTrend;
  revenue_growth_details: string;
  margin_trend: MarginTrend;
  margin_trend_details: string;
  key_insights: string[];
  long_form_analysis: string;
  critical_insights: string;
}

export interface ResearchResult {
  comprehensive_analysis: string;
  symbol: string;
  company_name?: string;
  report_date: string;
  critical_insights: string;
}