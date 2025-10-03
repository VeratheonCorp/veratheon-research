import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture(params=["asyncio"])
def anyio_backend(request):
    return request.param


@pytest.fixture
def mock_supabase_client():
    """Mock Supabase client for testing."""
    mock_client = MagicMock()

    # Mock table() chain
    mock_table = MagicMock()
    mock_client.table.return_value = mock_table

    # Mock common query methods
    mock_table.select.return_value = mock_table
    mock_table.insert.return_value = mock_table
    mock_table.update.return_value = mock_table
    mock_table.upsert.return_value = mock_table
    mock_table.delete.return_value = mock_table
    mock_table.eq.return_value = mock_table
    mock_table.lt.return_value = mock_table
    mock_table.gt.return_value = mock_table
    mock_table.in_.return_value = mock_table
    mock_table.like.return_value = mock_table
    mock_table.limit.return_value = mock_table

    # Mock execute() to return empty response by default
    mock_response = MagicMock()
    mock_response.data = []
    mock_table.execute.return_value = mock_response

    return mock_client


@pytest.fixture
def mock_supabase_cache(mock_supabase_client):
    """Mock SupabaseCache for testing."""
    with patch('src.lib.supabase_cache.get_supabase_client', return_value=mock_supabase_client):
        from src.lib.supabase_cache import SupabaseCache
        cache = SupabaseCache()
        yield cache


@pytest.fixture
def mock_job_tracker(mock_supabase_client):
    """Mock JobTracker for testing."""
    with patch('src.lib.supabase_job_tracker.get_supabase_client', return_value=mock_supabase_client):
        from src.lib.supabase_job_tracker import JobTracker
        tracker = JobTracker()
        yield tracker


@pytest.fixture(autouse=True)
def mock_supabase_globally():
    """Automatically mock Supabase client for all tests to prevent real connections."""
    mock_client = MagicMock()

    # Mock table() chain
    mock_table = MagicMock()
    mock_client.table.return_value = mock_table

    # Mock common query methods
    mock_table.select.return_value = mock_table
    mock_table.insert.return_value = mock_table
    mock_table.update.return_value = mock_table
    mock_table.upsert.return_value = mock_table
    mock_table.delete.return_value = mock_table
    mock_table.eq.return_value = mock_table
    mock_table.lt.return_value = mock_table
    mock_table.gt.return_value = mock_table
    mock_table.in_.return_value = mock_table
    mock_table.like.return_value = mock_table
    mock_table.limit.return_value = mock_table

    # Mock execute() to return empty response by default
    mock_response = MagicMock()
    mock_response.data = []
    mock_table.execute.return_value = mock_response

    with patch('src.lib.supabase_client.get_supabase_client', return_value=mock_client):
        yield mock_client