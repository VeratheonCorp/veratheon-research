import pytest
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


@pytest.fixture
def sample_symbol():
    """Sample stock symbol for testing."""
    return "AAPL"


@pytest.fixture
def consensus_validated_bottom_up():
    """Bottom-up EPS validation with consensus validated verdict."""
    return BottomUpEpsValidation(
        symbol="AAPL",
        independent_eps_estimate=6.85,
        consensus_eps=6.82,
        variance_percentage=0.44,
        confidence_level=ConfidenceLevel.HIGH,
        key_assumptions=[
            "Revenue growth of 5% YoY",
            "Operating margin expansion to 30.2%",
            "Share count reduction of 3%"
        ],
        validation_verdict=EpsValidationVerdict.CONSENSUS_VALIDATED,
        supporting_analysis="Bottom-up reconstruction validates consensus EPS within acceptable variance",
        risk_factors=["iPhone demand uncertainty", "Supply chain disruptions"]
    )


@pytest.fixture
def consensus_too_high_bottom_up():
    """Bottom-up EPS validation with consensus too high verdict."""
    return BottomUpEpsValidation(
        symbol="TSLA",
        independent_eps_estimate=2.45,
        consensus_eps=3.12,
        variance_percentage=-21.47,
        confidence_level=ConfidenceLevel.MEDIUM,
        key_assumptions=[
            "Vehicle deliveries growth of 15%",
            "Margin compression due to price cuts",
            "Increased R&D spending on FSD"
        ],
        validation_verdict=EpsValidationVerdict.CONSENSUS_TOO_HIGH,
        supporting_analysis="Bottom-up analysis suggests consensus is overly optimistic on margins",
        risk_factors=["Competitive pressure", "Regulatory challenges", "Execution risk"]
    )


@pytest.fixture
def consensus_too_low_bottom_up():
    """Bottom-up EPS validation with consensus too low verdict."""
    return BottomUpEpsValidation(
        symbol="NVDA",
        independent_eps_estimate=12.85,
        consensus_eps=10.45,
        variance_percentage=22.97,
        confidence_level=ConfidenceLevel.HIGH,
        key_assumptions=[
            "Data center revenue growth of 40%",
            "AI chip demand exceeding expectations",
            "Margin expansion from premium pricing"
        ],
        validation_verdict=EpsValidationVerdict.CONSENSUS_TOO_LOW,
        supporting_analysis="AI revolution driving stronger than expected demand and pricing power",
        risk_factors=["Cyclical downturn risk", "Competition from custom chips"]
    )


@pytest.fixture
def insufficient_data_bottom_up():
    """Bottom-up EPS validation with insufficient data verdict."""
    return BottomUpEpsValidation(
        symbol="NEWCO",
        independent_eps_estimate=0.0,
        consensus_eps=1.25,
        variance_percentage=0.0,
        confidence_level=ConfidenceLevel.LOW,
        key_assumptions=["Limited financial history", "Emerging business model"],
        validation_verdict=EpsValidationVerdict.INSUFFICIENT_DATA,
        supporting_analysis="Insufficient historical data for reliable bottom-up reconstruction",
        risk_factors=["Business model uncertainty", "Limited track record"]
    )


@pytest.fixture
def consensus_validated_peer_relative():
    """Peer-relative EPS validation with consensus validated verdict."""
    return PeerRelativeEpsValidation(
        symbol="AAPL",
        peer_group_avg_forward_pe=25.3,
        current_stock_price=175.80,
        implied_eps_from_peers=6.95,
        consensus_eps=6.82,
        relative_variance=1.91,
        peer_comparison_verdict=EpsValidationVerdict.CONSENSUS_VALIDATED,
        peer_analysis="Company trading in line with peer group expectations",
        industry_context="Technology sector showing stable valuation metrics"
    )


@pytest.fixture
def consensus_too_high_peer_relative():
    """Peer-relative EPS validation with consensus too high verdict."""
    return PeerRelativeEpsValidation(
        symbol="META",
        peer_group_avg_forward_pe=18.5,
        current_stock_price=325.50,
        implied_eps_from_peers=17.59,
        consensus_eps=20.45,
        relative_variance=-13.98,
        peer_comparison_verdict=EpsValidationVerdict.CONSENSUS_TOO_HIGH,
        peer_analysis="Consensus appears optimistic relative to peer group valuation",
        industry_context="Social media sector facing headwinds affecting profitability"
    )


@pytest.fixture
def upward_momentum_sentiment():
    """Market sentiment EPS check with upward revision momentum."""
    return MarketSentimentEpsCheck(
        symbol="NVDA",
        revision_momentum=RevisionMomentum.UPWARD,
        sentiment_eps_alignment=SentimentAlignment.BULLISH,
        whisper_vs_consensus=1.25,
        sentiment_validation_verdict=EpsValidationVerdict.CONSENSUS_TOO_LOW,
        revision_analysis="Strong upward revision momentum with 12 upgrades in past month",
        sentiment_insights=[
            "AI sentiment driving bullish expectations",
            "Whisper numbers significantly above consensus",
            "Management guidance suggesting upside"
        ],
        market_expectation_summary="Market expects significant consensus beat based on AI tailwinds"
    )


@pytest.fixture
def downward_momentum_sentiment():
    """Market sentiment EPS check with downward revision momentum."""
    return MarketSentimentEpsCheck(
        symbol="NFLX",
        revision_momentum=RevisionMomentum.DOWNWARD,
        sentiment_eps_alignment=SentimentAlignment.BEARISH,
        whisper_vs_consensus=-0.85,
        sentiment_validation_verdict=EpsValidationVerdict.CONSENSUS_TOO_HIGH,
        revision_analysis="Consistent downward revisions following subscriber growth concerns",
        sentiment_insights=[
            "Streaming competition intensifying",
            "Whisper numbers below consensus",
            "Management commentary more cautious"
        ],
        market_expectation_summary="Market expects consensus miss due to competitive pressures"
    )


@pytest.fixture
def stable_momentum_sentiment():
    """Market sentiment EPS check with stable revision momentum."""
    return MarketSentimentEpsCheck(
        symbol="MSFT",
        revision_momentum=RevisionMomentum.STABLE,
        sentiment_eps_alignment=SentimentAlignment.NEUTRAL,
        whisper_vs_consensus=0.15,
        sentiment_validation_verdict=EpsValidationVerdict.CONSENSUS_VALIDATED,
        revision_analysis="Minimal revision activity with stable analyst sentiment",
        sentiment_insights=[
            "Cloud growth expectations well-established",
            "Whisper numbers close to consensus",
            "Consistent execution track record"
        ],
        market_expectation_summary="Market confidence in consensus estimates based on stable business model"
    )


@pytest.fixture
def consensus_validated_synthesis():
    """EPS validation synthesis with overall consensus validated verdict."""
    return EpsValidationSynthesis(
        symbol="AAPL",
        overall_verdict=EpsValidationVerdict.CONSENSUS_VALIDATED,
        confidence_score=0.85,
        method_agreement={
            "bottom_up": EpsValidationVerdict.CONSENSUS_VALIDATED,
            "peer_relative": EpsValidationVerdict.CONSENSUS_VALIDATED,
            "market_sentiment": EpsValidationVerdict.CONSENSUS_VALIDATED
        },
        key_risks=["Macro economic headwinds", "Supply chain disruptions"],
        supporting_evidence=[
            "All three validation methods confirm consensus accuracy",
            "Bottom-up reconstruction within 1% of consensus",
            "Peer valuations support current expectations"
        ],
        consensus_adjustment_recommendation=None,
        synthesis_analysis="Strong validation across all methods supports consensus reliability",
        investment_implications="Current consensus provides reliable baseline for investment decisions"
    )


@pytest.fixture
def consensus_too_high_synthesis():
    """EPS validation synthesis with overall consensus too high verdict."""
    return EpsValidationSynthesis(
        symbol="TSLA",
        overall_verdict=EpsValidationVerdict.CONSENSUS_TOO_HIGH,
        confidence_score=0.72,
        method_agreement={
            "bottom_up": EpsValidationVerdict.CONSENSUS_TOO_HIGH,
            "peer_relative": EpsValidationVerdict.CONSENSUS_TOO_HIGH,
            "market_sentiment": EpsValidationVerdict.CONSENSUS_VALIDATED
        },
        key_risks=["Margin compression from competition", "Execution challenges", "Regulatory headwinds"],
        supporting_evidence=[
            "Bottom-up analysis shows 20%+ downside to consensus",
            "Peer valuations suggest overoptimism",
            "Recent guidance more conservative than consensus"
        ],
        consensus_adjustment_recommendation="Reduce consensus EPS estimate by 15-20%",
        synthesis_analysis="Multiple validation methods indicate consensus overestimation",
        investment_implications="Consider consensus risk in valuation models and position sizing"
    )


@pytest.fixture
def mixed_verdict_synthesis():
    """EPS validation synthesis with mixed verdicts across methods."""
    return EpsValidationSynthesis(
        symbol="AMZN",
        overall_verdict=EpsValidationVerdict.CONSENSUS_VALIDATED,
        confidence_score=0.58,
        method_agreement={
            "bottom_up": EpsValidationVerdict.CONSENSUS_TOO_LOW,
            "peer_relative": EpsValidationVerdict.CONSENSUS_TOO_HIGH,
            "market_sentiment": EpsValidationVerdict.CONSENSUS_VALIDATED
        },
        key_risks=["AWS growth uncertainty", "E-commerce margin pressure", "Capital allocation decisions"],
        supporting_evidence=[
            "Mixed signals across validation methods",
            "Bottom-up shows AWS upside potential",
            "Peer analysis suggests retail headwinds"
        ],
        consensus_adjustment_recommendation="Monitor for additional data points before adjusting",
        synthesis_analysis="Conflicting validation signals suggest consensus uncertainty",
        investment_implications="Exercise caution given validation method disagreement"
    )