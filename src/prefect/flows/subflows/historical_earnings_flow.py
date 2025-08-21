from prefect import flow, get_run_logger
from src.prefect.tasks.historical_earnings.historical_earnings_fetch_task import historical_earnings_fetch_task
from src.prefect.tasks.historical_earnings.historical_earnings_analysis_task import historical_earnings_analysis_task
from src.prefect.tasks.events.event_emission_task import emit_event_task
from src.research.historical_earnings.historical_earnings_models import HistoricalEarningsData, HistoricalEarningsAnalysis


@flow(name="historical-earnings-flow", log_prints=True)
async def historical_earnings_flow(symbol: str) -> HistoricalEarningsAnalysis:
    """
    Main flow for running historical earnings analysis.
    
    Analyzes historical earnings data for patterns in beats/misses, revenue growth rates, 
    and margin trends to establish baseline performance and predictability context.
    
    Args:
        symbol: Stock symbol to research
    Returns:
        HistoricalEarningsAnalysis containing the research results and patterns
    """
    logger = get_run_logger()
    
    # Emit stage start event
    emit_event_task(symbol, "stage_start", stage="historical_earnings", 
                   message="Starting historical earnings analysis...")
    
    logger.info(f"Starting historical earnings flow for {symbol}")
    
    # Fetch historical earnings data from Alpha Vantage
    historical_data: HistoricalEarningsData = await historical_earnings_fetch_task(symbol)

    # Perform historical earnings analysis
    historical_analysis: HistoricalEarningsAnalysis = await historical_earnings_analysis_task(
        symbol, historical_data
    )

    logger.info(f"Historical earnings flow completed for {symbol}: "
               f"Pattern: {historical_analysis.earnings_pattern}, "
               f"Predictability: {historical_analysis.predictability_score}/10")

    # Emit stage complete event
    emit_event_task(symbol, "stage_complete", stage="historical_earnings",
                   message="Historical earnings analysis completed",
                   data={
                       "earnings_pattern": historical_analysis.earnings_pattern,
                       "revenue_growth_trend": historical_analysis.revenue_growth_trend,
                       "margin_trend": historical_analysis.margin_trend,
                       "predictability_score": historical_analysis.predictability_score
                   })

    return historical_analysis