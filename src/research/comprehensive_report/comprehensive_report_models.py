from typing import Optional
from pydantic import BaseModel


class ComprehensiveReport(BaseModel):
    symbol: str
    company_name: Optional[str] = None
    report_date: str
    
    # The main comprehensive report as a single readable text block
    comprehensive_analysis: str
    
    # Critical insights for cross-model calibration
    critical_insights: str