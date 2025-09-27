import pytest
from pydantic import ValidationError
from src.research.eps_validation.eps_validation_models import (
    BottomUpEpsValidation,
    PeerRelativeEpsValidation,
    MarketSentimentEpsCheck,
    EpsValidationSynthesis,
    EpsValidationVerdict,
    RevisionMomentum,
    ConfidenceLevel,
    SentimentAlignment
)


class TestEpsValidationModels:

    def test_bottom_up_eps_validation_creation(self, consensus_validated_bottom_up):
        """Test that BottomUpEpsValidation model can be created with valid data."""
        validation = consensus_validated_bottom_up

        assert validation.symbol == "AAPL"
        assert validation.independent_eps_estimate == 6.85
        assert validation.consensus_eps == 6.82
        assert validation.variance_percentage == 0.44
        assert validation.confidence_level == ConfidenceLevel.HIGH
        assert validation.validation_verdict == EpsValidationVerdict.CONSENSUS_VALIDATED
        assert len(validation.key_assumptions) == 3
        assert len(validation.risk_factors) == 2

    def test_bottom_up_eps_validation_required_fields(self):
        """Test that BottomUpEpsValidation requires all mandatory fields."""
        with pytest.raises(ValidationError):
            BottomUpEpsValidation()

        with pytest.raises(ValidationError):
            BottomUpEpsValidation(symbol="AAPL")

    def test_peer_relative_eps_validation_creation(self, consensus_validated_peer_relative):
        """Test that PeerRelativeEpsValidation model can be created with valid data."""
        validation = consensus_validated_peer_relative

        assert validation.symbol == "AAPL"
        assert validation.peer_group_avg_forward_pe == 25.3
        assert validation.current_stock_price == 175.80
        assert validation.implied_eps_from_peers == 6.95
        assert validation.consensus_eps == 6.82
        assert validation.relative_variance == 1.91
        assert validation.peer_comparison_verdict == EpsValidationVerdict.CONSENSUS_VALIDATED

    def test_peer_relative_eps_validation_calculations(self):
        """Test that peer-relative calculations are consistent."""
        validation = PeerRelativeEpsValidation(
            symbol="TEST",
            peer_group_avg_forward_pe=20.0,
            current_stock_price=100.0,
            implied_eps_from_peers=5.0,  # 100 / 20
            consensus_eps=4.5,
            relative_variance=11.11,  # (5.0 - 4.5) / 4.5 * 100
            peer_comparison_verdict=EpsValidationVerdict.CONSENSUS_TOO_LOW,
            peer_analysis="Test analysis",
            industry_context="Test context"
        )

        # Verify the implied EPS calculation is consistent
        calculated_implied_eps = validation.current_stock_price / validation.peer_group_avg_forward_pe
        assert abs(calculated_implied_eps - validation.implied_eps_from_peers) < 0.01

    def test_market_sentiment_eps_check_creation(self, upward_momentum_sentiment):
        """Test that MarketSentimentEpsCheck model can be created with valid data."""
        sentiment = upward_momentum_sentiment

        assert sentiment.symbol == "NVDA"
        assert sentiment.revision_momentum == RevisionMomentum.UPWARD
        assert sentiment.sentiment_eps_alignment == SentimentAlignment.BULLISH
        assert sentiment.whisper_vs_consensus == 1.25
        assert sentiment.sentiment_validation_verdict == EpsValidationVerdict.CONSENSUS_TOO_LOW
        assert len(sentiment.sentiment_insights) == 3

    def test_market_sentiment_optional_whisper(self):
        """Test that whisper_vs_consensus is optional."""
        sentiment = MarketSentimentEpsCheck(
            symbol="TEST",
            revision_momentum=RevisionMomentum.STABLE,
            sentiment_eps_alignment=SentimentAlignment.NEUTRAL,
            whisper_vs_consensus=None,  # Optional field
            sentiment_validation_verdict=EpsValidationVerdict.CONSENSUS_VALIDATED,
            revision_analysis="Test analysis",
            market_expectation_summary="Test summary"
        )

        assert sentiment.whisper_vs_consensus is None

    def test_eps_validation_synthesis_creation(self, consensus_validated_synthesis):
        """Test that EpsValidationSynthesis model can be created with valid data."""
        synthesis = consensus_validated_synthesis

        assert synthesis.symbol == "AAPL"
        assert synthesis.overall_verdict == EpsValidationVerdict.CONSENSUS_VALIDATED
        assert synthesis.confidence_score == 0.85
        assert len(synthesis.method_agreement) == 3
        assert len(synthesis.key_risks) == 2
        assert len(synthesis.supporting_evidence) == 3
        assert synthesis.consensus_adjustment_recommendation is None

    def test_eps_validation_synthesis_confidence_score_bounds(self):
        """Test that confidence_score is properly bounded between 0 and 1."""
        with pytest.raises(ValidationError):
            EpsValidationSynthesis(
                symbol="TEST",
                overall_verdict=EpsValidationVerdict.CONSENSUS_VALIDATED,
                confidence_score=1.5,  # Invalid - above 1.0
                method_agreement={},
                key_risks=[],
                supporting_evidence=[],
                synthesis_analysis="Test",
                investment_implications="Test"
            )

        with pytest.raises(ValidationError):
            EpsValidationSynthesis(
                symbol="TEST",
                overall_verdict=EpsValidationVerdict.CONSENSUS_VALIDATED,
                confidence_score=-0.1,  # Invalid - below 0.0
                method_agreement={},
                key_risks=[],
                supporting_evidence=[],
                synthesis_analysis="Test",
                investment_implications="Test"
            )

    def test_eps_validation_verdict_enum_values(self):
        """Test that all EpsValidationVerdict enum values are accessible."""
        assert EpsValidationVerdict.CONSENSUS_VALIDATED == "CONSENSUS_VALIDATED"
        assert EpsValidationVerdict.CONSENSUS_TOO_HIGH == "CONSENSUS_TOO_HIGH"
        assert EpsValidationVerdict.CONSENSUS_TOO_LOW == "CONSENSUS_TOO_LOW"
        assert EpsValidationVerdict.INSUFFICIENT_DATA == "INSUFFICIENT_DATA"

    def test_revision_momentum_enum_values(self):
        """Test that all RevisionMomentum enum values are accessible."""
        assert RevisionMomentum.UPWARD == "UPWARD"
        assert RevisionMomentum.DOWNWARD == "DOWNWARD"
        assert RevisionMomentum.STABLE == "STABLE"
        assert RevisionMomentum.VOLATILE == "VOLATILE"
        assert RevisionMomentum.INSUFFICIENT_DATA == "INSUFFICIENT_DATA"

    def test_confidence_level_enum_values(self):
        """Test that all ConfidenceLevel enum values are accessible."""
        assert ConfidenceLevel.HIGH == "HIGH"
        assert ConfidenceLevel.MEDIUM == "MEDIUM"
        assert ConfidenceLevel.LOW == "LOW"

    def test_sentiment_alignment_enum_values(self):
        """Test that all SentimentAlignment enum values are accessible."""
        assert SentimentAlignment.BULLISH == "BULLISH"
        assert SentimentAlignment.BEARISH == "BEARISH"
        assert SentimentAlignment.NEUTRAL == "NEUTRAL"
        assert SentimentAlignment.CONFLICTED == "CONFLICTED"

    def test_model_serialization(self, consensus_validated_bottom_up):
        """Test that models can be serialized to and from dict."""
        original = consensus_validated_bottom_up

        # Convert to dict
        data = original.model_dump()
        assert isinstance(data, dict)
        assert data["symbol"] == "AAPL"
        assert data["validation_verdict"] == "CONSENSUS_VALIDATED"

        # Recreate from dict
        recreated = BottomUpEpsValidation(**data)
        assert recreated == original

    def test_mixed_verdict_synthesis_handling(self, mixed_verdict_synthesis):
        """Test that synthesis properly handles mixed verdicts across methods."""
        synthesis = mixed_verdict_synthesis

        assert synthesis.overall_verdict == EpsValidationVerdict.CONSENSUS_VALIDATED
        assert synthesis.confidence_score < 0.6  # Lower confidence due to mixed signals

        verdicts = synthesis.method_agreement
        assert verdicts["bottom_up"] == EpsValidationVerdict.CONSENSUS_TOO_LOW
        assert verdicts["peer_relative"] == EpsValidationVerdict.CONSENSUS_TOO_HIGH
        assert verdicts["market_sentiment"] == EpsValidationVerdict.CONSENSUS_VALIDATED

        # Should contain recommendation for monitoring
        assert "Monitor" in synthesis.consensus_adjustment_recommendation

    def test_consensus_adjustment_recommendation_logic(self, consensus_too_high_synthesis):
        """Test that consensus adjustment recommendations are provided when appropriate."""
        synthesis = consensus_too_high_synthesis

        assert synthesis.overall_verdict == EpsValidationVerdict.CONSENSUS_TOO_HIGH
        assert synthesis.consensus_adjustment_recommendation is not None
        assert "Reduce" in synthesis.consensus_adjustment_recommendation
        assert "15-20%" in synthesis.consensus_adjustment_recommendation