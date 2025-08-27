import pytest
from unittest.mock import patch
from src.tasks.news_sentiment.news_sentiment_fetch_summaries_task import news_sentiment_fetch_summaries_task
from src.tasks.news_sentiment.news_sentiment_analysis_task import news_sentiment_analysis_task
from src.research.news_sentiment.news_sentiment_models import (
    RawNewsSentimentSummary, 
    RawNewsSentimentFeed,
    NewsSentimentSummary
)
from agents import RunResult


class TestNewsSentimentFetchSummariesTask:
    
    @patch('src.tasks.news_sentiment.news_sentiment_fetch_summaries_task.get_news_sentiment_summary_for_peer_group')
    @pytest.mark.anyio
    async def test_news_sentiment_fetch_summaries_task_success(self, mock_get_summaries):
        """Test successful news sentiment summaries fetch."""
        # Mock the utility function response
        mock_summaries = [
            RawNewsSentimentSummary(
                feed=[
                    RawNewsSentimentFeed(
                        overall_sentiment_score=0.7,
                        overall_sentiment_label="Bullish",
                        ticker_sentiment=[{"ticker": "AAPL", "relevance_score": "0.9", "ticker_sentiment_score": "0.8", "ticker_sentiment_label": "Bullish"}]
                    )
                ]
            ),
            RawNewsSentimentSummary(
                feed=[
                    RawNewsSentimentFeed(
                        overall_sentiment_score=0.6,
                        overall_sentiment_label="Bullish",
                        ticker_sentiment=[{"ticker": "MSFT", "relevance_score": "0.85", "ticker_sentiment_score": "0.65", "ticker_sentiment_label": "Bullish"}]
                    )
                ]
            )
        ]
        mock_get_summaries.return_value = mock_summaries
        
        result = await news_sentiment_fetch_summaries_task("AAPL", ["MSFT", "GOOGL"])
        
        assert isinstance(result, list)
        assert len(result) == 2
        assert len(result[0].feed) == 1
        assert result[0].feed[0].overall_sentiment_label == "Bullish"
        assert len(result[1].feed) == 1
        assert result[1].feed[0].overall_sentiment_label == "Bullish"
        # Note: the task appends the symbol to peer_group, so final call includes AAPL
        mock_get_summaries.assert_called_once_with(["MSFT", "GOOGL", "AAPL"])

    @patch('src.tasks.news_sentiment.news_sentiment_fetch_summaries_task.get_news_sentiment_summary_for_peer_group')
    @pytest.mark.anyio
    async def test_news_sentiment_fetch_summaries_task_empty_peers(self, mock_get_summaries):
        """Test news sentiment fetch with empty peer group."""
        mock_summaries = [
            RawNewsSentimentSummary(
                feed=[
                    RawNewsSentimentFeed(
                        overall_sentiment_score=0.5,
                        overall_sentiment_label="Neutral",
                        ticker_sentiment=[{"ticker": "AAPL", "relevance_score": "0.8", "ticker_sentiment_score": "0.5", "ticker_sentiment_label": "Neutral"}]
                    )
                ]
            )
        ]
        mock_get_summaries.return_value = mock_summaries
        
        result = await news_sentiment_fetch_summaries_task("AAPL", [])
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert len(result[0].feed) == 1
        assert result[0].feed[0].overall_sentiment_label == "Neutral"
        # Even with empty peer group, symbol should be added
        mock_get_summaries.assert_called_once_with(["AAPL"])


class TestNewsSentimentAnalysisTask:
    
    @patch('src.tasks.news_sentiment.news_sentiment_analysis_task.Runner.run')
    @pytest.mark.anyio
    async def test_news_sentiment_analysis_task_success(self, mock_runner):
        """Test successful news sentiment analysis."""
        # Mock raw news sentiment summaries
        raw_summaries = [
            RawNewsSentimentSummary(
                feed=[
                    RawNewsSentimentFeed(
                        overall_sentiment_score=0.8,
                        overall_sentiment_label="Bullish",
                        ticker_sentiment=[{"ticker": "AAPL", "relevance_score": "0.9", "ticker_sentiment_score": "0.85", "ticker_sentiment_label": "Bullish"}]
                    )
                ]
            )
        ]
        
        # Mock the agent response
        mock_sentiment = NewsSentimentSummary(
            symbol="AAPL",
            news_sentiment_analysis="Strong positive sentiment driven by earnings beat and product demand. Market shows bullish outlook on company fundamentals.",
            overall_sentiment_label="Bullish"
        )
        
        # Mock the runner result
        mock_result = type('MockResult', (), {'final_output': mock_sentiment})()
        mock_runner.return_value = mock_result
        
        result = await news_sentiment_analysis_task(
            "AAPL", 
            raw_summaries,
            earnings_projections_analysis={"projected_eps": 2.65},
            management_guidance_analysis={"guidance_tone": "POSITIVE"}
        )
        
        assert isinstance(result, NewsSentimentSummary)
        assert result.symbol == "AAPL"
        assert result.overall_sentiment_label == "Bullish"
        assert "positive sentiment" in result.news_sentiment_analysis
        mock_runner.assert_called_once()

    @patch('src.tasks.news_sentiment.news_sentiment_analysis_task.Runner.run')
    @pytest.mark.anyio
    async def test_news_sentiment_analysis_task_no_context(self, mock_runner):
        """Test news sentiment analysis without additional context."""
        raw_summaries = [
            RawNewsSentimentSummary(
                feed=[
                    RawNewsSentimentFeed(
                        overall_sentiment_score=0.5,
                        overall_sentiment_label="Neutral",
                        ticker_sentiment=[{"ticker": "AAPL", "relevance_score": "0.7", "ticker_sentiment_score": "0.5", "ticker_sentiment_label": "Neutral"}]
                    )
                ]
            )
        ]
        
        mock_sentiment = NewsSentimentSummary(
            symbol="AAPL",
            news_sentiment_analysis="Neutral sentiment with general coverage showing no strong directional bias.",
            overall_sentiment_label="Neutral"
        )
        
        # Mock the runner result
        mock_result = type('MockResult', (), {'final_output': mock_sentiment})()
        mock_runner.return_value = mock_result
        
        result = await news_sentiment_analysis_task("AAPL", raw_summaries)
        
        assert isinstance(result, NewsSentimentSummary)
        assert result.symbol == "AAPL"
        assert result.overall_sentiment_label == "Neutral"
        assert "Neutral sentiment" in result.news_sentiment_analysis
        mock_runner.assert_called_once()