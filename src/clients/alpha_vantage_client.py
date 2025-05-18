import os
from dotenv import load_dotenv
from alpha_vantage.timeseries import TimeSeries
import requests
from datetime import datetime, timedelta
import logging as log



class AlphaVantageClient: 
    def __init__(self) -> None:
        load_dotenv()  # Load environment variables
        api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        if not api_key:
            raise ValueError("ALPHA_VANTAGE_API_KEY not found in environment.")
        self.api_key = api_key
        self.ts = TimeSeries(key=api_key, output_format='pandas')
        self.base_url = "https://www.alphavantage.co/query"

    def get_intraday_data(self, symbol: str, interval: str ='1min', outputsize: str ='compact') -> tuple:
        try:
            data, meta_data = self.ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
            return data, meta_data
        except Exception as e:
            log.error("Error fetching intraday data for %s: %s", symbol, e)
            return None, None

    def check_connectivity(self) -> None:
        """Checks connectivity by fetching SPY intraday."""
        log.info("Checking connectivity to Alpha Vantage...")
        try:
            data, _ = self.get_intraday_data(symbol='SPY')
            if data is not None:
                log.info("Successfully connected and fetched SPY data.")
            else:
                log.error("Failed to fetch SPY data from Alpha Vantage.")
        except Exception as e:
            log.error("Unexpected error during connectivity check: %s", e)

    def get_daily_closing_price(self, symbol: str) -> tuple:
        """
        Fetches the most recent daily closing price.
        Returns (closing_price, date) or (None, None) on error.
        """
        try:
            data, _ = self.ts.get_daily(symbol=symbol, outputsize='compact')
            if data is not None and not data.empty:
                most_recent_date = data.index[0]
                closing_price = data.loc[most_recent_date]['4. close']
                return closing_price, most_recent_date
            else:
                log.info("No daily data returned for %s.", symbol)
                return None, None
        except Exception as e:
            log.error("Error fetching daily closing price for %s: %s", symbol, e)
            return None, None

    def _fetch_json(self, params: dict) -> dict:
        """Generic fetcher for Alpha Vantage JSON endpoints."""
        try:
            response = requests.get(self.base_url, params={**params, 'apikey': self.api_key}, timeout=10)
            response.raise_for_status()
            return dict(response.json())
        except Exception as e:
            log.error("Error fetching %s: %s", params.get('function'), e)
            return {}

    def get_news(self, symbol: str) -> list:
        """Fetches recent news sentiment for the given symbol."""
        params = {
            'function': 'NEWS_SENTIMENT',
            'tickers': symbol,
            'sort': 'relevance',
            'time_from': (datetime.now() - timedelta(days=180)).strftime('%Y%m%dT%H%M')
        }
        data = self._fetch_json(params)
        feed = data.get('feed')
        if feed:
            log.debug("Recent news for %s:", symbol)
            for n in feed:
                log.debug("- %s", n.get('title', '[No title]'))
            return list(feed)
        else:
            log.info("No news data found for %s. Response: %s", symbol, data)
            return []

    def get_company_overview(self, symbol: str) -> dict:
        """Fetches company overview metrics for the given symbol."""
        params = {'function': 'OVERVIEW', 'symbol': symbol}
        data = self._fetch_json(params)
        if data and data.get('Symbol'):
            return data
        else:
            log.info("No overview data found for %s. Response: %s", symbol, data)
            return {}

