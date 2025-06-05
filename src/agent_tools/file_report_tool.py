import json
import os
from typing import Dict, Any, List, Optional, Union
from pathlib import Path
from datetime import datetime

from ..company_research.models.reports import (
    ComprehensiveEquityResearchReport,
    ParametersReport,
    MacroEconomicReport,
    FundamentalAnalysisReport,
    DCFValuationReport,
    MultiplesValuationReport,
    ValuationReport,
    ScenarioAnalysisReport,
    QualitativeReport,
    TechnicalMarketSentimentReport,
    BenchmarkReviewReport,
    FinalSynthesisReport,
    MonitoringReport
)

class FileReportTool:
    """Tool for OpenAI agents to file specific reports into the comprehensive report structure"""
    
    # Mapping of report types to their corresponding Pydantic models
    REPORT_TYPE_MAPPING = {
        "parameters": ParametersReport,
        "macro_industry": MacroEconomicReport,
        "fundamental_analysis": FundamentalAnalysisReport,
        "dcf_valuation": DCFValuationReport,
        "multiples_valuation": MultiplesValuationReport,
        "valuation": ValuationReport,
        "scenario_analysis": ScenarioAnalysisReport,
        "qualitative": QualitativeReport,
        "technical_sentiment": TechnicalMarketSentimentReport,
        "benchmark_review": BenchmarkReviewReport,
        "final_synthesis": FinalSynthesisReport,
        "monitoring": MonitoringReport
    }
    
    def __init__(self, reports_directory: str = "/tmp/equity_research_reports"):
        """Initialize the file report tool with a directory for storing reports"""
        self.reports_directory = Path(reports_directory)
        self.reports_directory.mkdir(parents=True, exist_ok=True)
    
    def file_report(
        self, 
        report_type: str, 
        report_data: Dict[str, Any], 
        ticker: str,
        report_id: Optional[str] = None,
        analyst_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        File a specific report into the comprehensive report structure.
        
        Args:
            report_type: Type of report (e.g., 'parameters', 'macro_industry', etc.)
            report_data: Dictionary containing the report data
            ticker: Stock ticker symbol
            report_id: Optional existing report ID to update
            analyst_name: Name of the analyst filing the report
            
        Returns:
            Dictionary with success status and report information
        """
        try:
            # Validate report type
            if report_type not in self.REPORT_TYPE_MAPPING:
                return {
                    "success": False,
                    "error": f"Invalid report type: {report_type}. Valid types: {list(self.REPORT_TYPE_MAPPING.keys())}"
                }
            
            # Load or create comprehensive report
            if report_id:
                comprehensive_report = self.load_report(report_id)
                if not comprehensive_report:
                    return {
                        "success": False,
                        "error": f"Report with ID {report_id} not found"
                    }
            else:
                # Create new comprehensive report with minimal required data
                comprehensive_report = self._create_new_comprehensive_report(ticker, analyst_name)
            
            # Validate and create the specific report
            report_model = self.REPORT_TYPE_MAPPING[report_type]
            try:
                validated_report = report_model(**report_data)
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Report data validation failed: {str(e)}"
                }
            
            # Update the comprehensive report with the new section
            setattr(comprehensive_report, report_type, validated_report)
            comprehensive_report.update_timestamp()
            
            # Save the updated report
            saved_report_id = self.save_report(comprehensive_report)
            
            return {
                "success": True,
                "report_id": saved_report_id,
                "report_type": report_type,
                "ticker": ticker,
                "message": f"Successfully filed {report_type} report for {ticker}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error filing report: {str(e)}"
            }
    
    def load_report(self, report_id: str) -> Optional[ComprehensiveEquityResearchReport]:
        """Load an existing comprehensive report by ID"""
        try:
            report_file = self.reports_directory / f"{report_id}.json"
            if not report_file.exists():
                return None
                
            with open(report_file, 'r') as f:
                report_data = json.load(f)
                
            return ComprehensiveEquityResearchReport(**report_data)
        except Exception:
            return None
    
    def save_report(self, report: ComprehensiveEquityResearchReport) -> str:
        """Save a comprehensive report to disk"""
        report_file = self.reports_directory / f"{report.report_id}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report.dict(), f, indent=2, default=str)
        
        return report.report_id
    
    def get_report_status(self, report_id: str) -> Dict[str, Any]:
        """Get the status of a comprehensive report (which sections are completed)"""
        report = self.load_report(report_id)
        if not report:
            return {"error": f"Report {report_id} not found"}
        
        status = {
            "report_id": report_id,
            "ticker": report.parameters.ticker if hasattr(report, 'parameters') else "Unknown",
            "created_at": report.created_at,
            "last_updated": report.last_updated,
            "completed_sections": [],
            "missing_sections": []
        }
        
        for section_name in self.REPORT_TYPE_MAPPING.keys():
            if hasattr(report, section_name) and getattr(report, section_name) is not None:
                status["completed_sections"].append(section_name)
            else:
                status["missing_sections"].append(section_name)
        
        status["completion_percentage"] = len(status["completed_sections"]) / len(self.REPORT_TYPE_MAPPING) * 100
        
        return status
    
    def list_reports(self) -> List[Dict[str, Any]]:
        """List all available reports with basic information"""
        reports = []
        
        for report_file in self.reports_directory.glob("*.json"):
            try:
                with open(report_file, 'r') as f:
                    report_data = json.load(f)
                
                reports.append({
                    "report_id": report_data.get("report_id"),
                    "ticker": report_data.get("parameters", {}).get("ticker", "Unknown"),
                    "created_at": report_data.get("created_at"),
                    "last_updated": report_data.get("last_updated"),
                    "analyst_name": report_data.get("analyst_name")
                })
            except Exception:
                continue
        
        return sorted(reports, key=lambda x: x["last_updated"], reverse=True)
    
    def _create_new_comprehensive_report(
        self, 
        ticker: str, 
        analyst_name: Optional[str] = None
    ) -> ComprehensiveEquityResearchReport:
        """Create a new comprehensive report with minimal required data"""
        # Create minimal parameters report to satisfy the requirement
        minimal_parameters = ParametersReport(
            ticker=ticker,
            current_price=0.0,  # Will be updated when parameters agent runs
            target_price=0.0,   # Will be updated when parameters agent runs
            time_horizon_years=1.0,
            upside_downside_pct=0.0
        )
        
        return ComprehensiveEquityResearchReport(
            parameters=minimal_parameters,
            analyst_name=analyst_name,
            # All other sections will be None initially and added by agents
            macro_industry=None,
            fundamental_analysis=None,
            valuation=None,
            scenario_analysis=None,
            qualitative=None,
            technical_sentiment=None,
            benchmark_review=None,
            final_synthesis=None,
            monitoring=None
        )

# Convenience function for OpenAI agents to use directly
def file_equity_research_report(
    report_type: str,
    report_data: Dict[str, Any],
    ticker: str,
    report_id: Optional[str] = None,
    analyst_name: Optional[str] = None,
    reports_directory: Optional[str] = None
) -> Dict[str, Any]:
    """
    Convenience function for OpenAI agents to file reports.
    
    Usage example:
    result = file_equity_research_report(
        report_type="macro_industry",
        report_data={
            "economic_cycle": "expansion",
            "economic_outlook": "Positive growth expected",
            "interest_rate_forecast": {"2024": 5.25, "2025": 4.75},
            "inflation_forecast": {"2024": 3.2, "2025": 2.8},
            "regulatory_factors": ["New EPA regulations"],
            "geopolitical_risks": ["Trade tensions"],
            "industry_lifecycle": "maturity",
            "competitive_intensity": "High",
            "porter_five_forces": {
                "buyer_power": "Medium",
                "supplier_power": "Low",
                "threat_of_substitutes": "High",
                "threat_of_new_entrants": "Low",
                "competitive_rivalry": "High"
            }
        },
        ticker="AAPL",
        analyst_name="Research Agent"
    )
    """
    tool = FileReportTool(reports_directory or "/tmp/equity_research_reports")
    return tool.file_report(report_type, report_data, ticker, report_id, analyst_name)
