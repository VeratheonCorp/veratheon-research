import pytest
from unittest.mock import patch, MagicMock, AsyncMock
from src.tasks.eps_validation.bottom_up_eps_validation_task import bottom_up_eps_validation_task
from src.tasks.eps_validation.peer_relative_eps_validation_task import peer_relative_eps_validation_task
from src.tasks.eps_validation.market_sentiment_eps_check_task import market_sentiment_eps_check_task
from src.tasks.eps_validation.eps_validation_synthesis_task import eps_validation_synthesis_task
from src.research.eps_validation.eps_validation_models import (
    BottomUpEpsValidation,
    PeerRelativeEpsValidation,
    MarketSentimentEpsCheck,
    EpsValidationSynthesis,
    EpsValidationVerdict,
    ConfidenceLevel
)
from src.research.financial_statements.financial_statements_models import FinancialStatementsData, FinancialStatementsAnalysis
from src.research.earnings_projections.earnings_projections_models import EarningsProjectionData, EarningsProjectionAnalysis


class TestEpsValidationTasks:

    @pytest.mark.asyncio
    async def test_bottom_up_eps_validation_task_insufficient_data(self):
        """Test bottom-up EPS validation task with insufficient data."""
        result = await bottom_up_eps_validation_task(
            symbol="TEST",
            financial_statements_data=None,
            financial_statements_analysis=None,
            earnings_projections_data=None,
            earnings_projections_analysis=None,
            consensus_eps=5.0
        )

        assert isinstance(result, BottomUpEpsValidation)
        assert result.symbol == "TEST"
        assert result.validation_verdict == EpsValidationVerdict.INSUFFICIENT_DATA
        assert result.confidence_level == ConfidenceLevel.LOW
        assert result.consensus_eps == 5.0
        assert "Insufficient financial data" in result.key_assumptions[0]

    @pytest.mark.asyncio
    @patch('src.tasks.eps_validation.bottom_up_eps_validation_task.Runner')
    async def test_bottom_up_eps_validation_task_with_data(self, mock_runner, consensus_validated_bottom_up):
        """Test bottom-up EPS validation task with financial data."""
        # Mock the runner and its result
        mock_run_result = MagicMock()
        mock_run_result.success = True
        mock_run_result.data = consensus_validated_bottom_up
        mock_runner_instance = AsyncMock()
        mock_runner_instance.run.return_value = mock_run_result
        mock_runner.return_value = mock_runner_instance

        # Create mock financial data
        mock_financial_data = MagicMock(spec=FinancialStatementsData)
        mock_financial_analysis = MagicMock(spec=FinancialStatementsAnalysis)

        result = await bottom_up_eps_validation_task(
            symbol="AAPL",
            financial_statements_data=mock_financial_data,
            financial_statements_analysis=mock_financial_analysis,
            consensus_eps=6.82
        )

        assert isinstance(result, BottomUpEpsValidation)
        assert result.symbol == "AAPL"
        assert result.validation_verdict == EpsValidationVerdict.CONSENSUS_VALIDATED
        mock_runner_instance.run.assert_called_once()

    @pytest.mark.asyncio
    @patch('src.tasks.eps_validation.bottom_up_eps_validation_task.Runner')
    async def test_bottom_up_eps_validation_task_agent_failure(self, mock_runner):
        """Test bottom-up EPS validation task when agent fails."""
        # Mock the runner to return a failed result
        mock_run_result = MagicMock()
        mock_run_result.success = False
        mock_run_result.data = None
        mock_runner_instance = AsyncMock()
        mock_runner_instance.run.return_value = mock_run_result
        mock_runner.return_value = mock_runner_instance

        mock_financial_data = MagicMock(spec=FinancialStatementsData)

        result = await bottom_up_eps_validation_task(
            symbol="FAIL",
            financial_statements_data=mock_financial_data,
            consensus_eps=5.0
        )

        assert isinstance(result, BottomUpEpsValidation)
        assert result.symbol == "FAIL"
        assert result.validation_verdict == EpsValidationVerdict.INSUFFICIENT_DATA
        assert "Agent processing failed" in result.supporting_analysis

    @pytest.mark.asyncio
    async def test_peer_relative_eps_validation_task_insufficient_data(self):
        """Test peer-relative EPS validation task with insufficient data."""
        result = await peer_relative_eps_validation_task(
            symbol="TEST",
            current_stock_price=None,
            peer_group=None,
            consensus_eps=5.0
        )

        assert isinstance(result, PeerRelativeEpsValidation)
        assert result.symbol == "TEST"
        assert result.peer_comparison_verdict == EpsValidationVerdict.INSUFFICIENT_DATA
        assert result.consensus_eps == 5.0

    @pytest.mark.asyncio
    @patch('src.tasks.eps_validation.peer_relative_eps_validation_task.Runner')
    async def test_peer_relative_eps_validation_task_with_data(self, mock_runner, consensus_validated_peer_relative):
        """Test peer-relative EPS validation task with peer data."""
        # Mock the runner and its result
        mock_run_result = MagicMock()
        mock_run_result.success = True
        mock_run_result.data = consensus_validated_peer_relative
        mock_runner_instance = AsyncMock()
        mock_runner_instance.run.return_value = mock_run_result
        mock_runner.return_value = mock_runner_instance

        # Mock peer group data
        mock_peer_data = {
            "peer_group": [
                {"symbol": "MSFT", "forward_pe": 28.5},
                {"symbol": "GOOGL", "forward_pe": 22.1}
            ],
            "avg_forward_pe": 25.3
        }

        result = await peer_relative_eps_validation_task(
            symbol="AAPL",
            peer_group_data=mock_peer_data,
            current_stock_price=175.80,
            consensus_eps=6.82
        )

        assert isinstance(result, PeerRelativeEpsValidation)
        assert result.symbol == "AAPL"
        assert result.peer_comparison_verdict == EpsValidationVerdict.CONSENSUS_VALIDATED
        mock_runner_instance.run.assert_called_once()

    @pytest.mark.asyncio
    async def test_market_sentiment_eps_check_task_insufficient_data(self):
        """Test market sentiment EPS check task with insufficient data."""
        result = await market_sentiment_eps_check_task(
            symbol="TEST",
            news_sentiment_data=None,
            consensus_eps=5.0
        )

        assert isinstance(result, MarketSentimentEpsCheck)
        assert result.symbol == "TEST"
        assert result.sentiment_validation_verdict == EpsValidationVerdict.INSUFFICIENT_DATA

    @pytest.mark.asyncio
    @patch('src.tasks.eps_validation.market_sentiment_eps_check_task.Runner')
    async def test_market_sentiment_eps_check_task_with_data(self, mock_runner, upward_momentum_sentiment):
        """Test market sentiment EPS check task with sentiment data."""
        # Mock the runner and its result
        mock_run_result = MagicMock()
        mock_run_result.success = True
        mock_run_result.data = upward_momentum_sentiment
        mock_runner_instance = AsyncMock()
        mock_runner_instance.run.return_value = mock_run_result
        mock_runner.return_value = mock_runner_instance

        # Mock sentiment data
        mock_sentiment_data = {
            "sentiment_score": 0.8,
            "recent_news": ["Positive earnings guidance", "Strong Q3 results"],
            "analyst_revisions": ["Upgrade from Morgan Stanley", "Price target increase"]
        }

        result = await market_sentiment_eps_check_task(
            symbol="NVDA",
            news_sentiment_data=mock_sentiment_data,
            consensus_eps=10.45
        )

        assert isinstance(result, MarketSentimentEpsCheck)
        assert result.symbol == "NVDA"
        assert result.sentiment_validation_verdict == EpsValidationVerdict.CONSENSUS_TOO_LOW
        mock_runner_instance.run.assert_called_once()

    @pytest.mark.asyncio
    async def test_eps_validation_synthesis_task_no_validation_results(self):
        """Test EPS validation synthesis task with no validation results."""
        result = await eps_validation_synthesis_task(
            symbol="TEST",
            bottom_up_validation=None,
            peer_relative_validation=None,
            sentiment_validation=None
        )

        assert isinstance(result, EpsValidationSynthesis)
        assert result.symbol == "TEST"
        assert result.overall_verdict == EpsValidationVerdict.INSUFFICIENT_DATA
        assert result.confidence_score == 0.0

    @pytest.mark.asyncio
    @patch('src.tasks.eps_validation.eps_validation_synthesis_task.Runner')
    async def test_eps_validation_synthesis_task_with_validation_results(
        self,
        mock_runner,
        consensus_validated_synthesis,
        consensus_validated_bottom_up,
        consensus_validated_peer_relative,
        stable_momentum_sentiment
    ):
        """Test EPS validation synthesis task with validation results."""
        # Mock the runner and its result
        mock_run_result = MagicMock()
        mock_run_result.success = True
        mock_run_result.data = consensus_validated_synthesis
        mock_runner_instance = AsyncMock()
        mock_runner_instance.run.return_value = mock_run_result
        mock_runner.return_value = mock_runner_instance

        result = await eps_validation_synthesis_task(
            symbol="AAPL",
            bottom_up_validation=consensus_validated_bottom_up,
            peer_relative_validation=consensus_validated_peer_relative,
            sentiment_validation=stable_momentum_sentiment
        )

        assert isinstance(result, EpsValidationSynthesis)
        assert result.symbol == "AAPL"
        assert result.overall_verdict == EpsValidationVerdict.CONSENSUS_VALIDATED
        assert result.confidence_score == 0.85
        mock_runner_instance.run.assert_called_once()

    @pytest.mark.asyncio
    async def test_eps_validation_synthesis_task_mixed_results(
        self,
        consensus_too_high_bottom_up,
        consensus_validated_peer_relative,
        upward_momentum_sentiment
    ):
        """Test EPS validation synthesis task with mixed validation results."""
        result = await eps_validation_synthesis_task(
            symbol="MIXED",
            bottom_up_validation=consensus_too_high_bottom_up,
            peer_relative_validation=consensus_validated_peer_relative,
            sentiment_validation=upward_momentum_sentiment
        )

        assert isinstance(result, EpsValidationSynthesis)
        assert result.symbol == "MIXED"
        # When only one method suggests consensus is too high, synthesis should be more cautious
        assert result.confidence_score < 0.7  # Lower confidence due to mixed signals

    @pytest.mark.asyncio
    @patch('src.tasks.eps_validation.eps_validation_synthesis_task.Runner')
    async def test_eps_validation_synthesis_task_agent_failure(self, mock_runner):
        """Test EPS validation synthesis task when agent fails."""
        # Mock the runner to return a failed result
        mock_run_result = MagicMock()
        mock_run_result.success = False
        mock_run_result.data = None
        mock_runner_instance = AsyncMock()
        mock_runner_instance.run.return_value = mock_run_result
        mock_runner.return_value = mock_runner_instance

        mock_validation = MagicMock(spec=BottomUpEpsValidation)

        result = await eps_validation_synthesis_task(
            symbol="FAIL",
            bottom_up_validation=mock_validation,
            peer_relative_validation=None,
            sentiment_validation=None
        )

        assert isinstance(result, EpsValidationSynthesis)
        assert result.symbol == "FAIL"
        assert result.overall_verdict == EpsValidationVerdict.INSUFFICIENT_DATA
        assert "Synthesis agent processing failed" in result.synthesis_analysis

    def test_task_function_signatures(self):
        """Test that all task functions have the expected signatures."""
        import inspect

        # Check bottom_up_eps_validation_task signature
        sig = inspect.signature(bottom_up_eps_validation_task)
        assert 'symbol' in sig.parameters
        assert 'financial_statements_data' in sig.parameters
        assert 'consensus_eps' in sig.parameters

        # Check peer_relative_eps_validation_task signature
        sig = inspect.signature(peer_relative_eps_validation_task)
        assert 'symbol' in sig.parameters
        assert 'peer_group_data' in sig.parameters
        assert 'current_stock_price' in sig.parameters

        # Check market_sentiment_eps_check_task signature
        sig = inspect.signature(market_sentiment_eps_check_task)
        assert 'symbol' in sig.parameters
        assert 'news_sentiment_data' in sig.parameters

        # Check eps_validation_synthesis_task signature
        sig = inspect.signature(eps_validation_synthesis_task)
        assert 'symbol' in sig.parameters
        assert 'bottom_up_validation' in sig.parameters
        assert 'peer_relative_validation' in sig.parameters
        assert 'sentiment_validation' in sig.parameters

    def test_all_tasks_are_async(self):
        """Test that all task functions are async."""
        import inspect

        tasks = [
            bottom_up_eps_validation_task,
            peer_relative_eps_validation_task,
            market_sentiment_eps_check_task,
            eps_validation_synthesis_task
        ]

        for task in tasks:
            assert inspect.iscoroutinefunction(task), f"{task.__name__} should be async"