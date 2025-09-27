import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from src.flows.subflows.bottom_up_eps_validation_flow import bottom_up_eps_validation_flow
from src.flows.subflows.peer_relative_eps_validation_flow import peer_relative_eps_validation_flow
from src.flows.subflows.market_sentiment_eps_check_flow import market_sentiment_eps_check_flow
from src.flows.subflows.eps_validation_synthesis_flow import eps_validation_synthesis_flow
from src.research.eps_validation.eps_validation_models import (
    BottomUpEpsValidation,
    PeerRelativeEpsValidation,
    MarketSentimentEpsCheck,
    EpsValidationSynthesis,
    EpsValidationVerdict,
    ConfidenceLevel
)


class TestEpsValidationFlows:

    @pytest.mark.asyncio
    @patch('src.flows.subflows.bottom_up_eps_validation_flow.update_job_status')
    @patch('src.flows.subflows.bottom_up_eps_validation_flow.bottom_up_eps_validation_cache_retrieval_task')
    @patch('src.flows.subflows.bottom_up_eps_validation_flow.bottom_up_eps_validation_task')
    async def test_bottom_up_eps_validation_flow_cache_hit(
        self,
        mock_task,
        mock_cache_task,
        mock_update_status,
        consensus_validated_bottom_up
    ):
        """Test bottom-up EPS validation flow when cache hit occurs."""
        # Mock cache hit
        mock_cache_task.return_value = consensus_validated_bottom_up

        result = await bottom_up_eps_validation_flow(
            symbol="AAPL",
            job_id="test-job-123",
            force_recompute=False
        )

        assert isinstance(result, BottomUpEpsValidation)
        assert result.symbol == "AAPL"
        assert result.validation_verdict == EpsValidationVerdict.CONSENSUS_VALIDATED

        # Verify cache was checked
        mock_cache_task.assert_called_once_with("AAPL", False)
        # Verify task was not called (cache hit)
        mock_task.assert_not_called()
        # Verify status was updated
        mock_update_status.assert_called()

    @pytest.mark.asyncio
    @patch('src.flows.subflows.bottom_up_eps_validation_flow.update_job_status')
    @patch('src.flows.subflows.bottom_up_eps_validation_flow.bottom_up_eps_validation_cache_retrieval_task')
    @patch('src.flows.subflows.bottom_up_eps_validation_flow.bottom_up_eps_validation_task')
    async def test_bottom_up_eps_validation_flow_cache_miss(
        self,
        mock_task,
        mock_cache_task,
        mock_update_status,
        consensus_validated_bottom_up
    ):
        """Test bottom-up EPS validation flow when cache miss occurs."""
        # Mock cache miss
        mock_cache_task.return_value = None
        # Mock task execution
        mock_task.return_value = consensus_validated_bottom_up

        result = await bottom_up_eps_validation_flow(
            symbol="AAPL",
            job_id="test-job-123",
            force_recompute=False,
            financial_statements_data=MagicMock(),
            consensus_eps=6.82
        )

        assert isinstance(result, BottomUpEpsValidation)
        assert result.symbol == "AAPL"

        # Verify cache was checked
        mock_cache_task.assert_called_once_with("AAPL", False)
        # Verify task was called (cache miss)
        mock_task.assert_called_once()
        # Verify status updates
        assert mock_update_status.call_count >= 2  # Start and complete

    @pytest.mark.asyncio
    @patch('src.flows.subflows.bottom_up_eps_validation_flow.update_job_status')
    @patch('src.flows.subflows.bottom_up_eps_validation_flow.bottom_up_eps_validation_cache_retrieval_task')
    @patch('src.flows.subflows.bottom_up_eps_validation_flow.bottom_up_eps_validation_task')
    async def test_bottom_up_eps_validation_flow_force_recompute(
        self,
        mock_task,
        mock_cache_task,
        mock_update_status,
        consensus_validated_bottom_up
    ):
        """Test bottom-up EPS validation flow with force_recompute=True."""
        # Mock task execution
        mock_task.return_value = consensus_validated_bottom_up

        result = await bottom_up_eps_validation_flow(
            symbol="AAPL",
            job_id="test-job-123",
            force_recompute=True
        )

        assert isinstance(result, BottomUpEpsValidation)

        # Verify cache was checked with force_recompute=True
        mock_cache_task.assert_called_once_with("AAPL", True)
        # Verify task was called even if cache might have data
        mock_task.assert_called_once()

    @pytest.mark.asyncio
    @patch('src.flows.subflows.peer_relative_eps_validation_flow.update_job_status')
    @patch('src.flows.subflows.peer_relative_eps_validation_flow.peer_relative_eps_validation_cache_retrieval_task')
    @patch('src.flows.subflows.peer_relative_eps_validation_flow.peer_relative_eps_validation_task')
    async def test_peer_relative_eps_validation_flow_success(
        self,
        mock_task,
        mock_cache_task,
        mock_update_status,
        consensus_validated_peer_relative
    ):
        """Test peer-relative EPS validation flow successful execution."""
        # Mock cache miss and successful task execution
        mock_cache_task.return_value = None
        mock_task.return_value = consensus_validated_peer_relative

        result = await peer_relative_eps_validation_flow(
            symbol="AAPL",
            job_id="test-job-123",
            peer_group_data={"avg_forward_pe": 25.3},
            current_stock_price=175.80,
            consensus_eps=6.82
        )

        assert isinstance(result, PeerRelativeEpsValidation)
        assert result.symbol == "AAPL"
        assert result.peer_comparison_verdict == EpsValidationVerdict.CONSENSUS_VALIDATED

        mock_task.assert_called_once()
        mock_update_status.assert_called()

    @pytest.mark.asyncio
    @patch('src.flows.subflows.market_sentiment_eps_check_flow.update_job_status')
    @patch('src.flows.subflows.market_sentiment_eps_check_flow.market_sentiment_eps_check_cache_retrieval_task')
    @patch('src.flows.subflows.market_sentiment_eps_check_flow.market_sentiment_eps_check_task')
    async def test_market_sentiment_eps_check_flow_success(
        self,
        mock_task,
        mock_cache_task,
        mock_update_status,
        upward_momentum_sentiment
    ):
        """Test market sentiment EPS check flow successful execution."""
        # Mock cache miss and successful task execution
        mock_cache_task.return_value = None
        mock_task.return_value = upward_momentum_sentiment

        result = await market_sentiment_eps_check_flow(
            symbol="NVDA",
            job_id="test-job-123",
            news_sentiment_data={"sentiment_score": 0.8},
            consensus_eps=10.45
        )

        assert isinstance(result, MarketSentimentEpsCheck)
        assert result.symbol == "NVDA"
        assert result.sentiment_validation_verdict == EpsValidationVerdict.CONSENSUS_TOO_LOW

        mock_task.assert_called_once()
        mock_update_status.assert_called()

    @pytest.mark.asyncio
    @patch('src.flows.subflows.eps_validation_synthesis_flow.update_job_status')
    @patch('src.flows.subflows.eps_validation_synthesis_flow.eps_validation_synthesis_cache_retrieval_task')
    @patch('src.flows.subflows.eps_validation_synthesis_flow.eps_validation_synthesis_task')
    async def test_eps_validation_synthesis_flow_success(
        self,
        mock_task,
        mock_cache_task,
        mock_update_status,
        consensus_validated_synthesis,
        consensus_validated_bottom_up,
        consensus_validated_peer_relative,
        stable_momentum_sentiment
    ):
        """Test EPS validation synthesis flow successful execution."""
        # Mock cache miss and successful task execution
        mock_cache_task.return_value = None
        mock_task.return_value = consensus_validated_synthesis

        result = await eps_validation_synthesis_flow(
            symbol="AAPL",
            job_id="test-job-123",
            bottom_up_validation=consensus_validated_bottom_up,
            peer_relative_validation=consensus_validated_peer_relative,
            sentiment_validation=stable_momentum_sentiment
        )

        assert isinstance(result, EpsValidationSynthesis)
        assert result.symbol == "AAPL"
        assert result.overall_verdict == EpsValidationVerdict.CONSENSUS_VALIDATED
        assert result.confidence_score == 0.85

        mock_task.assert_called_once()
        mock_update_status.assert_called()

    @pytest.mark.asyncio
    async def test_flow_error_handling(self):
        """Test that flows handle errors gracefully."""
        with patch('src.flows.subflows.bottom_up_eps_validation_flow.bottom_up_eps_validation_cache_retrieval_task') as mock_cache:
            with patch('src.flows.subflows.bottom_up_eps_validation_flow.bottom_up_eps_validation_task') as mock_task:
                with patch('src.flows.subflows.bottom_up_eps_validation_flow.update_job_status') as mock_status:
                    # Mock cache miss
                    mock_cache.return_value = None
                    # Mock task raising an exception
                    mock_task.side_effect = Exception("Test error")

                    # Flow should handle the exception gracefully
                    result = await bottom_up_eps_validation_flow(
                        symbol="ERROR",
                        job_id="test-job-123"
                    )

                    # Should return a result with insufficient data verdict
                    assert isinstance(result, BottomUpEpsValidation)
                    assert result.symbol == "ERROR"
                    assert result.validation_verdict == EpsValidationVerdict.INSUFFICIENT_DATA

    @pytest.mark.asyncio
    @patch('src.flows.subflows.bottom_up_eps_validation_flow.update_job_status')
    async def test_flow_job_status_integration(self, mock_update_status):
        """Test that flows properly integrate with job status tracking."""
        with patch('src.flows.subflows.bottom_up_eps_validation_flow.bottom_up_eps_validation_cache_retrieval_task', return_value=None):
            with patch('src.flows.subflows.bottom_up_eps_validation_flow.bottom_up_eps_validation_task') as mock_task:
                mock_task.return_value = MagicMock(spec=BottomUpEpsValidation)

                await bottom_up_eps_validation_flow(
                    symbol="AAPL",
                    job_id="test-job-123"
                )

                # Verify status updates were called
                assert mock_update_status.call_count >= 1
                # Verify job_id was passed correctly
                calls = mock_update_status.call_args_list
                for call in calls:
                    args, kwargs = call
                    assert "test-job-123" in args or "test-job-123" in kwargs.values()

    def test_flow_function_signatures(self):
        """Test that all flow functions have the expected signatures."""
        import inspect

        # Check bottom_up_eps_validation_flow signature
        sig = inspect.signature(bottom_up_eps_validation_flow)
        assert 'symbol' in sig.parameters
        assert 'job_id' in sig.parameters
        assert 'force_recompute' in sig.parameters

        # Check peer_relative_eps_validation_flow signature
        sig = inspect.signature(peer_relative_eps_validation_flow)
        assert 'symbol' in sig.parameters
        assert 'job_id' in sig.parameters
        assert 'peer_group_data' in sig.parameters

        # Check market_sentiment_eps_check_flow signature
        sig = inspect.signature(market_sentiment_eps_check_flow)
        assert 'symbol' in sig.parameters
        assert 'job_id' in sig.parameters
        assert 'news_sentiment_data' in sig.parameters

        # Check eps_validation_synthesis_flow signature
        sig = inspect.signature(eps_validation_synthesis_flow)
        assert 'symbol' in sig.parameters
        assert 'job_id' in sig.parameters
        assert 'bottom_up_validation' in sig.parameters

    def test_all_flows_are_async(self):
        """Test that all flow functions are async."""
        import inspect

        flows = [
            bottom_up_eps_validation_flow,
            peer_relative_eps_validation_flow,
            market_sentiment_eps_check_flow,
            eps_validation_synthesis_flow
        ]

        for flow in flows:
            assert inspect.iscoroutinefunction(flow), f"{flow.__name__} should be async"

    @pytest.mark.asyncio
    async def test_flow_parameter_passing(self):
        """Test that flows properly pass parameters to underlying tasks."""
        with patch('src.flows.subflows.bottom_up_eps_validation_flow.bottom_up_eps_validation_cache_retrieval_task', return_value=None):
            with patch('src.flows.subflows.bottom_up_eps_validation_flow.bottom_up_eps_validation_task') as mock_task:
                with patch('src.flows.subflows.bottom_up_eps_validation_flow.update_job_status'):
                    mock_task.return_value = MagicMock(spec=BottomUpEpsValidation)

                    # Test with specific parameters
                    mock_financial_data = MagicMock()
                    mock_earnings_data = MagicMock()

                    await bottom_up_eps_validation_flow(
                        symbol="AAPL",
                        job_id="test-job-123",
                        financial_statements_data=mock_financial_data,
                        earnings_projections_data=mock_earnings_data,
                        consensus_eps=6.82
                    )

                    # Verify task was called with correct parameters
                    mock_task.assert_called_once()
                    call_kwargs = mock_task.call_args.kwargs
                    assert call_kwargs['symbol'] == "AAPL"
                    assert call_kwargs['financial_statements_data'] == mock_financial_data
                    assert call_kwargs['earnings_projections_data'] == mock_earnings_data
                    assert call_kwargs['consensus_eps'] == 6.82

    @pytest.mark.asyncio
    async def test_flow_cache_integration(self):
        """Test that flows properly integrate with caching system."""
        with patch('src.flows.subflows.bottom_up_eps_validation_flow.bottom_up_eps_validation_cache_retrieval_task') as mock_cache:
            with patch('src.flows.subflows.bottom_up_eps_validation_flow.bottom_up_eps_validation_task') as mock_task:
                with patch('src.flows.subflows.bottom_up_eps_validation_flow.update_job_status'):
                    cached_result = MagicMock(spec=BottomUpEpsValidation)
                    mock_cache.return_value = cached_result

                    result = await bottom_up_eps_validation_flow(
                        symbol="AAPL",
                        job_id="test-job-123",
                        force_recompute=False
                    )

                    # Verify cache was checked
                    mock_cache.assert_called_once_with("AAPL", False)
                    # Verify task was not called (cache hit)
                    mock_task.assert_not_called()
                    # Verify cached result was returned
                    assert result == cached_result