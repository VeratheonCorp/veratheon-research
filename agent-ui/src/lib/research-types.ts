// TypeScript interfaces matching Python Pydantic models

export interface ComprehensiveReport {
  comprehensive_analysis: string;
  symbol: string;
  company_name?: string;
  report_date: string;
}

export interface KeyInsights {
  critical_insights: string;
  symbol: string;
  company_name?: string;
  report_date: string;
}

export interface ResearchResult {
  symbol: string;
  comprehensive_report: ComprehensiveReport;
  key_insights: KeyInsights;
}