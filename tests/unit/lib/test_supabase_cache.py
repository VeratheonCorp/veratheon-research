"""Tests for Supabase cache functionality."""

import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from src.lib.supabase_cache import SupabaseCache


class TestSupabaseCache:
    """Test SupabaseCache class."""

    @pytest.fixture
    def mock_response(self):
        """Create a mock Supabase response."""
        response = MagicMock()
        response.data = []
        return response

    @pytest.fixture
    def cache_with_mock(self, mock_supabase_client, mock_response):
        """Create a SupabaseCache instance with mocked client."""
        cache = SupabaseCache()
        cache._client = mock_supabase_client
        # Setup default mock response
        mock_supabase_client.table.return_value.execute.return_value = mock_response
        return cache, mock_supabase_client, mock_response

    def test_cache_report_success(self, cache_with_mock):
        """Test caching a report successfully."""
        cache, mock_client, mock_response = cache_with_mock

        test_data = {"analysis": "Test analysis", "symbol": "AAPL"}
        result = cache.cache_report("test_report", "AAPL", test_data, ttl=3600)

        assert result is True
        mock_client.table.assert_called_with("research_cache")
        # Verify upsert was called
        assert mock_client.table.return_value.upsert.called

    def test_get_cached_report_hit(self, cache_with_mock):
        """Test getting a cached report (cache hit)."""
        cache, mock_client, mock_response = cache_with_mock

        # Mock cache hit
        future_time = (datetime.now() + timedelta(hours=1)).isoformat()
        mock_response.data = [{
            "data": {"analysis": "Cached analysis"},
            "expires_at": future_time
        }]

        result = cache.get_cached_report("test_report", "AAPL")

        assert result is not None
        assert result["analysis"] == "Cached analysis"
        mock_client.table.assert_called_with("research_cache")

    def test_get_cached_report_miss(self, cache_with_mock):
        """Test getting a cached report (cache miss)."""
        cache, mock_client, mock_response = cache_with_mock

        # Mock cache miss (empty response)
        mock_response.data = []

        result = cache.get_cached_report("test_report", "AAPL")

        assert result is None

    def test_get_cached_report_expired(self, cache_with_mock):
        """Test getting an expired cached report."""
        cache, mock_client, mock_response = cache_with_mock

        # Mock expired cache entry
        past_time = (datetime.now() - timedelta(hours=1)).isoformat()
        mock_response.data = [{
            "data": {"analysis": "Expired analysis"},
            "expires_at": past_time
        }]

        result = cache.get_cached_report("test_report", "AAPL")

        assert result is None

    def test_cache_analysis_with_pydantic_model(self, cache_with_mock):
        """Test caching analysis with a pydantic model."""
        cache, mock_client, mock_response = cache_with_mock

        # Mock pydantic model
        mock_model = MagicMock()
        mock_model.model_dump.return_value = {"field1": "value1", "field2": "value2"}

        result = cache.cache_analysis("test_analysis", "AAPL", mock_model)

        assert result is True
        mock_model.model_dump.assert_called_once()

    def test_invalidate_cache_pattern(self, cache_with_mock):
        """Test invalidating cache entries by pattern."""
        cache, mock_client, mock_response = cache_with_mock

        # Mock deleted entries
        mock_response.data = [{"id": 1}, {"id": 2}, {"id": 3}]

        deleted_count = cache.invalidate_cache("report:test_*")

        assert deleted_count == 3
        # Verify pattern was converted from Redis wildcard to SQL LIKE
        assert mock_client.table.return_value.like.called

    def test_get_cache_info_with_symbol(self, cache_with_mock):
        """Test getting cache info filtered by symbol."""
        cache, mock_client, mock_response = cache_with_mock

        mock_response.data = [
            {
                "cache_key": "report:test:AAPL:20250101",
                "cache_type": "report",
                "symbol": "AAPL",
                "created_at": datetime.now().isoformat(),
                "expires_at": (datetime.now() + timedelta(hours=1)).isoformat()
            }
        ]

        info = cache.get_cache_info("AAPL")

        assert info["total_cached_items"] == 1
        assert len(info["keys"]) == 1
        assert "report:test:AAPL:20250101" in info["keys"]
        # Verify symbol filter was applied
        mock_client.table.return_value.eq.assert_called_with("symbol", "AAPL")

    def test_cache_report_exception_handling(self, cache_with_mock):
        """Test cache report handles exceptions gracefully."""
        cache, mock_client, mock_response = cache_with_mock

        # Mock exception during upsert
        mock_client.table.return_value.upsert.side_effect = Exception("Database error")

        result = cache.cache_report("test_report", "AAPL", {"data": "test"})

        assert result is False

    def test_get_cached_report_exception_handling(self, cache_with_mock):
        """Test get cached report handles exceptions gracefully."""
        cache, mock_client, mock_response = cache_with_mock

        # Mock exception during query
        mock_client.table.return_value.execute.side_effect = Exception("Query error")

        result = cache.get_cached_report("test_report", "AAPL")

        assert result is None
