import pytest
from unittest.mock import patch, MagicMock
from src.research.eps_validation.bottom_up_eps_validation_agent import bottom_up_eps_validation_agent
from src.research.eps_validation.peer_relative_eps_validation_agent import peer_relative_eps_validation_agent
from src.research.eps_validation.market_sentiment_eps_check_agent import market_sentiment_eps_check_agent
from src.research.eps_validation.eps_validation_synthesis_agent import eps_validation_synthesis_agent
from src.research.eps_validation.eps_validation_models import (
    BottomUpEpsValidation,
    PeerRelativeEpsValidation,
    MarketSentimentEpsCheck,
    EpsValidationSynthesis,
    EpsValidationVerdict,
    ConfidenceLevel
)


class TestEpsValidationAgents:

    @patch('src.lib.llm_model.get_model')
    def test_bottom_up_eps_validation_agent_creation(self, mock_get_model):
        """Test that bottom-up EPS validation agent is properly configured."""
        mock_get_model.return_value = MagicMock()

        agent = bottom_up_eps_validation_agent

        assert agent.name == "Bottom-Up EPS Validation Analyst"
        assert agent.output_type == BottomUpEpsValidation
        assert "Reconstruct EPS from financial fundamentals" in agent.instructions

    @patch('src.lib.llm_model.get_model')
    def test_peer_relative_eps_validation_agent_creation(self, mock_get_model):
        """Test that peer-relative EPS validation agent is properly configured."""
        mock_get_model.return_value = MagicMock()

        agent = peer_relative_eps_validation_agent

        assert agent.name == "Peer-Relative EPS Validation Analyst"
        assert agent.output_type == PeerRelativeEpsValidation
        assert "peer group forward P/E ratios" in agent.instructions

    @patch('src.lib.llm_model.get_model')
    def test_market_sentiment_eps_check_agent_creation(self, mock_get_model):
        """Test that market sentiment EPS check agent is properly configured."""
        mock_get_model.return_value = MagicMock()

        agent = market_sentiment_eps_check_agent

        assert agent.name == "Market Sentiment EPS Check Analyst"
        assert agent.output_type == MarketSentimentEpsCheck
        assert "revision trends, and whisper numbers" in agent.instructions

    @patch('src.lib.llm_model.get_model')
    def test_eps_validation_synthesis_agent_creation(self, mock_get_model):
        """Test that EPS validation synthesis agent is properly configured."""
        mock_get_model.return_value = MagicMock()

        agent = eps_validation_synthesis_agent

        assert agent.name == "EPS Validation Synthesis Analyst"
        assert agent.output_type == EpsValidationSynthesis
        assert "Synthesize results from multiple EPS validation methods" in agent.instructions

    def test_bottom_up_agent_instructions_contain_required_elements(self):
        """Test that bottom-up agent instructions contain all required analysis elements."""
        instructions = bottom_up_eps_validation_agent.instructions

        # Check for required analysis components
        assert "Revenue projections" in instructions
        assert "Gross margin analysis" in instructions
        assert "Operating expense trends" in instructions
        assert "Tax rate assumptions" in instructions
        assert "Share count" in instructions

        # Check for validation methodology
        assert "VALIDATION METHODOLOGY" in instructions
        assert "variance percentage" in instructions
        assert "confidence level" in instructions

        # Check for enum requirements
        assert "ConfidenceLevel" in instructions
        assert "EpsValidationVerdict" in instructions

    def test_peer_relative_agent_instructions_contain_required_elements(self):
        """Test that peer-relative agent instructions contain all required analysis elements."""
        instructions = peer_relative_eps_validation_agent.instructions

        # Check for required analysis components
        assert "peer group" in instructions
        assert "forward P/E" in instructions
        assert "implied EPS" in instructions
        assert "stock price" in instructions

        # Check for validation methodology
        assert "ANALYSIS METHODOLOGY" in instructions
        assert "peer average P/E" in instructions

    def test_market_sentiment_agent_instructions_contain_required_elements(self):
        """Test that market sentiment agent instructions contain all required analysis elements."""
        instructions = market_sentiment_eps_check_agent.instructions

        # Check for required analysis components
        assert "revision momentum" in instructions or "REVISION MOMENTUM" in instructions
        assert "sentiment" in instructions
        assert "whisper numbers" in instructions
        assert "revisions" in instructions

        # Check for enum requirements
        assert "RevisionMomentum" in instructions
        assert "SentimentAlignment" in instructions

    def test_synthesis_agent_instructions_contain_required_elements(self):
        """Test that synthesis agent instructions contain all required analysis elements."""
        instructions = eps_validation_synthesis_agent.instructions

        # Check for synthesis methodology
        assert "validation methods" in instructions
        assert "overall_verdict" in instructions
        assert "confidence" in instructions
        assert "investment" in instructions

        # Check for decision making logic
        assert "SYNTHESIS METHODOLOGY" in instructions
        assert "VERDICT DETERMINATION" in instructions

    def test_all_agents_have_proper_names(self):
        """Test that all agents have descriptive, professional names."""
        agents = [
            bottom_up_eps_validation_agent,
            peer_relative_eps_validation_agent,
            market_sentiment_eps_check_agent,
            eps_validation_synthesis_agent
        ]

        for agent in agents:
            assert agent.name is not None
            assert len(agent.name) > 10  # Should be descriptive
            assert "Analyst" in agent.name  # Should indicate analyst role

    def test_all_agents_have_proper_output_types(self):
        """Test that all agents have the correct output types configured."""
        assert bottom_up_eps_validation_agent.output_type == BottomUpEpsValidation
        assert peer_relative_eps_validation_agent.output_type == PeerRelativeEpsValidation
        assert market_sentiment_eps_check_agent.output_type == MarketSentimentEpsCheck
        assert eps_validation_synthesis_agent.output_type == EpsValidationSynthesis

    def test_agent_instructions_contain_enum_requirements(self):
        """Test that agent instructions properly specify enum requirements."""
        agents_and_expected_enums = [
            (bottom_up_eps_validation_agent, ["ConfidenceLevel", "EpsValidationVerdict"]),
            (peer_relative_eps_validation_agent, ["EpsValidationVerdict"]),
            (market_sentiment_eps_check_agent, ["RevisionMomentum", "SentimentAlignment", "EpsValidationVerdict"]),
            (eps_validation_synthesis_agent, ["EpsValidationVerdict"])
        ]

        for agent, expected_enums in agents_and_expected_enums:
            for enum_name in expected_enums:
                assert enum_name in agent.instructions, f"Agent {agent.name} missing {enum_name} in instructions"

    def test_agents_use_model_from_get_model(self):
        """Test that all agents are configured to use the model from get_model()."""
        # This test ensures that the agents are using the centralized model configuration
        # We can't directly test the model without mocking, but we can verify the pattern
        agents = [
            bottom_up_eps_validation_agent,
            peer_relative_eps_validation_agent,
            market_sentiment_eps_check_agent,
            eps_validation_synthesis_agent
        ]

        for agent in agents:
            # Verify that agent has a model attribute (this confirms it was configured)
            assert hasattr(agent, 'model')
            assert agent.model is not None