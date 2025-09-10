// TypeScript interfaces matching Python Pydantic models

export interface ComprehensiveReport {
  symbol: string;
  company_name?: string;
  report_date: string;
  comprehensive_analysis: string;
  critical_insights: string;
}

export interface ResearchResult {
  symbol: string;
  comprehensive_report: ComprehensiveReport;
}