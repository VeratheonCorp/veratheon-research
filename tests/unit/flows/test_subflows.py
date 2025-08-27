import pytest
from unittest.mock import patch, AsyncMock
from src.flows.subflows.historical_earnings_flow import historical_earnings_flow
from src.flows.subflows.earnings_projections_flow import earnings_projections_flow
from src.flows.subflows.financial_statements_flow import financial_statements_flow
from src.flows.subflows.management_guidance_flow import management_guidance_flow
from src.research.historical_earnings.historical_earnings_models import (
    HistoricalEarningsData,
    HistoricalEarningsAnalysis
)
from src.research.earnings_projections.earnings_projections_models import (
    EarningsProjectionData,
    EarningsProjectionAnalysis,
    NextQuarterProjection
)
from src.research.financial_statements.financial_statements_models import (
    FinancialStatementsData,
    FinancialStatementsAnalysis
)
from src.research.management_guidance.management_guidance_models import (
    ManagementGuidanceData,
    ManagementGuidanceAnalysis
)


class TestHistoricalEarningsFlow:
    
    @patch('src.flows.subflows.historical_earnings_flow.publish_status_update_task')
    @patch('src.flows.subflows.historical_earnings_flow.historical_earnings_analysis_task')
    @patch('src.flows.subflows.historical_earnings_flow.historical_earnings_fetch_task')
    @pytest.mark.anyio
    async def test_historical_earnings_flow_success(
        self, 
        mock_fetch_task,
        mock_analysis_task,
        mock_publish_status_update_task
    ):
        """Test successful historical earnings flow execution."""
        
        # Mock fetch task result
        mock_data = HistoricalEarningsData(
            symbol="AAPL",
            quarterly_earnings=[{"fiscalDateEnding": "2023-12-31", "reportedEPS": "2.50"}],
            annual_earnings=[{"fiscalDateEnding": "2023-12-31", "reportedEPS": "10.00"}],
            income_statement=[{"fiscalDateEnding": "2023-12-31", "totalRevenue": "100000000"}]
        )
        mock_fetch_task.return_value = mock_data
        
        # Mock analysis task result
        mock_analysis = HistoricalEarningsAnalysis(
            symbol="AAPL",
            earnings_pattern="CONSISTENT_BEATS",
            earnings_pattern_details="Company consistently beats estimates by 5-10%",
            revenue_growth_trend="STABLE",
            revenue_growth_details="Revenue growth averaging 8-12% annually",
            margin_trend="IMPROVING",
            margin_trend_details="Operating margins expanding from 25% to 30%",
            key_insights=["Strong pricing power", "Operational efficiency gains"],
            analysis_confidence_score=85,
            predictability_score=90,
            full_analysis="Strong historical performance with consistent beats"
        )
        mock_analysis_task.return_value = mock_analysis
        
        # Mock status update task
        mock_publish_status_update_task.return_value = True
        
        # Execute the flow
        result = await historical_earnings_flow("AAPL")
        
        # Verify the result
        assert isinstance(result, HistoricalEarningsAnalysis)
        assert result.symbol == "AAPL"
        assert result.earnings_pattern == "CONSISTENT_BEATS"
        
        # Verify tasks were called correctly
        mock_fetch_task.assert_called_once_with("AAPL")
        mock_analysis_task.assert_called_once_with("AAPL", mock_data)
        
        # Verify status updates
        assert mock_publish_status_update_task.call_count == 2
        start_call = mock_publish_status_update_task.call_args_list[0]
        assert start_call[0][0] == "starting"
        assert start_call[0][1]["flow"] == "historical_earnings_flow"
        assert start_call[0][1]["symbol"] == "AAPL"


class TestEarningsProjectionsFlow:
    
    @patch('src.flows.subflows.earnings_projections_flow.publish_status_update_task')
    @patch('src.flows.subflows.earnings_projections_flow.earnings_projections_analysis_task')
    @patch('src.flows.subflows.earnings_projections_flow.earnings_projections_fetch_task')
    @pytest.mark.anyio
    async def test_earnings_projections_flow_success(
        self,
        mock_fetch_task,
        mock_analysis_task,
        mock_publish_status_update_task
    ):
        """Test successful earnings projections flow execution."""
        
        # Mock fetch task result
        mock_data = EarningsProjectionData(
            symbol="AAPL",
            quarterly_income_statements=[{"fiscalDateEnding": "2023-12-31", "totalRevenue": "50000000"}],
            annual_income_statements=[{"fiscalDateEnding": "2023-12-31", "totalRevenue": "200000000"}],
            consensus_estimates={"next_quarter_eps": "2.50", "next_quarter_revenue": "55000000"},
            historical_earnings_context=None,
            financial_statements_context=None
        )
        mock_fetch_task.return_value = mock_data
        
        # Mock analysis task result
        next_quarter = NextQuarterProjection(
            projected_eps=2.65,
            projected_revenue=56000000.0,
            consensus_eps_estimate=2.50,
            consensus_revenue_estimate=55000000.0,
            eps_vs_consensus_percent=6.0,
            revenue_vs_consensus_percent=1.8,
            confidence_level="HIGH"
        )
        mock_analysis = EarningsProjectionAnalysis(
            symbol="AAPL",
            next_quarter_projection=next_quarter,
            methodology_summary="Analysis based on revenue growth trends",
            key_assumptions=["Revenue growth continues", "Margins stable"],
            overall_confidence="HIGH"
        )
        mock_analysis_task.return_value = mock_analysis
        
        # Mock status update task
        mock_publish_status_update_task.return_value = True
        
        # Execute the flow with context
        historical_context = {"pattern": "CONSISTENT_BEATS"}
        financial_context = {"trend": "IMPROVING"}
        
        result = await earnings_projections_flow(
            "AAPL", 
            historical_context, 
            financial_context
        )
        
        # Verify the result
        assert isinstance(result, EarningsProjectionAnalysis)
        assert result.symbol == "AAPL"
        assert result.next_quarter_projection.projected_eps == 2.65
        assert result.overall_confidence == "HIGH"
        
        # Verify tasks were called correctly
        mock_fetch_task.assert_called_once_with("AAPL", historical_context, financial_context)
        mock_analysis_task.assert_called_once_with("AAPL", mock_data)
        
        # Verify status updates
        assert mock_publish_status_update_task.call_count == 2

    @patch('src.flows.subflows.earnings_projections_flow.publish_status_update_task')
    @patch('src.flows.subflows.earnings_projections_flow.earnings_projections_analysis_task')
    @patch('src.flows.subflows.earnings_projections_flow.earnings_projections_fetch_task')
    @pytest.mark.anyio
    async def test_earnings_projections_flow_no_context(
        self,
        mock_fetch_task,
        mock_analysis_task,
        mock_publish_status_update_task
    ):
        """Test earnings projections flow without historical context."""
        
        # Mock minimal fetch task result
        mock_data = EarningsProjectionData(
            symbol="AAPL",
            quarterly_income_statements=[],
            annual_income_statements=[],
            consensus_estimates={},
            historical_earnings_context=None,
            financial_statements_context=None
        )
        mock_fetch_task.return_value = mock_data
        
        # Mock minimal analysis task result
        next_quarter = NextQuarterProjection(
            projected_eps=2.50,
            projected_revenue=55000000.0,
            consensus_eps_estimate=None,
            consensus_revenue_estimate=None,
            eps_vs_consensus_percent=None,
            revenue_vs_consensus_percent=None,
            confidence_level="MEDIUM"
        )
        mock_analysis = EarningsProjectionAnalysis(
            symbol="AAPL",
            next_quarter_projection=next_quarter,
            methodology_summary="Limited data analysis",
            key_assumptions=["Basic financial trends"],
            overall_confidence="MEDIUM"
        )
        mock_analysis_task.return_value = mock_analysis
        
        # Mock status update task
        mock_publish_status_update_task.return_value = True
        
        # Execute the flow without context
        result = await earnings_projections_flow("AAPL")
        
        # Verify the result
        assert isinstance(result, EarningsProjectionAnalysis)
        assert result.symbol == "AAPL"
        assert result.overall_confidence == "MEDIUM"
        
        # Verify tasks were called with None context
        mock_fetch_task.assert_called_once_with("AAPL", None, None)


class TestFinancialStatementsFlow:
    
    @patch('src.flows.subflows.financial_statements_flow.publish_status_update_task')
    @patch('src.flows.subflows.financial_statements_flow.financial_statements_analysis_task')
    @patch('src.flows.subflows.financial_statements_flow.financial_statements_fetch_task')
    @pytest.mark.anyio
    async def test_financial_statements_flow_success(
        self,
        mock_fetch_task,
        mock_analysis_task,
        mock_publish_status_update_task
    ):
        """Test successful financial statements flow execution."""
        
        # Mock fetch task result
        mock_data = FinancialStatementsData(
            symbol="AAPL",
            income_statements=[{"fiscalDateEnding": "2023-12-31", "totalRevenue": "100000000", "netIncome": "20000000"}],
            balance_sheets=[{"fiscalDateEnding": "2023-12-31", "totalAssets": "500000000"}],
            cash_flow_statements=[{"fiscalDateEnding": "2023-12-31", "operatingCashflow": "30000000"}]
        )
        mock_fetch_task.return_value = mock_data
        
        # Mock analysis task result
        mock_analysis = FinancialStatementsAnalysis(
            symbol="AAPL",
            revenue_driver_trend="STRENGTHENING",
            revenue_driver_details="Product demand driving revenue growth",
            cost_structure_trend="IMPROVING_EFFICIENCY", 
            cost_structure_details="Operating leverage improving margins",
            working_capital_trend="IMPROVING_MANAGEMENT",
            working_capital_details="Efficient cash conversion cycle",
            key_financial_changes=["Revenue growth acceleration", "Margin expansion"],
            near_term_projection_risks=["Economic slowdown risk"],
            analysis_confidence_score=85,
            data_quality_score=90,
            full_analysis="Strong financial performance with improving trends"
        )
        mock_analysis_task.return_value = mock_analysis
        
        # Mock status update task
        mock_publish_status_update_task.return_value = True
        
        # Execute the flow
        result = await financial_statements_flow("AAPL")
        
        # Verify the result
        assert isinstance(result, FinancialStatementsAnalysis)
        assert result.symbol == "AAPL"
        assert result.revenue_driver_trend == "IMPROVING"
        
        # Verify tasks were called correctly
        mock_fetch_task.assert_called_once_with("AAPL")
        mock_analysis_task.assert_called_once_with("AAPL", mock_data)
        
        # Verify status updates
        assert mock_publish_status_update_task.call_count == 2


class TestManagementGuidanceFlow:
    
    @patch('src.flows.subflows.management_guidance_flow.publish_status_update_task')
    @patch('src.flows.subflows.management_guidance_flow.management_guidance_analysis_task')
    @patch('src.flows.subflows.management_guidance_flow.management_guidance_fetch_task')
    @pytest.mark.anyio
    async def test_management_guidance_flow_success(
        self,
        mock_fetch_task,
        mock_analysis_task,
        mock_publish_status_update_task
    ):
        """Test successful management guidance flow execution."""
        
        # Mock fetch task result
        mock_data = ManagementGuidanceData(
            symbol="AAPL",
            quarter="Q4",
            year="2023",
            earnings_transcript="Management provided positive guidance...",
            consensus_estimates={"next_quarter_eps": "2.50"}
        )
        mock_fetch_task.return_value = mock_data
        
        # Mock analysis task result
        mock_analysis = ManagementGuidanceAnalysis(
            symbol="AAPL",
            overall_guidance_tone="POSITIVE",
            consensus_validation_signal="CONFIRMS",
            guidance_summary="Strong forward guidance provided"
        )
        mock_analysis_task.return_value = mock_analysis
        
        # Mock status update task
        mock_publish_status_update_task.return_value = True
        
        # Mock context data
        historical_context = HistoricalEarningsAnalysis(
            symbol="AAPL",
            earnings_pattern="CONSISTENT_BEATS",
            revenue_growth_trend="STABLE",
            margin_trend="IMPROVING",
            analysis_summary="Strong performance"
        )
        financial_context = FinancialStatementsAnalysis(
            symbol="AAPL",
            revenue_driver_trend="IMPROVING",
            cost_structure_trend="STABLE",
            working_capital_trend="EFFICIENT",
            profitability_trends="IMPROVING",
            liquidity_assessment="STRONG",
            analysis_summary="Strong financials"
        )
        
        # Execute the flow
        result = await management_guidance_flow(
            "AAPL", 
            historical_context, 
            financial_context
        )
        
        # Verify the result
        assert isinstance(result, ManagementGuidanceAnalysis)
        assert result.symbol == "AAPL"
        assert result.overall_guidance_tone == "POSITIVE"
        
        # Verify tasks were called correctly
        mock_fetch_task.assert_called_once_with("AAPL")
        mock_analysis_task.assert_called_once_with(
            "AAPL", 
            mock_data,
            historical_context,
            financial_context
        )
        
        # Verify status updates
        assert mock_publish_status_update_task.call_count == 2