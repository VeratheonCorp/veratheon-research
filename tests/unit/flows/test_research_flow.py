import pytest
from unittest.mock import patch, AsyncMock
from src.flows.research_flow import main_research_flow
from src.research.historical_earnings.historical_earnings_models import HistoricalEarningsAnalysis
from src.research.financial_statements.financial_statements_models import FinancialStatementsAnalysis
from src.research.earnings_projections.earnings_projections_models import (
    EarningsProjectionAnalysis,
    NextQuarterProjection
)
from src.research.management_guidance.management_guidance_models import ManagementGuidanceAnalysis
from src.research.forward_pe.forward_pe_models import ForwardPeValuation, ForwardPeSanityCheck
from src.research.news_sentiment.news_sentiment_models import NewsSentimentSummary
from src.research.trade_ideas.trade_idea_models import TradeIdea
from src.research.common.models.peer_group import PeerGroup


class TestMainResearchFlow:
    
    @patch('src.flows.research_flow.publish_status_update_task')
    @patch('src.flows.research_flow.trade_ideas_flow')
    @patch('src.flows.research_flow.news_sentiment_flow')
    @patch('src.flows.research_flow.forward_pe_flow')
    @patch('src.flows.research_flow.forward_pe_sanity_check_flow')
    @patch('src.flows.research_flow.peer_group_agent')
    @patch('src.flows.research_flow.management_guidance_flow')
    @patch('src.flows.research_flow.earnings_projections_flow')
    @patch('src.flows.research_flow.financial_statements_flow')
    @patch('src.flows.research_flow.historical_earnings_flow')
    @pytest.mark.anyio
    async def test_main_research_flow_success(
        self,
        mock_historical_earnings_flow,
        mock_financial_statements_flow,
        mock_earnings_projections_flow,
        mock_management_guidance_flow,
        mock_peer_group_agent,
        mock_forward_pe_sanity_check_flow,
        mock_forward_pe_flow,
        mock_news_sentiment_flow,
        mock_trade_ideas_flow,
        mock_publish_status_update_task
    ):
        """Test successful execution of the complete main research flow."""
        
        # Mock historical earnings analysis
        mock_historical = HistoricalEarningsAnalysis(
            symbol="AAPL",
            earnings_pattern="CONSISTENT_BEATS",
            revenue_growth_trend="STABLE",
            margin_trend="IMPROVING",
            analysis_summary="Strong historical performance"
        )
        mock_historical_earnings_flow.return_value = mock_historical
        
        # Mock financial statements analysis  
        mock_financial = FinancialStatementsAnalysis(
            symbol="AAPL",
            revenue_driver_trend="IMPROVING",
            cost_structure_trend="STABLE", 
            working_capital_trend="EFFICIENT",
            profitability_trends="IMPROVING",
            liquidity_assessment="STRONG",
            analysis_summary="Strong financial performance"
        )
        mock_financial_statements_flow.return_value = mock_financial
        
        # Mock earnings projections analysis
        next_quarter = NextQuarterProjection(
            projected_eps=2.65,
            projected_revenue=56000000.0,
            consensus_eps_estimate=2.50,
            consensus_revenue_estimate=55000000.0,
            eps_vs_consensus_percent=6.0,
            revenue_vs_consensus_percent=1.8,
            confidence_level="HIGH"
        )
        mock_projections = EarningsProjectionAnalysis(
            symbol="AAPL",
            next_quarter_projection=next_quarter,
            methodology_summary="Analysis based on revenue growth trends",
            key_assumptions=["Revenue growth continues", "Margins stable"],
            overall_confidence="HIGH"
        )
        mock_earnings_projections_flow.return_value = mock_projections
        
        # Mock management guidance analysis
        mock_guidance = ManagementGuidanceAnalysis(
            symbol="AAPL",
            overall_guidance_tone="POSITIVE",
            consensus_validation_signal="CONFIRMS",
            guidance_summary="Strong forward guidance provided"
        )
        mock_management_guidance_flow.return_value = mock_guidance
        
        # Mock peer group
        mock_peers = PeerGroup(
            symbol="AAPL",
            peer_symbols=["MSFT", "GOOGL", "AMZN"],
            reasoning="Technology companies with similar market cap",
            industry_sector="Technology"
        )
        mock_peer_group_agent.return_value = mock_peers
        
        # Mock forward PE sanity check
        mock_sanity = ForwardPeSanityCheck(
            symbol="AAPL",
            data_quality="HIGH",
            earnings_consistency="CONSISTENT", 
            pe_reasonableness="REASONABLE",
            red_flags=[],
            confidence_score=0.85,
            overall_assessment="Data appears reliable"
        )
        mock_forward_pe_sanity_check_flow.return_value = mock_sanity
        
        # Mock forward PE valuation
        mock_pe_valuation = ForwardPeValuation(
            symbol="AAPL",
            forward_pe_ratio=25.0,
            peer_avg_pe=27.5,
            relative_valuation="UNDERVALUED",
            valuation_summary="Trading below peer average",
            target_price_range={"low": 160.0, "high": 180.0},
            confidence_level="HIGH"
        )
        mock_forward_pe_flow.return_value = mock_pe_valuation
        
        # Mock news sentiment summary
        mock_sentiment = NewsSentimentSummary(
            symbol="AAPL",
            overall_sentiment="POSITIVE",
            sentiment_score=0.75,
            key_themes=["Strong earnings", "Product demand"],
            positive_factors=["Revenue growth"],
            negative_factors=["Supply chain concerns"],
            sentiment_trend="IMPROVING",
            impact_on_price="BULLISH"
        )
        mock_news_sentiment_flow.return_value = mock_sentiment
        
        # Mock trade ideas
        mock_trade_idea = TradeIdea(
            symbol="AAPL",
            recommendation="BUY",
            confidence_level="HIGH",
            target_price=175.0,
            stop_loss=140.0,
            time_horizon="3-6 months",
            investment_thesis="Undervalued with strong fundamentals",
            key_catalysts=["Upcoming earnings", "Product launches"],
            risk_factors=["Market volatility"],
            position_sizing="Medium allocation"
        )
        mock_trade_ideas_flow.return_value = mock_trade_idea
        
        # Mock status update task
        mock_publish_status_update_task.return_value = True
        
        # Execute the main research flow
        result = await main_research_flow("AAPL")
        
        # Verify the result
        assert isinstance(result, TradeIdea)
        assert result.symbol == "AAPL"
        assert result.recommendation == "BUY"
        assert result.confidence_level == "HIGH"
        
        # Verify all flows were called in the correct order
        mock_historical_earnings_flow.assert_called_once_with("AAPL")
        mock_financial_statements_flow.assert_called_once_with("AAPL")
        mock_earnings_projections_flow.assert_called_once_with(
            "AAPL", 
            mock_historical.model_dump(),
            mock_financial.model_dump()
        )
        mock_management_guidance_flow.assert_called_once_with(
            "AAPL",
            mock_historical,
            mock_financial
        )
        mock_peer_group_agent.assert_called_once_with("AAPL", mock_financial)
        mock_forward_pe_sanity_check_flow.assert_called_once_with("AAPL")
        mock_forward_pe_flow.assert_called_once_with(
            "AAPL",
            mock_peers,
            mock_projections,
            mock_guidance,
            mock_sanity
        )
        mock_news_sentiment_flow.assert_called_once_with(
            "AAPL",
            mock_peers,
            mock_projections,
            mock_guidance
        )
        mock_trade_ideas_flow.assert_called_once_with(
            "AAPL",
            mock_pe_valuation,
            mock_sentiment,
            mock_historical,
            mock_financial,
            mock_projections,
            mock_guidance
        )
        
        # Verify status updates were published
        assert mock_publish_status_update_task.call_count == 2
        
        # Check starting status update
        start_call = mock_publish_status_update_task.call_args_list[0]
        assert start_call[0][0] == "starting"
        assert start_call[0][1]["flow"] == "main_research_flow"
        assert start_call[0][1]["symbol"] == "AAPL"
        
        # Check completion status update
        end_call = mock_publish_status_update_task.call_args_list[1]
        assert end_call[0][0] == "completed"
        assert end_call[0][1]["flow"] == "main_research_flow"
        assert end_call[0][1]["symbol"] == "AAPL"
        assert "duration_seconds" in end_call[0][1]

    @patch('src.flows.research_flow.publish_status_update_task')
    @patch('src.flows.research_flow.historical_earnings_flow')
    @pytest.mark.anyio
    async def test_main_research_flow_early_failure(
        self,
        mock_historical_earnings_flow,
        mock_publish_status_update_task
    ):
        """Test main research flow behavior when an early step fails."""
        
        # Mock status update task
        mock_publish_status_update_task.return_value = True
        
        # Mock historical earnings flow to raise an exception
        mock_historical_earnings_flow.side_effect = Exception("Historical earnings data unavailable")
        
        # Execute the main research flow and expect it to fail
        with pytest.raises(Exception, match="Historical earnings data unavailable"):
            await main_research_flow("INVALID")
        
        # Verify the starting status update was published
        mock_publish_status_update_task.assert_called_once_with(
            "starting", 
            {"flow": "main_research_flow", "symbol": "INVALID"}
        )
        
        # Verify historical earnings flow was attempted
        mock_historical_earnings_flow.assert_called_once_with("INVALID")