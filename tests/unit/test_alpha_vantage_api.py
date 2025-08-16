import pytest
from unittest.mock import patch, MagicMock
from src.lib.alpha_vantage_api import (
    call_alpha_vantage,
    call_alpha_vantage_overview,
    call_alpha_vantage_income_statement,
    call_alpha_vantage_balance_sheet,
    call_alpha_vantage_cash_flow,
    call_alpha_vantage_global_quote,
    call_alpha_vantage_earnings,
    call_alpha_vantage_time_series_daily_adjusted,
    call_alpha_vantage_news_sentiment,
    call_alpha_vantage_rsi,
    call_alpha_vantage_macd,
)

@pytest.fixture
def mock_alpha_vantage_client():
    with patch('src.lib.alpha_vantage_api.client', new_callable=MagicMock) as mock_client:
        yield mock_client

def test_call_alpha_vantage(mock_alpha_vantage_client):
    # Arrange
    mock_alpha_vantage_client.run_query.return_value = {'success': True}
    
    # Act
    result = call_alpha_vantage("TEST_URI")
    
    # Assert
    assert result == {'success': True}
    mock_alpha_vantage_client.run_query.assert_called_once_with("TEST_URI")

def test_call_alpha_vantage_overview(mock_alpha_vantage_client):
    call_alpha_vantage_overview("AAPL")
    mock_alpha_vantage_client.run_query.assert_called_once_with("OVERVIEW&symbol=AAPL")

def test_call_alpha_vantage_income_statement(mock_alpha_vantage_client):
    call_alpha_vantage_income_statement("MSFT")
    mock_alpha_vantage_client.run_query.assert_called_once_with("INCOME_STATEMENT&symbol=MSFT")

def test_call_alpha_vantage_balance_sheet(mock_alpha_vantage_client):
    call_alpha_vantage_balance_sheet("GOOGL")
    mock_alpha_vantage_client.run_query.assert_called_once_with("BALANCE_SHEET&symbol=GOOGL")

def test_call_alpha_vantage_cash_flow(mock_alpha_vantage_client):
    call_alpha_vantage_cash_flow("AMZN")
    mock_alpha_vantage_client.run_query.assert_called_once_with("CASH_FLOW&symbol=AMZN")

def test_call_alpha_vantage_global_quote(mock_alpha_vantage_client):
    call_alpha_vantage_global_quote("NFLX")
    mock_alpha_vantage_client.run_query.assert_called_once_with("GLOBAL_QUOTE&symbol=NFLX")

def test_call_alpha_vantage_earnings(mock_alpha_vantage_client):
    call_alpha_vantage_earnings("NVDA")
    mock_alpha_vantage_client.run_query.assert_called_once_with("EARNINGS&symbol=NVDA")

def test_call_alpha_vantage_time_series_daily_adjusted(mock_alpha_vantage_client):
    call_alpha_vantage_time_series_daily_adjusted("TSLA")
    mock_alpha_vantage_client.run_query.assert_called_once_with("TIME_SERIES_DAILY_ADJUSTED&symbol=TSLA")

def test_call_alpha_vantage_news_sentiment(mock_alpha_vantage_client):
    call_alpha_vantage_news_sentiment("AAPL,MSFT")
    mock_alpha_vantage_client.run_query.assert_called_once_with("NEWS_SENTIMENT&tickers=AAPL,MSFT")

def test_call_alpha_vantage_rsi(mock_alpha_vantage_client):
    call_alpha_vantage_rsi("AMD")
    mock_alpha_vantage_client.run_query.assert_called_once_with("RSI&symbol=AMD&interval=daily&time_period=14&series_type=close")

def test_call_alpha_vantage_macd(mock_alpha_vantage_client):
    call_alpha_vantage_macd("INTC")
    mock_alpha_vantage_client.run_query.assert_called_once_with("MACD&symbol=INTC&interval=daily&fastperiod=12&slowperiod=26&signalperiod=9")
