import pytest
from src.research.eps_validation.eps_validation_models import (
    PeerRelativeEpsValidation,
    MarketSentimentEpsCheck,
    EpsValidationSynthesis,
    TechnicalEpsValidation,
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
def consensus_validated_peer_relative():
    """Peer-relative EPS validation with consensus validated verdict."""
    return PeerRelativeEpsValidation(
        symbol="AAPL",
        peer_group_avg_forward_pe=25.3,
        current_stock_price=175.80,
        peer_implied_eps_estimate=6.95,
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
        peer_implied_eps_estimate=17.59,
        consensus_eps=20.45,
        relative_variance=-13.98,
        peer_comparison_verdict=EpsValidationVerdict.CONSENSUS_TOO_HIGH,
        peer_analysis="Consensus appears optimistic relative to peer group valuation",
        industry_context="Social media sector facing headwinds affecting profitability"
    )


@pytest.fixture
def consensus_too_low_peer_relative():
    """Peer-relative EPS validation with consensus too low verdict."""
    return PeerRelativeEpsValidation(
        symbol="GOOGL",
        peer_group_avg_forward_pe=22.8,
        current_stock_price=138.50,
        peer_implied_eps_estimate=6.07,
        consensus_eps=5.25,
        relative_variance=15.62,
        peer_comparison_verdict=EpsValidationVerdict.CONSENSUS_TOO_LOW,
        peer_analysis="Peer group valuations suggest consensus is conservative",
        industry_context="Search and cloud segments showing strong growth prospects"
    )


@pytest.fixture
def insufficient_data_peer_relative():
    """Peer-relative EPS validation with insufficient data verdict."""
    return PeerRelativeEpsValidation(
        symbol="STARTUP",
        peer_group_avg_forward_pe=0.0,
        current_stock_price=45.20,
        peer_implied_eps_estimate=0.0,
        consensus_eps=1.85,
        relative_variance=0.0,
        peer_comparison_verdict=EpsValidationVerdict.INSUFFICIENT_DATA,
        peer_analysis="No comparable peer group available for early-stage technology company",
        industry_context="Emerging sector with limited public company comparables"
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
def insufficient_data_sentiment():
    """Market sentiment EPS check with insufficient data verdict."""
    return MarketSentimentEpsCheck(
        symbol="PRIVATE",
        revision_momentum=RevisionMomentum.INSUFFICIENT_DATA,
        sentiment_eps_alignment=SentimentAlignment.NEUTRAL,
        whisper_vs_consensus=None,
        sentiment_validation_verdict=EpsValidationVerdict.INSUFFICIENT_DATA,
        revision_analysis="Limited analyst coverage with insufficient revision data",
        sentiment_insights=[
            "Minimal public market information",
            "No whisper number data available",
            "Limited news sentiment data"
        ],
        market_expectation_summary="Insufficient market data to assess sentiment alignment with consensus"
    )


@pytest.fixture
def consensus_validated_synthesis():
    """EPS validation synthesis with overall consensus validated verdict."""
    return EpsValidationSynthesis(
        symbol="AAPL",
        overall_verdict=EpsValidationVerdict.CONSENSUS_VALIDATED,
        confidence_score=0.85,
        method_agreement={
            "peer_relative": EpsValidationVerdict.CONSENSUS_VALIDATED,
            "market_sentiment": EpsValidationVerdict.CONSENSUS_VALIDATED,
            "technical": EpsValidationVerdict.CONSENSUS_VALIDATED
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
            "peer_relative": EpsValidationVerdict.CONSENSUS_TOO_HIGH,
            "market_sentiment": EpsValidationVerdict.CONSENSUS_VALIDATED,
            "technical": EpsValidationVerdict.CONSENSUS_TOO_HIGH
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
            "peer_relative": EpsValidationVerdict.CONSENSUS_TOO_HIGH,
            "market_sentiment": EpsValidationVerdict.CONSENSUS_VALIDATED,
            "technical": EpsValidationVerdict.CONSENSUS_TOO_LOW
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


@pytest.fixture
def consensus_too_low_synthesis():
    """EPS validation synthesis with overall consensus too low verdict."""
    return EpsValidationSynthesis(
        symbol="NVDA",
        overall_verdict=EpsValidationVerdict.CONSENSUS_TOO_LOW,
        confidence_score=0.78,
        method_agreement={
            "peer_relative": EpsValidationVerdict.CONSENSUS_TOO_LOW,
            "market_sentiment": EpsValidationVerdict.CONSENSUS_TOO_LOW,
            "technical": EpsValidationVerdict.CONSENSUS_TOO_LOW
        },
        key_risks=["AI bubble concerns", "Cyclical semiconductor downturn"],
        supporting_evidence=[
            "All validation methods suggest consensus underestimation",
            "AI demand exceeding all expectations",
            "Pricing power stronger than anticipated"
        ],
        consensus_adjustment_recommendation="Increase consensus EPS estimate by 20-25%",
        synthesis_analysis="Strong convergence across methods indicates significant consensus underestimation",
        investment_implications="Current consensus may not reflect AI revolution impact on fundamentals"
    )


@pytest.fixture
def insufficient_data_synthesis():
    """EPS validation synthesis with insufficient data verdict."""
    return EpsValidationSynthesis(
        symbol="NEWTECH",
        overall_verdict=EpsValidationVerdict.INSUFFICIENT_DATA,
        confidence_score=0.25,
        method_agreement={
            "peer_relative": EpsValidationVerdict.INSUFFICIENT_DATA,
            "market_sentiment": EpsValidationVerdict.INSUFFICIENT_DATA,
            "technical": EpsValidationVerdict.INSUFFICIENT_DATA
        },
        key_risks=["Business model uncertainty", "Limited operating history", "Regulatory unknowns"],
        supporting_evidence=[
            "All validation methods lack sufficient data",
            "No reliable financial history",
            "Limited peer group comparables"
        ],
        consensus_adjustment_recommendation=None,
        synthesis_analysis="Insufficient data across all validation methods prevents reliable consensus assessment",
        investment_implications="High uncertainty requires manual analysis and enhanced due diligence"
    )


# TEMPLATE: Test fixtures for new validation methods
# Replace 'technical' with your validation method name

@pytest.fixture
def consensus_validated_technical():
    """Technical EPS validation with consensus validated verdict."""
    return TechnicalEpsValidation(
        symbol="AAPL",
        price_momentum_score=0.2,
        volume_trend_indicator="INCREASING",
        consensus_eps=6.82,
        technical_implied_eps_estimate=6.79,
        technical_variance_percentage=-0.44,
        validation_verdict=EpsValidationVerdict.CONSENSUS_VALIDATED,
        confidence_level=ConfidenceLevel.HIGH,
        technical_indicators=[
            "RSI: 58 (neutral-bullish)",
            "MACD: Positive crossover",
            "Volume: Above 20-day average",
            "Support at $175"
        ],
        support_resistance_analysis="Strong support at $175 level with resistance at $185, technical outlook supports current EPS expectations",
        risk_factors=["Market volatility", "Sector rotation risk"]
    )


@pytest.fixture
def consensus_too_high_technical():
    """Technical EPS validation with consensus too high verdict."""
    return TechnicalEpsValidation(
        symbol="TSLA",
        price_momentum_score=-0.6,
        volume_trend_indicator="DECREASING",
        consensus_eps=3.25,
        technical_implied_eps_estimate=2.60,
        technical_variance_percentage=-20.0,
        validation_verdict=EpsValidationVerdict.CONSENSUS_TOO_HIGH,
        confidence_level=ConfidenceLevel.MEDIUM,
        technical_indicators=[
            "RSI: 35 (oversold territory)",
            "MACD: Negative divergence",
            "Volume: Below average",
            "Breaking key support levels"
        ],
        support_resistance_analysis="Breaking below key support at $200, bearish technical pattern suggests consensus estimates too optimistic",
        risk_factors=["Weak technical momentum", "Volume confirmation lacking", "Key support breakdown"]
    )


@pytest.fixture
def consensus_too_low_technical():
    """Technical EPS validation with consensus too low verdict."""
    return TechnicalEpsValidation(
        symbol="NVDA",
        price_momentum_score=0.8,
        volume_trend_indicator="INCREASING",
        consensus_eps=12.50,
        technical_implied_eps_estimate=15.60,
        technical_variance_percentage=24.8,
        validation_verdict=EpsValidationVerdict.CONSENSUS_TOO_LOW,
        confidence_level=ConfidenceLevel.HIGH,
        technical_indicators=[
            "RSI: 75 (strong bullish)",
            "MACD: Strong positive momentum",
            "Volume: 2x average",
            "Breaking resistance levels"
        ],
        support_resistance_analysis="Strong breakout above $450 resistance with heavy volume, technical strength suggests consensus underestimates earnings potential",
        risk_factors=["Overbought conditions", "Potential profit-taking"]
    )


@pytest.fixture
def insufficient_data_technical():
    """Technical EPS validation with insufficient data verdict."""
    return TechnicalEpsValidation(
        symbol="PRIVATE",
        price_momentum_score=0.0,
        volume_trend_indicator="INSUFFICIENT_DATA",
        consensus_eps=0.0,
        technical_implied_eps_estimate=0.0,
        technical_variance_percentage=0.0,
        validation_verdict=EpsValidationVerdict.INSUFFICIENT_DATA,
        confidence_level=ConfidenceLevel.LOW,
        technical_indicators=["Insufficient price data for technical analysis"],
        support_resistance_analysis="Cannot perform technical analysis due to limited price and volume data",
        risk_factors=["No technical data available", "Unable to validate through technical methods"]
    )