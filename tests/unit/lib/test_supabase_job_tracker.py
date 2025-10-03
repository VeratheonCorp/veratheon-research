"""Tests for Supabase job tracker functionality."""

import pytest
from unittest.mock import MagicMock
from datetime import datetime
from src.lib.supabase_job_tracker import JobTracker, JobStatus


class TestJobTracker:
    """Test JobTracker class."""

    @pytest.fixture
    def mock_response(self):
        """Create a mock Supabase response."""
        response = MagicMock()
        response.data = []
        return response

    @pytest.fixture
    def tracker_with_mock(self, mock_supabase_client, mock_response):
        """Create a JobTracker instance with mocked client."""
        tracker = JobTracker()
        tracker._client = mock_supabase_client
        # Setup default mock response
        mock_supabase_client.table.return_value.execute.return_value = mock_response
        return tracker, mock_supabase_client, mock_response

    def test_create_job(self, tracker_with_mock):
        """Test creating a new job."""
        tracker, mock_client, mock_response = tracker_with_mock

        # Mock successful insert
        mock_response.data = [{"id": 123}]

        job_id = tracker.create_job("research", "AAPL", metadata={"user": "test"})

        assert job_id == "123"
        mock_client.table.assert_called_with("research_jobs")
        # Verify insert was called
        assert mock_client.table.return_value.insert.called

    def test_update_job_status(self, tracker_with_mock):
        """Test updating job status."""
        tracker, mock_client, mock_response = tracker_with_mock

        # Mock getting current job data first
        mock_get_response = MagicMock()
        mock_get_response.data = [{
            "id": 123,
            "status": "pending",
            "metadata": {"steps": [], "job_type": "research"}
        }]

        # Mock update response
        mock_update_response = MagicMock()
        mock_update_response.data = [{"id": 123, "status": "running"}]

        # Setup to return different responses for select and update
        mock_client.table.return_value.execute.side_effect = [
            mock_get_response,
            mock_update_response
        ]

        result = tracker.update_job_status("123", JobStatus.RUNNING, step="Analyzing data")

        assert result is True

    def test_complete_job(self, tracker_with_mock):
        """Test completing a job with result data."""
        tracker, mock_client, mock_response = tracker_with_mock

        # Mock getting current job data
        mock_get_response = MagicMock()
        mock_get_response.data = [{
            "id": 123,
            "status": "running",
            "metadata": {"steps": [], "job_type": "research"}
        }]

        # Mock update response
        mock_update_response = MagicMock()
        mock_update_response.data = [{"id": 123, "status": "completed"}]

        mock_client.table.return_value.execute.side_effect = [
            mock_get_response,
            mock_update_response
        ]

        result_data = {"analysis": "Complete"}
        result = tracker.update_job_status("123", JobStatus.COMPLETED, result=result_data)

        assert result is True

    def test_fail_job(self, tracker_with_mock):
        """Test failing a job with error message."""
        tracker, mock_client, mock_response = tracker_with_mock

        # Mock getting current job data
        mock_get_response = MagicMock()
        mock_get_response.data = [{
            "id": 123,
            "status": "running",
            "metadata": {"steps": [], "job_type": "research"}
        }]

        # Mock update response
        mock_update_response = MagicMock()
        mock_update_response.data = [{"id": 123, "status": "failed"}]

        mock_client.table.return_value.execute.side_effect = [
            mock_get_response,
            mock_update_response
        ]

        result = tracker.update_job_status("123", JobStatus.FAILED, error="Error occurred")

        assert result is True

    def test_get_job_status(self, tracker_with_mock):
        """Test getting job status."""
        tracker, mock_client, mock_response = tracker_with_mock

        # Mock job data
        mock_response.data = [{
            "id": 123,
            "symbol": "AAPL",
            "status": "running",
            "created_at": "2025-01-01T00:00:00",
            "updated_at": "2025-01-01T00:00:00",
            "metadata": {"job_type": "research", "steps": ["step1", "step2"]}
        }]

        status = tracker.get_job_status("123")

        assert status is not None
        assert status["status"] == "running"
        assert status["symbol"] == "AAPL"

    def test_get_job_status_not_found(self, tracker_with_mock):
        """Test getting status for non-existent job."""
        tracker, mock_client, mock_response = tracker_with_mock

        # Mock empty response
        mock_response.data = []

        status = tracker.get_job_status("999")

        assert status is None

    def test_cancel_job(self, tracker_with_mock):
        """Test cancelling a job."""
        tracker, mock_client, mock_response = tracker_with_mock

        # Mock getting current job data
        mock_get_response = MagicMock()
        mock_get_response.data = [{
            "id": 123,
            "status": "running",
            "metadata": {"steps": [], "job_type": "research"}
        }]

        # Mock update response
        mock_update_response = MagicMock()
        mock_update_response.data = [{"id": 123, "status": "cancelled"}]

        mock_client.table.return_value.execute.side_effect = [
            mock_get_response,
            mock_update_response
        ]

        result = tracker.cancel_job("123")

        assert result is True

    def test_create_job_exception_handling(self, tracker_with_mock):
        """Test create job handles exceptions gracefully."""
        tracker, mock_client, mock_response = tracker_with_mock

        # Mock exception during insert
        mock_client.table.return_value.execute.side_effect = Exception("Database error")

        with pytest.raises(Exception):
            tracker.create_job("research", "AAPL")

    def test_update_job_status_invalid_id(self, tracker_with_mock):
        """Test update job status with invalid job ID."""
        tracker, mock_client, mock_response = tracker_with_mock

        # Mock empty response (job not found)
        mock_response.data = []

        result = tracker.update_job_status("invalid", JobStatus.RUNNING)

        assert result is False
