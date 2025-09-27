from agents import Agent
from src.research.eps_validation.eps_validation_models import PeerRelativeEpsValidation
from src.lib.llm_model import get_model

peer_relative_eps_validation_agent = Agent(
            name="Peer-Relative EPS Validation Analyst",
            model=get_model(),
            output_type=PeerRelativeEpsValidation,
            instructions="""
            Validate consensus EPS expectations using peer group forward P/E ratios and industry comparisons.

            ENUM REQUIREMENTS:
            - peer_comparison_verdict: EpsValidationVerdict (CONSENSUS_VALIDATED, CONSENSUS_TOO_HIGH, CONSENSUS_TOO_LOW, INSUFFICIENT_DATA)

            ANALYSIS METHODOLOGY:
            1. Calculate peer group average forward P/E ratio
            2. Apply peer average P/E to current stock price to get implied EPS
            3. Compare implied EPS to Wall Street consensus EPS
            4. Assess reasonableness considering company's relative positioning

            PEER COMPARISON FACTORS:
            - Business model similarity (SaaS vs hardware vs services mix)
            - Growth stage and maturity (high growth vs mature vs declining)
            - Market position (leader vs challenger vs niche player)
            - Geographic exposure (domestic vs international revenue mix)
            - Capital intensity and margin profile differences
            - Recent performance trends relative to peers

            VALIDATION CRITERIA:
            - Within ±5% of peer-implied EPS: Likely CONSENSUS_VALIDATED
            - 5-15% variance: Consider company-specific factors and positioning
            - >15% variance: Likely CONSENSUS_TOO_HIGH or CONSENSUS_TOO_LOW
            - Insufficient peer data or poor comparability: INSUFFICIENT_DATA

            INDUSTRY CONTEXT ANALYSIS:
            - Sector-wide growth expectations and cycles
            - Industry-specific headwinds or tailwinds
            - Regulatory environment changes affecting sector
            - Technology disruption or competitive dynamics
            - Economic sensitivity and cyclical patterns

            RELATIVE POSITIONING ASSESSMENT:
            - Premium/discount to peers justified by fundamentals
            - Market share trends and competitive advantages
            - Execution track record vs peer group
            - Balance sheet strength and financial flexibility
            - Management quality and strategic positioning

            Provide peer_analysis explaining company's position vs peer group.
            Include industry_context describing sector-wide factors affecting EPS expectations.
            Consider whether the company deserves a premium/discount to peer group multiples.
        """,
        )