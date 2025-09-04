from src.tasks.financial_statements.financial_statements_fetch_task import financial_statements_fetch_task
from src.tasks.financial_statements.financial_statements_analysis_task import financial_statements_analysis_task
from src.tasks.financial_statements.financial_statements_reporting_task import financial_statements_reporting_task
from src.tasks.common.status_update_task import publish_status_update_task
from src.research.financial_statements.financial_statements_models import FinancialStatementsData, FinancialStatementsAnalysis
import logging
import time

logger = logging.getLogger(__name__)

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
    start_time = time.time()
    logger.info(f"Financial statements flow started for {symbol}")
    
    await publish_status_update_task("starting", {"flow": "financial_statements_flow", "symbol": symbol})
    
    # Fetch financial statements data from Alpha Vantage
    financial_data: FinancialStatementsData = await financial_statements_fetch_task(symbol)

    # Perform financial statements analysis
    financial_analysis: FinancialStatementsAnalysis = await financial_statements_analysis_task(
        symbol, financial_data
    )

    # Generate reporting output
    await financial_statements_reporting_task(symbol, financial_analysis)

    logger.info(f"Financial statements flow completed for {symbol} in {int(time.time() - start_time)} seconds")
    
    await publish_status_update_task("completed", {"flow": "financial_statements_flow", "symbol": symbol, "duration_seconds": int(time.time() - start_time)})

    return financial_analysis