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
  symbol: string;
  historical_earnings_analysis: HistoricalEarningsAnalysis;
  financial_statements_analysis: any; // TODO: Add proper typing
  earnings_projections_analysis: any; // TODO: Add proper typing
  management_guidance_analysis: any; // TODO: Add proper typing
  peer_group: any; // TODO: Add proper typing
  forward_pe_sanity_check: any; // TODO: Add proper typing
  forward_pe_valuation: any; // TODO: Add proper typing
  news_sentiment_summary: any; // TODO: Add proper typing
  trade_idea: any; // TODO: Add proper typing
}