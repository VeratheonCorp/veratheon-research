from prefect import task, get_run_logger
from src.research.financial_statements.financial_statements_models import FinancialStatementsData, FinancialStatementsAnalysis
from src.research.financial_statements.financial_statements_agent import financial_statements_analysis_agent
from agents import Runner, RunResult
import json


@task(name="financial_statements_analysis_task", persist_result=True)
async def financial_statements_analysis_task(
    symbol: str, 
    financial_data: FinancialStatementsData
) -> FinancialStatementsAnalysis:
    """
    Task to perform financial statements analysis for changes in revenue drivers, cost structures, and working capital.
    
    Args:
        symbol: Stock symbol to research
        financial_data: Financial statements data from Alpha Vantage
    Returns:
        FinancialStatementsAnalysis containing the analysis results and trends
    """
    logger = get_run_logger()
    logger.info(f"Performing financial statements analysis for {symbol}")

    # Prepare the input for the agent
    input_data = f"""
    symbol: {symbol}
    financial_statements_data: {financial_data.model_dump_json()}
    """

    result: RunResult = await Runner.run(
        financial_statements_analysis_agent,
        input=input_data
    )
    
    financial_analysis: FinancialStatementsAnalysis = result.final_output

    logger.info(f"Financial statements analysis completed for {symbol}: "
               f"Revenue trend: {financial_analysis.revenue_driver_trend}, "
               f"Cost trend: {financial_analysis.cost_structure_trend}, "
               f"Working capital trend: {financial_analysis.working_capital_trend}, "
               f"Confidence: {financial_analysis.analysis_confidence_score}/10")

    return financial_analysis