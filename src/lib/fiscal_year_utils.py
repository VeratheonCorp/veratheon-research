"""
Fiscal Year Utilities

Centralized logic for determining whether to use quarterly or annual data
based on a company's fiscal year timing.
"""

import logging
from datetime import datetime, timedelta
from typing import Tuple, Optional
from dataclasses import dataclass

from src.lib.alpha_vantage_api import call_alpha_vantage_overview

logger = logging.getLogger(__name__)


@dataclass
class FiscalYearInfo:
    """Information about a company's fiscal year and data selection decision."""

    symbol: str
    fiscal_year_end_month: str
    fiscal_year_end_date: Optional[datetime]
    use_annual_data: bool
    days_to_fiscal_end: Optional[int]
    decision_reason: str


def parse_fiscal_year_end(fiscal_year_end_str: str, current_year: Optional[int] = None) -> datetime:
    """
    Parse Alpha Vantage fiscal year end string into a datetime object.

    Args:
        fiscal_year_end_str: String like "September", "December", etc.
        current_year: Year to use (defaults to current year)

    Returns:
        datetime object for the next fiscal year end date

    Raises:
        ValueError: If fiscal year end string cannot be parsed
    """
    if current_year is None:
        current_year = datetime.now().year

    month_mapping = {
        "january": 1, "february": 2, "march": 3, "april": 4,
        "may": 5, "june": 6, "july": 7, "august": 8,
        "september": 9, "october": 10, "november": 11, "december": 12
    }

    month_name = fiscal_year_end_str.lower().strip()
    if month_name not in month_mapping:
        raise ValueError(f"Could not parse fiscal year end: {fiscal_year_end_str}")

    month = month_mapping[month_name]

    # Get the last day of the fiscal year end month
    if month == 2:  # February
        # Handle leap years
        if current_year % 4 == 0 and (current_year % 100 != 0 or current_year % 400 == 0):
            day = 29
        else:
            day = 28
    elif month in [4, 6, 9, 11]:  # April, June, September, November
        day = 30
    else:
        day = 31

    # Calculate the next fiscal year end
    fiscal_end_this_year = datetime(current_year, month, day)

    if datetime.now() <= fiscal_end_this_year:
        return fiscal_end_this_year
    else:
        # If we've passed this year's fiscal end, next one is next year
        next_year = current_year + 1
        if month == 2 and next_year % 4 == 0 and (next_year % 100 != 0 or next_year % 400 == 0):
            day = 29
        else:
            day = 28 if month == 2 else (30 if month in [4, 6, 9, 11] else 31)
        return datetime(next_year, month, day)


def get_fiscal_year_info(symbol: str, threshold_days: int = 90) -> FiscalYearInfo:
    """
    Get fiscal year information and determine whether to use annual vs quarterly data.

    Args:
        symbol: Stock symbol
        threshold_days: Number of days from fiscal year end to switch to annual data (default: 90)

    Returns:
        FiscalYearInfo object with decision and reasoning
    """
    try:
        # Get company overview data
        overview = call_alpha_vantage_overview(symbol)
        fiscal_year_end_str = overview.get('FiscalYearEnd')

        if not fiscal_year_end_str:
            logger.warning(f"No fiscal year end data available for {symbol}")
            return FiscalYearInfo(
                symbol=symbol,
                fiscal_year_end_month="Unknown",
                fiscal_year_end_date=None,
                use_annual_data=False,
                days_to_fiscal_end=None,
                decision_reason="No fiscal year end data available - defaulting to quarterly"
            )

        # Parse fiscal year end
        fiscal_year_end = parse_fiscal_year_end(fiscal_year_end_str)
        today = datetime.now()

        # Calculate days until fiscal year end
        days_to_fiscal_end = (fiscal_year_end - today).days

        # If within threshold days of fiscal year end, use annual data
        use_annual = abs(days_to_fiscal_end) <= threshold_days

        if use_annual:
            decision_reason = (
                f"Within {threshold_days} days of fiscal year end "
                f"({fiscal_year_end.strftime('%Y-%m-%d')}) - using annual data for "
                f"more stable year-end projections"
            )
        else:
            decision_reason = (
                f"More than {threshold_days} days from fiscal year end "
                f"({fiscal_year_end.strftime('%Y-%m-%d')}) - using quarterly data for "
                f"more timely analysis"
            )

        logger.info(f"Fiscal year decision for {symbol}: {'ANNUAL' if use_annual else 'QUARTERLY'} - {decision_reason}")

        return FiscalYearInfo(
            symbol=symbol,
            fiscal_year_end_month=fiscal_year_end_str,
            fiscal_year_end_date=fiscal_year_end,
            use_annual_data=use_annual,
            days_to_fiscal_end=days_to_fiscal_end,
            decision_reason=decision_reason
        )

    except Exception as e:
        logger.error(f"Error determining fiscal timing for {symbol}: {e}")
        return FiscalYearInfo(
            symbol=symbol,
            fiscal_year_end_month="Error",
            fiscal_year_end_date=None,
            use_annual_data=False,
            days_to_fiscal_end=None,
            decision_reason=f"Error determining fiscal timing: {e} - defaulting to quarterly"
        )


def should_use_annual_data(symbol: str, threshold_days: int = 90) -> bool:
    """
    Simple helper function to determine if annual data should be used.

    Args:
        symbol: Stock symbol
        threshold_days: Number of days from fiscal year end to switch to annual data

    Returns:
        True if annual data should be used, False for quarterly
    """
    fiscal_info = get_fiscal_year_info(symbol, threshold_days)
    return fiscal_info.use_annual_data


def get_appropriate_financial_data(financial_data: dict, use_annual: bool, periods: int = 4) -> list:
    """
    Extract the appropriate financial data (quarterly or annual) based on fiscal timing.

    Args:
        financial_data: Financial data from Alpha Vantage (e.g., income statement)
        use_annual: Whether to use annual data
        periods: Number of periods to return

    Returns:
        List of financial statement periods (quarterly or annual)
    """
    if use_annual:
        return financial_data.get('annualReports', [])[:periods]
    else:
        return financial_data.get('quarterlyReports', [])[:periods]


def get_data_period_label(use_annual: bool) -> str:
    """
    Get a human-readable label for the data period being used.

    Args:
        use_annual: Whether annual data is being used

    Returns:
        String label for the data period
    """
    return "annual" if use_annual else "quarterly"


def log_fiscal_decision(symbol: str, threshold_days: int = 90) -> FiscalYearInfo:
    """
    Log the fiscal year decision for debugging and transparency.

    Args:
        symbol: Stock symbol
        threshold_days: Number of days threshold

    Returns:
        FiscalYearInfo object with decision details
    """
    fiscal_info = get_fiscal_year_info(symbol, threshold_days)

    logger.info(f"=== FISCAL YEAR DECISION FOR {symbol} ===")
    logger.info(f"Fiscal Year End: {fiscal_info.fiscal_year_end_month}")
    logger.info(f"Days to Fiscal End: {fiscal_info.days_to_fiscal_end}")
    logger.info(f"Data Selection: {'ANNUAL' if fiscal_info.use_annual_data else 'QUARTERLY'}")
    logger.info(f"Reason: {fiscal_info.decision_reason}")
    logger.info("=" * 50)

    return fiscal_info