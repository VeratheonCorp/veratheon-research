from typing import List
from src.lib.alpha_vantage_api import call_alpha_vantage_earnings, call_alpha_vantage_earnings_calendar, call_alpha_vantage_global_quote, call_alpha_vantage_overview
from src.research.forward_pe.forward_pe_models import EarningsSummary, RawEarnings, RawGlobalQuote
import logging
log = logging.getLogger(__name__)

def get_quarterly_eps_data_for_symbols(symbols: List[str], horizon: int) -> List[EarningsSummary]:
    """
    Calls Alpha Vantage APIs for the specified symbols and returns all necessary data for forward PE analysis.
    
    Args:
        symbols: List of stock symbols to get earnings for
        horizon: Number of years of earnings data to return (minimum 1 year).
    
    Returns:
        A list of EarningsSummary objects containing annual and quarterly earnings data, 
        as well as the next quarter's consensus EPS estimate, and the latest closing price.
    """
    earnings_summaries = []

    for symbol in symbols:

        # Get the overview data for the symbol
        overview_json = call_alpha_vantage_overview(symbol)
        # If the overview data is empty, skip this symbol
        if not overview_json:
            log.warning(f"Overview data is empty for symbol: {symbol}. Skipping.")
            continue

        # Get the earnings data for the symbol
        raw_earnings: RawEarnings = call_alpha_vantage_earnings(symbol)

        # Get the earnings calendar for the symbol
        raw_earnings_calendar_json = call_alpha_vantage_earnings_calendar(symbol)
        next_quarter_consensus_eps = raw_earnings_calendar_json.get('earnings_calendar', [{}])[0].get('estimate', "Not enough consensus")
    
        raw_global_quote: RawGlobalQuote = call_alpha_vantage_global_quote(symbol)
        current_price = raw_global_quote['Global Quote']['05. price']
        
        # Parse horizon in months
        if isinstance(horizon, str) and 'month' in horizon.lower():
            try:
                months = int(horizon.lower().replace('month', '').strip())
            except ValueError:
                log.warning("Could not parse horizon, defaulting to 12 months")
                months = 12
        else:
            # Convert years to months if not already in months
            months = int(horizon) * 12 if horizon else 12
        
        # Calculate the number of full quarters in the horizon
        quarters = max(4, (months + 2) // 3)  # Round up to nearest quarter
        
        # Truncate quarterly earnings first
        if raw_earnings['quarterlyEarnings']:
            raw_earnings['quarterlyEarnings'] = raw_earnings['quarterlyEarnings'][:quarters]

        earnings_summary = EarningsSummary(
            symbol=symbol,
            quarterly_earnings=raw_earnings['quarterlyEarnings'],
            next_quarter_consensus_eps=str(next_quarter_consensus_eps),
            closing_price=current_price
        )

        print(earnings_summary)
        
        earnings_summaries.append(earnings_summary)

    return earnings_summaries


if __name__ == "__main__":
    print(get_quarterly_eps_data_for_symbols(["AAPL", "MSFT", "GOOGL", "AMZN", "META"], 3))
