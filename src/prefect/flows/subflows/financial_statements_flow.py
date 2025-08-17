from prefect import flow, get_run_logger
from src.prefect.tasks.financial_statements.financial_statements_fetch_task import financial_statements_fetch_task
from src.prefect.tasks.financial_statements.financial_statements_analysis_task import financial_statements_analysis_task
from src.research.financial_statements.financial_statements_models import FinancialStatementsData, FinancialStatementsAnalysis


@flow(name="financial-statements-flow", log_prints=True)
async def financial_statements_flow(symbol: str) -> FinancialStatementsAnalysis:
    """
    Main flow for analyzing recent financial statements for changes in revenue drivers, cost structures, and working capital.
    
    This analysis directly informs the accuracy of near-term projections by examining recent operational changes
    that affect business fundamentals driving earnings.
    
    Args:
        symbol: Stock symbol to research
    Returns:
        FinancialStatementsAnalysis containing the research results and trends
    """
    logger = get_run_logger()
    
    logger.info(f"Starting financial statements flow for {symbol}")
    
    # Fetch financial statements data from Alpha Vantage
    financial_data: FinancialStatementsData = await financial_statements_fetch_task(symbol)

    # Perform financial statements analysis
    financial_analysis: FinancialStatementsAnalysis = await financial_statements_analysis_task(
        symbol, financial_data
    )

    logger.info(f"Financial statements flow completed for {symbol}: "
               f"Revenue drivers: {financial_analysis.revenue_driver_trend}, "
               f"Cost efficiency: {financial_analysis.cost_structure_trend}, "
               f"Working capital: {financial_analysis.working_capital_trend}")

    return financial_analysis