from prefect import task, get_run_logger
from src.research.historical_earnings.historical_earnings_models import HistoricalEarningsData, HistoricalEarningsAnalysis
from src.research.historical_earnings.historical_earnings_agent import historical_earnings_analysis_agent
from agents import Runner, RunResult
import json


@task(name="historical_earnings_analysis_task", persist_result=True)
async def historical_earnings_analysis_task(
    symbol: str, 
    historical_data: HistoricalEarningsData
) -> HistoricalEarningsAnalysis:
    """
    Task to perform historical earnings analysis for patterns in beats/misses, revenue growth, and margin trends.
    
    Args:
        symbol: Stock symbol to research
        historical_data: Historical earnings data from Alpha Vantage
    Returns:
        HistoricalEarningsAnalysis containing the analysis results and patterns
    """
    logger = get_run_logger()
    logger.info(f"Performing historical earnings analysis for {symbol}")

    # Prepare the input for the agent
    input_data = f"""
    symbol: {symbol}
    historical_earnings_data: {historical_data.model_dump_json()}
    """

    result: RunResult = await Runner.run(
        historical_earnings_analysis_agent,
        input=input_data
    )
    
    historical_analysis: HistoricalEarningsAnalysis = result.final_output

    logger.info(f"Historical earnings analysis for {symbol}: {json.dumps(historical_analysis.model_dump(), indent=2)}")

    return historical_analysis