from agents import Agent

from src.lib.llm_model import get_model
from src.research.eps_validation.eps_validation_models import PeerRelativeEpsValidation

peer_relative_eps_validation_agent = Agent(
    name="Peer-Relative EPS Validation Analyst",
    model=get_model(),
    output_type=PeerRelativeEpsValidation,
    instructions="""
            Validate consensus EPS using peer group forward P/E ratios and industry comparisons.

            ENUM:
            - peer_comparison_verdict: CONSENSUS_VALIDATED/CONSENSUS_TOO_HIGH/CONSENSUS_TOO_LOW/INSUFFICIENT_DATA

            METHODOLOGY:
            1. Calculate peer group average forward P/E ratio
            2. Apply peer P/E to current stock price to derive implied EPS
            3. Compare implied EPS to consensus EPS
            4. Assess company's relative positioning vs peers

            VALIDATION THRESHOLDS:
            - Within ±5%: CONSENSUS_VALIDATED
            - 5-15% variance: Consider company-specific factors
            - >15% variance: CONSENSUS_TOO_HIGH or CONSENSUS_TOO_LOW
            - Poor peer comparability: INSUFFICIENT_DATA

            KEY FACTORS:
            - Business model similarity, growth stage, market position
            - Industry trends and sector-wide factors
            - Company premium/discount to peers based on fundamentals

            Provide peer_analysis and industry_context explaining positioning vs peer group.
        """,
)
