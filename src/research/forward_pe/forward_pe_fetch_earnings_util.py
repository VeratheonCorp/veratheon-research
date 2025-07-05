from typing import List
from src.lib.alpha_vantage_api import call_alpha_vantage_earnings, call_alpha_vantage_earnings_calendar, call_alpha_vantage_global_quote
from src.research.forward_pe.forward_pe_models import EarningsSummary, RawEarnings, RawGlobalQuote

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
        raw_earnings: RawEarnings = call_alpha_vantage_earnings(symbol)

        raw_earnings_calendar_json = call_alpha_vantage_earnings_calendar(symbol)
        raw_earnings_calendar = [dict(zip(raw_earnings_calendar_json.earnings_calendar[0].keys(), row)) for row in raw_earnings_calendar_json.earnings_calendar]
        next_quarter_consensus_eps = [row['estimate'] for row in raw_earnings_calendar]

        raw_global_quote: RawGlobalQuote = call_alpha_vantage_global_quote(symbol)
        
        
        # Ensure horizon is at least 1 year
        horizon = max(1, int(horizon))
        
        # Truncate annual earnings
        if raw_earnings.annual_earnings:
            raw_earnings.annual_earnings = raw_earnings.annual_earnings[:horizon]
        
        # Truncate quarterly earnings (4 quarters per year)
        if raw_earnings.quarterly_earnings:
            raw_earnings.quarterly_earnings = raw_earnings.quarterly_earnings[:horizon * 4]
        
        earnings_summaries.append(EarningsSummary(
            symbol=symbol,
            annual_earnings=raw_earnings.annual_earnings,
            quarterly_earnings=raw_earnings.quarterly_earnings,
            next_quarter_consensus_eps=next_quarter_consensus_eps,
            closing_price=raw_global_quote.price
        ))

    return earnings_summaries


if __name__ == "__main__":
    print(get_quarterly_eps_data_for_symbols(["AAPL", "MSFT", "GOOGL", "AMZN", "META"], 3))
