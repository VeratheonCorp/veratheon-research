// TypeScript interfaces matching Python Pydantic models

export interface ComprehensiveReport {
  comprehensive_analysis: string;
  symbol: string;
  company_name?: string;
  report_date: string;
  critical_insights: string;
}

export interface ResearchResult {
  symbol: string;
  comprehensive_report: ComprehensiveReport;
}