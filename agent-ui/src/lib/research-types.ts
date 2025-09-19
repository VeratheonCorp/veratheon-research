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

// Trade-related interfaces
export interface TradeDetails {
  symbol: string;
  instrumentType: 'stock' | 'option';
  direction: 'long' | 'short';
  optionType: 'call' | 'put' | null;
  strikePrice: number | null;
  expirationDate: string;
  isHedge: boolean;
  rationale: string;
}

export interface Trade extends TradeDetails {
  id: string;
  timestamp: string;
  status: 'pending' | 'validated' | 'invalidated';
  validationReason?: string;
}

export interface TradeResponse {
  success: boolean;
  message: string;
  trade?: Trade;
  error?: string;
}

export interface TradeValidationRequest {
  tradeId: string;
  symbol: string;
  researchData?: ResearchResult;
}