import pytest
from unittest.mock import patch, MagicMock
from src.tasks.common.status_update_task import publish_status_update_task


class TestStatusUpdateTask:
    
    @patch('src.tasks.common.status_update_task.redis.from_url')
    @pytest.mark.anyio
    async def test_publish_status_update_task_success(self, mock_redis_from_url):
        """Test successful status update publishing."""
        # Mock Redis client
        mock_redis_client = MagicMock()
        mock_redis_client.publish.return_value = 1  # Indicates 1 subscriber received the message
        mock_redis_from_url.return_value = mock_redis_client
        
        result = await publish_status_update_task(
            "starting",
            {"flow": "historical_earnings_flow", "symbol": "AAPL"}
        )
        
        assert result is True
        mock_redis_from_url.assert_called_once_with("redis://localhost:6379/0", decode_responses=True)
        mock_redis_client.publish.assert_called_once()
        mock_redis_client.close.assert_called_once()
        
        # Check the published message structure
        call_args = mock_redis_client.publish.call_args
        channel, message = call_args[0]
        assert channel == "research_status_updates"
        
        # Parse the JSON message to verify structure
        import json
        parsed_message = json.loads(message)
        assert parsed_message["status"] == "starting"
        assert parsed_message["details"]["flow"] == "historical_earnings_flow"
        assert parsed_message["details"]["symbol"] == "AAPL"
        assert "timestamp" in parsed_message

    @patch('src.tasks.common.status_update_task.redis.from_url')
    @pytest.mark.anyio
    async def test_publish_status_update_task_no_details(self, mock_redis_from_url):
        """Test status update publishing without details."""
        mock_redis_client = MagicMock()
        mock_redis_client.publish.return_value = 2  # Multiple subscribers
        mock_redis_from_url.return_value = mock_redis_client
        
        result = await publish_status_update_task("completed")
        
        assert result is True
        mock_redis_client.publish.assert_called_once()
        
        # Check the published message has empty details
        call_args = mock_redis_client.publish.call_args
        channel, message = call_args[0]
        
        import json
        parsed_message = json.loads(message)
        assert parsed_message["status"] == "completed"
        assert parsed_message["details"] == {}

    @patch('src.tasks.common.status_update_task.redis.from_url')
    @pytest.mark.anyio
    async def test_publish_status_update_task_no_subscribers(self, mock_redis_from_url):
        """Test status update publishing with no subscribers."""
        mock_redis_client = MagicMock()
        mock_redis_client.publish.return_value = 0  # No subscribers
        mock_redis_from_url.return_value = mock_redis_client
        
        result = await publish_status_update_task("in_progress", {"step": "analysis"})
        
        assert result is False  # Should return False when no subscribers
        mock_redis_client.publish.assert_called_once()
        mock_redis_client.close.assert_called_once()

    @patch.dict('os.environ', {'REDIS_URL': 'redis://custom-host:6380/1'})
    @patch('src.tasks.common.status_update_task.redis.from_url')
    @pytest.mark.anyio
    async def test_publish_status_update_task_custom_redis_url(self, mock_redis_from_url):
        """Test status update publishing with custom Redis URL."""
        mock_redis_client = MagicMock()
        mock_redis_client.publish.return_value = 1
        mock_redis_from_url.return_value = mock_redis_client
        
        result = await publish_status_update_task("starting")
        
        assert result is True
        mock_redis_from_url.assert_called_once_with("redis://custom-host:6380/1", decode_responses=True)

    @patch('src.tasks.common.status_update_task.redis.from_url')
    @pytest.mark.anyio
    async def test_publish_status_update_task_redis_exception(self, mock_redis_from_url):
        """Test status update publishing with Redis exception."""
        # Mock Redis to raise an exception
        mock_redis_from_url.side_effect = Exception("Redis connection failed")
        
        result = await publish_status_update_task("error", {"error": "test error"})
        
        assert result is False  # Should return False on exception
        mock_redis_from_url.assert_called_once()

    @patch('src.tasks.common.status_update_task.redis.from_url')
    @pytest.mark.anyio
    async def test_publish_status_update_task_publish_exception(self, mock_redis_from_url):
        """Test status update publishing with publish exception."""
        mock_redis_client = MagicMock()
        mock_redis_client.publish.side_effect = Exception("Publish failed")
        mock_redis_from_url.return_value = mock_redis_client
        
        result = await publish_status_update_task("failed")
        
        assert result is False  # Should return False on publish exception
        mock_redis_client.publish.assert_called_once()
        # close() should not be called if publish fails
        mock_redis_client.close.assert_not_called()