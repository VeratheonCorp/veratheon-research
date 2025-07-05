import pytest
from unittest.mock import patch, MagicMock
from lib.clients.alpha_vantage_client import AlphaVantageClient

@pytest.fixture
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("ALPHA_VANTAGE_API_KEY", "test_api_key")

@patch('lib.clients.alpha_vantage_client.requests.Session')
def test_run_query_success(mock_session, mock_env_vars):
    # Arrange
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.headers = {'Content-Type': 'application/json'}
    mock_response.json.return_value = {'foo': 'bar'}
    mock_session.return_value.get.return_value = mock_response

    client = AlphaVantageClient()
    
    # Act
    result = client.run_query("test_query")

    # Assert
    assert result == {'foo': 'bar'}
    mock_session.return_value.get.assert_called_once_with('https://www.alphavantage.co/query?function=test_query&apikey=test_api_key')

@patch('lib.clients.alpha_vantage_client.requests.Session')
def test_run_query_http_error(mock_session, mock_env_vars):
    # Arrange
    mock_response = MagicMock()
    mock_response.raise_for_status.side_effect = Exception("HTTP Error")
    mock_session.return_value.get.return_value = mock_response

    client = AlphaVantageClient()

    # Act & Assert
    with pytest.raises(Exception, match="HTTP Error"):
        client.run_query("test_query")

@patch('lib.clients.alpha_vantage_client.load_dotenv')
def test_missing_api_key(mock_load_dotenv, monkeypatch):
    # Arrange
    monkeypatch.delenv("ALPHA_VANTAGE_API_KEY", raising=False)

    # Act & Assert
    with pytest.raises(ValueError, match="ALPHA_VANTAGE_API_KEY not found in environment."):
        AlphaVantageClient()
