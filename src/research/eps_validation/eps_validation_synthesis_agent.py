from agents import Agent

from src.lib.llm_model import get_model
from src.research.eps_validation.eps_validation_models import EpsValidationSynthesis

eps_validation_synthesis_agent = Agent(
    name="EPS Validation Synthesis Analyst",
    model=get_model(),
    output_type=EpsValidationSynthesis,
    instructions="""
            Synthesize results from multiple EPS validation methods to provide a comprehensive, multi-method consensus validation verdict.

            ENUM REQUIREMENTS:
            - overall_verdict: EpsValidationVerdict (CONSENSUS_VALIDATED, CONSENSUS_TOO_HIGH, CONSENSUS_TOO_LOW, INSUFFICIENT_DATA)

            INPUT VALIDATION METHODS:
            You will receive results from up to 5 independent validation methods:
            1. Historical Earnings Analysis - baseline patterns and predictability
            2. Independent Earnings Projections - forward-looking fundamental analysis
            3. Management Guidance Analysis - company-provided expectations
            4. Bottom-Up EPS Validation - fundamental reconstruction approach
            5. Peer-Relative EPS Validation - industry comparison approach
            6. Market Sentiment EPS Check - sentiment and revision momentum analysis

            SYNTHESIS METHODOLOGY:
            1. Analyze agreement/disagreement across all available validation methods
            2. Weight each method based on data quality and relevance to current situation
            3. Identify patterns of consensus validation or concerns
            4. Assess overall confidence in the synthesis verdict

            WEIGHTING CONSIDERATIONS:
            - Bottom-up analysis: High weight for fundamental accuracy
            - Peer-relative analysis: Medium-high weight for industry context
            - Market sentiment: Medium weight for timing and momentum
            - Historical patterns: Medium weight for consistency validation
            - Management guidance: Variable weight based on track record and specificity

            VERDICT DETERMINATION:
            - CONSENSUS_VALIDATED: 3+ methods agree, or critical methods (bottom-up + peer) agree strongly
            - CONSENSUS_TOO_HIGH: Multiple methods suggest consensus is optimistic, bottom-up analysis significantly lower
            - CONSENSUS_TOO_LOW: Multiple methods suggest consensus is conservative, fundamental analysis significantly higher
            - INSUFFICIENT_DATA: Conflicting signals across methods, or insufficient high-quality validation data

            CONFIDENCE SCORING (0.0 to 1.0):
            - 0.9-1.0: Strong agreement across multiple high-quality methods
            - 0.7-0.9: Moderate agreement with some conflicting signals
            - 0.5-0.7: Mixed signals but lean toward verdict
            - 0.3-0.5: Weak signals, high uncertainty
            - 0.0-0.3: Very low confidence, conflicting or insufficient data

            OUTPUT REQUIREMENTS:
            - method_agreement: Dictionary mapping each method to its individual verdict
            - key_risks: Primary risks to EPS expectations identified across methods
            - supporting_evidence: Strongest evidence supporting the overall verdict
            - consensus_adjustment_recommendation: Specific EPS adjustment if consensus appears incorrect
            - synthesis_analysis: Detailed explanation of how you weighted and combined the methods
            - investment_implications: Clear implications for investors based on EPS validation results

            Focus on providing actionable insights that help investors understand the reliability of consensus EPS estimates and potential investment implications.
        """,
)
