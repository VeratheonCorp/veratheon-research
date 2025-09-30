from agents import Agent

from src.lib.llm_model import get_model
from src.research.eps_validation.eps_validation_models import EpsValidationSynthesis

eps_validation_synthesis_agent = Agent(
    name="EPS Validation Synthesis Analyst",
    model=get_model(),
    output_type=EpsValidationSynthesis,
    instructions="""
            Synthesize multiple EPS validation methods into a comprehensive consensus verdict.

            ENUM:
            - overall_verdict: CONSENSUS_VALIDATED/CONSENSUS_TOO_HIGH/CONSENSUS_TOO_LOW/INSUFFICIENT_DATA

            INPUT METHODS (up to 6):
            1. Historical Earnings - baseline patterns
            2. Independent Projections - forward-looking fundamentals
            3. Management Guidance - company expectations
            4. Bottom-Up Validation - fundamental reconstruction
            5. Peer-Relative - industry comparison
            6. Market Sentiment - revision momentum

            METHODOLOGY:
            1. Analyze agreement/disagreement across methods
            2. Weight by data quality: Bottom-up/projections (high), peer-relative (medium-high), sentiment (medium)
            3. Determine overall verdict and confidence

            VERDICT RULES:
            - CONSENSUS_VALIDATED: 3+ methods agree, or critical methods align
            - CONSENSUS_TOO_HIGH: Multiple methods suggest optimism, bottom-up lower
            - CONSENSUS_TOO_LOW: Multiple methods suggest conservatism, fundamentals higher
            - INSUFFICIENT_DATA: Conflicting signals or poor data quality

            CONFIDENCE (0.0-1.0):
            - 0.9-1.0: Strong agreement
            - 0.7-0.9: Moderate agreement
            - 0.5-0.7: Mixed signals, lean toward verdict
            - 0.3-0.5: Weak signals
            - 0.0-0.3: Very low confidence

            Provide method_agreement, key_risks, supporting_evidence, consensus_adjustment_recommendation, synthesis_analysis, and investment_implications.
        """,
)
