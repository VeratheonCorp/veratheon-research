"""
TEMPLATE: Technical EPS Validation Agent

This file serves as a template for creating new EPS validation methods.
Replace 'technical' with your validation method name throughout.
"""

from agents import Agent
from src.lib.llm_model import get_model
from src.research.eps_validation.eps_validation_models import TechnicalEpsValidation

# TEMPLATE: Agent configuration for technical EPS validation
technical_eps_validation_agent = Agent(
    name="technical_eps_validation_agent",
    model=get_model(),
    instructions="""
    Validate EPS estimates through technical analysis of price action, volume, and momentum.

    OBJECTIVE:
    1. Analyze technical indicators (price momentum, volume, RSI, MACD)
    2. Calculate implied EPS from technical price targets
    3. Compare to consensus EPS and determine validation verdict

    VALIDATION VERDICTS:
    - CONSENSUS_VALIDATED: Technical analysis supports consensus (within ±5%)
    - CONSENSUS_TOO_HIGH: Technical suggests overoptimism (>10% variance)
    - CONSENSUS_TOO_LOW: Technical suggests underestimation (>10% variance)
    - INSUFFICIENT_DATA: Unable to perform reliable validation

    CONFIDENCE LEVELS:
    - HIGH: Strong technical signals with volume confirmation
    - MEDIUM: Moderate signals with some conflicting indicators
    - LOW: Weak or conflicting signals

    KEY INDICATORS:
    - Price momentum and trend direction
    - Volume patterns and accumulation/distribution
    - Support/resistance levels
    - Moving averages and oscillators

    Provide technical_analysis with specific indicators, volume_analysis, and risk_factors.
    Include investment_implications based on technical validation.
    """,
    output_type=TechnicalEpsValidation,
)