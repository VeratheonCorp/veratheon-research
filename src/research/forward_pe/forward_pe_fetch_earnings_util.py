from typing import List, Dict, Any
from src.lib.alpha_vantage_api import call_alpha_vantage_earnings, call_alpha_vantage_earnings_calendar, call_alpha_vantage_global_quote, call_alpha_vantage_overview
from src.research.forward_pe.forward_pe_models import EarningsSummary, RawEarnings, RawGlobalQuote
import logging
log = logging.getLogger(__name__)

def get_quarterly_eps_data_for_symbols(symbols: List[str]) -> List[EarningsSummary]:
    """
    Calls Alpha Vantage APIs for the specified symbols and returns all necessary data for forward PE analysis.
    
    Args:
        symbols: List of stock symbols to get earnings for
    
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

        overview = call_alpha_vantage_overview(symbol)
        clean_overview_of_useless_data(overview)
        
        # Truncate quarterly earnings first
        # Always return 9 quarters of data
        quarters = 9
        if raw_earnings['quarterlyEarnings']:
            raw_earnings['quarterlyEarnings'] = raw_earnings['quarterlyEarnings'][:quarters]

        earnings_summary = EarningsSummary(
            symbol=symbol,
            overview=overview,
            quarterly_earnings=raw_earnings['quarterlyEarnings'],
            next_quarter_consensus_eps=str(next_quarter_consensus_eps),
            current_price=current_price
        )
        
        earnings_summaries.append(earnings_summary)

    return earnings_summaries


def clean_earnings_of_useless_data(earnings: Dict[str, Any]) -> Dict[str, Any]:
    # Remove dates that dont matter
    earnings.pop()

def clean_overview_of_useless_data(overview: Dict[str, Any]) -> Dict[str, Any]:
    # Remove the Description, address, and other useless data
    overview.pop("Symbol", None)
    overview.pop("AssetType", None)
    overview.pop("Name", None)
    overview.pop("Description", None)
    overview.pop("CIK", None)
    overview.pop("Exchange", None)
    overview.pop("Currency", None)
    overview.pop("Country", None)
    overview.pop("Sector", None)
    overview.pop("Industry", None)
    overview.pop("Address", None)
    overview.pop("OfficialSite", None)
    overview.pop("FiscalYearEnd", None)
    overview.pop("LatestQuarter", None)
    # overview.pop("MarketCapitalization", None)
    # overview.pop("Beta", None)
    # overview.pop("52WeekHigh", None)
    # overview.pop("52WeekLow", None)
    # overview.pop("50DayMovingAverage", None)
    # overview.pop("200DayMovingAverage", None)
    # overview.pop("SharesOutstanding", None)
    overview.pop("SharesFloat", None)
    overview.pop("PercentInsiders", None)
    overview.pop("PercentInstitutions", None)
    overview.pop("DividendDate", None)
    overview.pop("ExDividendDate", None)
    overview.pop("AnalystRatingStrongBuy", None)
    overview.pop("AnalystRatingBuy", None)
    overview.pop("AnalystRatingHold", None)
    overview.pop("AnalystRatingSell", None)
    overview.pop("AnalystRatingStrongSell", None)
    # overview.pop("AnalystTargetPrice", None)
    

    
    
    
    