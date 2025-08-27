import pytest
from unittest.mock import patch
from src.tasks.trade_ideas.trade_ideas_task import trade_ideas_task
from src.research.forward_pe.forward_pe_models import ForwardPeValuation
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary
from src.research.trade_ideas.trade_idea_models import TradeIdea
from agents import RunResult


class TestTradeIdeasTask:
    
    @patch('src.tasks.trade_ideas.trade_ideas_task.Runner.run')
    @pytest.mark.anyio
    async def test_trade_ideas_task_success(self, mock_runner):
        """Test successful trade ideas generation."""
        # Mock forward PE valuation
        earnings_analysis = ForwardPeValuation(
            analysis="Trading below peer average with strong fundamentals. Forward PE of 25.0 vs peer average of 27.5 suggests undervaluation with target range $160-180.",
            analysis_confidence_score=85
        )
        
        # Mock news sentiment summary
        news_sentiment = NewsSentimentSummary(
            symbol="AAPL",
            news_sentiment_analysis="Strong positive sentiment driven by earnings beat and product demand. Market shows bullish outlook with improving trend.",
            overall_sentiment_label="Bullish"
        )
        
        # Mock the agent response
        mock_trade_idea = TradeIdea(
            high_level_trade_idea="BUY AAPL - Undervalued tech leader with strong fundamentals",
            reasoning="Trading below peer average with strong fundamentals and positive sentiment. Forward PE suggests undervaluation with bullish news sentiment supporting upside.",
            simple_equity_trade_specifics="Long AAPL at $150, target $175, stop loss $140, 3-6 month horizon",
            option_play="Buy AAPL Mar calls, strike $155, delta 0.65, for leveraged exposure",
            simple_equity_trade_specifics_confidence_score=85,
            option_play_confidence_score=75,
            risk_hedge="Consider position sizing at 3-5% of portfolio to manage single name risk"
        )
        
        # Mock the runner result
        mock_result = type('MockResult', (), {'final_output': mock_trade_idea})()
        mock_runner.return_value = mock_result
        
        result = await trade_ideas_task(
            "AAPL",
            earnings_analysis,
            news_sentiment,
            historical_earnings_analysis={"pattern": "CONSISTENT_BEATS"},
            financial_statements_analysis={"trend": "IMPROVING"},
            earnings_projections_analysis={"projected_eps": 2.65},
            management_guidance_analysis={"guidance_tone": "POSITIVE"}
        )
        
        assert isinstance(result, TradeIdea)
        assert "BUY AAPL" in result.high_level_trade_idea
        assert result.simple_equity_trade_specifics_confidence_score == 85
        assert result.option_play_confidence_score == 75
        assert "$175" in result.simple_equity_trade_specifics
        mock_runner.assert_called_once()

    @patch('src.tasks.trade_ideas.trade_ideas_task.Runner.run')
    @pytest.mark.anyio
    async def test_trade_ideas_task_minimal_context(self, mock_runner):
        """Test trade ideas generation with minimal context."""
        # Mock basic forward PE valuation
        earnings_analysis = ForwardPeValuation(
            analysis="Trading above peer average with fair valuation but some overvaluation concerns. Forward PE of 30.0 vs peer average of 27.5.",
            analysis_confidence_score=65
        )
        
        # Mock neutral news sentiment
        news_sentiment = NewsSentimentSummary(
            symbol="AAPL",
            news_sentiment_analysis="Neutral sentiment with general coverage showing no strong directional bias.",
            overall_sentiment_label="Neutral"
        )
        
        # Mock cautious trade idea
        mock_trade_idea = TradeIdea(
            high_level_trade_idea="HOLD AAPL - Overvalued but quality, wait for better entry",
            reasoning="Trading above peer average with neutral sentiment. Valuation stretched but quality company warrants patience for better entry point.",
            simple_equity_trade_specifics="Hold current position, consider adding below $140, target $145",
            option_play="Sell covered calls at $155 strike to generate income while waiting",
            simple_equity_trade_specifics_confidence_score=65,
            option_play_confidence_score=70,
            risk_hedge="Maintain small allocation (1-2% of portfolio) given valuation concerns"
        )
        
        # Mock the runner result
        mock_result = type('MockResult', (), {'final_output': mock_trade_idea})()
        mock_runner.return_value = mock_result
        
        result = await trade_ideas_task("AAPL", earnings_analysis, news_sentiment)
        
        assert isinstance(result, TradeIdea)
        assert "HOLD AAPL" in result.high_level_trade_idea
        assert result.simple_equity_trade_specifics_confidence_score == 65
        assert "better entry" in result.reasoning.lower()
        mock_runner.assert_called_once()

    @patch('src.tasks.trade_ideas.trade_ideas_task.Runner.run')
    @pytest.mark.anyio
    async def test_trade_ideas_task_negative_sentiment(self, mock_runner):
        """Test trade ideas generation with negative sentiment."""
        # Mock negative forward PE valuation
        earnings_analysis = ForwardPeValuation(
            analysis="Significantly overvalued with declining fundamentals. Forward PE of 35.0 vs peer average of 27.5 suggests major overvaluation with target $100-120.",
            analysis_confidence_score=80
        )
        
        # Mock negative news sentiment
        news_sentiment = NewsSentimentSummary(
            symbol="AAPL",
            news_sentiment_analysis="Negative sentiment driven by declining sales and competitive pressure. Market concerns about revenue decline and market share loss.",
            overall_sentiment_label="Bearish"
        )
        
        # Mock sell recommendation
        mock_trade_idea = TradeIdea(
            high_level_trade_idea="SELL AAPL - Overvalued with deteriorating fundamentals",
            reasoning="Significantly overvalued with declining fundamentals and negative sentiment. Multiple headwinds suggest further downside risk.",
            simple_equity_trade_specifics="Sell AAPL at current levels, target $110, stop loss $160",
            option_play="Buy AAPL puts, strike $140, 3-month expiry for hedging/shorting",
            simple_equity_trade_specifics_confidence_score=80,
            option_play_confidence_score=75,
            risk_hedge="Reduce or exit position entirely given deteriorating outlook"
        )
        
        # Mock the runner result
        mock_result = type('MockResult', (), {'final_output': mock_trade_idea})()
        mock_runner.return_value = mock_result
        
        result = await trade_ideas_task("AAPL", earnings_analysis, news_sentiment)
        
        assert isinstance(result, TradeIdea)
        assert "SELL AAPL" in result.high_level_trade_idea
        assert result.simple_equity_trade_specifics_confidence_score == 80
        assert "declining" in result.reasoning.lower()
        mock_runner.assert_called_once()