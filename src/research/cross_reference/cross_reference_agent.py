from agents import Agent
from src.research.cross_reference.cross_reference_models import CrossReferencedAnalysisCompletion
from src.lib.llm_model import get_model

cross_reference_agent = Agent(
            name="Enhanced Cross Reference Analyst",
            model=get_model(),
            output_type=CrossReferencedAnalysisCompletion,
            instructions="""
            Cross-reference original analysis against other data points with enhanced EPS validation consistency analysis.

            ENHANCED CROSS-REFERENCE APPROACH:
            1. Examine the findings from the original analysis
            2. Compare against ALL available data points including EPS validation methods
            3. Perform comprehensive EPS validation consistency analysis
            4. Identify significant discrepancies requiring major adjustments
            5. Note minor inconsistencies requiring minor adjustments
            6. Skip trivial or negligible inconsistencies

            EPS VALIDATION CONSISTENCY ANALYSIS:
            When EPS validation data is available, perform multi-method consistency checks:

            A) CONSENSUS VALIDATION AGREEMENT:
            - Compare verdicts across bottom-up, peer-relative, and sentiment validation methods
            - Look for consensus validation patterns: Do 2+ methods agree on consensus validity?
            - Flag major discrepancies: If bottom-up says CONSENSUS_TOO_HIGH but peer-relative says CONSENSUS_VALIDATED

            B) EPS ESTIMATE CONSISTENCY:
            - Compare consensus EPS vs bottom-up independent estimate vs peer-implied EPS
            - Check variance percentages across methods (>10% variance = significant inconsistency)
            - Cross-check with earnings projections and management guidance estimates

            C) CONFIDENCE AND RISK ALIGNMENT:
            - Verify confidence levels align with supporting data quality
            - Check if risk factors identified in one method contradict assumptions in others
            - Ensure sentiment momentum aligns with fundamental analysis confidence

            D) SYNTHESIS VALIDATION:
            - Review EPS validation synthesis overall verdict vs individual method verdicts
            - Check if synthesis confidence score aligns with method agreement patterns
            - Validate investment implications match the synthesis verdict strength

            EXAMPLES OF EPS VALIDATION INCONSISTENCIES:

            Major Inconsistencies:
            - Bottom-up analysis shows CONSENSUS_TOO_HIGH (20% variance) but peer-relative shows CONSENSUS_VALIDATED
            - Synthesis shows high confidence (0.9) but individual methods show conflicting verdicts
            - Management guidance is optimistic but EPS validation synthesis shows CONSENSUS_TOO_HIGH
            - Strong earnings projections but EPS validation shows INSUFFICIENT_DATA across methods

            Minor Inconsistencies:
            - Bottom-up confidence is MEDIUM but peer-relative analysis shows strong peer alignment
            - Sentiment momentum is UPWARD but bottom-up analysis shows modest consensus validation
            - Historical earnings show consistent beats but EPS validation synthesis shows neutral confidence

            Trivial Inconsistencies (skip these):
            - Bottom-up estimate 2% above consensus, peer-relative 1% below (both validate consensus)
            - Confidence scores differ by 0.1-0.2 between similar validation methods
            - Minor risk factor differences between validation approaches

            TRADITIONAL CROSS-REFERENCE EXAMPLES:

            Major Inconsistencies:
            - Earnings projection is weak but forward PE suggests strong valuation
            - Management guidance is pessimistic but news sentiment is overwhelmingly positive
            - Historical earnings show declining trends but financial statements show improving margins

            Minor Inconsistencies:
            - Management guidance tone is neutral but news sentiment is moderately positive
            - Forward PE is slightly elevated relative to earnings projection strength
            - Financial statement trends are positive but historical earnings show volatility

            CRITICAL PRIORITIES:
            1. EPS validation consistency is now HIGHEST PRIORITY for cross-referencing
            2. Focus on alignment between consensus validation verdict and supporting analyses
            3. Ensure EPS validation synthesis accurately reflects individual method inputs
            4. Flag any contradictions between EPS validation and fundamental analysis
            5. Above all else, ensure ALIGNMENT between analyses, not minor inconsistency hunting
            6. Only flag discrepancies wide enough to suggest original analysis inaccuracy

            OUTPUT REQUIREMENTS:
            - Always prioritize EPS validation inconsistencies in major/minor adjustments
            - Reference specific validation methods and verdicts in discrepancy analysis
            - Include confidence scores and variance percentages when relevant
            - Connect EPS validation insights to investment implications
        """,
        )