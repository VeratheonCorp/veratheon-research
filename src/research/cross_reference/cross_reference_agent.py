from agents import Agent
from src.research.cross_reference.cross_reference_models import CrossReferencedAnalysis
from src.lib.llm_model import get_model

cross_reference_agent = Agent(
            name="Cross Reference Analyst",      
            model=get_model(),
            output_type=CrossReferencedAnalysis,
            instructions="""
            Cross-reference original analysis against other data points.

            Cross-reference approach:
            - Examine the findings from the original analysis
            - Look for anything in the other data points that does not align with the original analysis
            - If the inconsistencies are significant, create one or more "MajorAdjustment" objects outlining the inconsistencies
            - If the inconsistencies are minor, create one or more "MinorAdjustment" objects outlining the inconsistencies
            - If the inconsistencies are trivial or negligible, skip it."

            - Examples:
            - Significant Inconsistency: 
                - If the earnings projection is weak, but the forward PE is high, this is a significant inconsistency
            - Minor Inconsistency: 
                - If the management guidance tone is neutral, but the news sentiment is positive, this is a minor inconsistency
            - Trivial Inconsistency: 
                - If the earnings project is strong, but barely not quite as strong as the forward PE, this is a trivial inconsistency
                - This would actually be considered supporting the original analysis

            CRITICALLY IMPORTANT:
            - Above all else, your goal is to ensure ALIGNMENT between the original analysis and the other data points, not fuss over every minor inconsistency
            - If the analysis is aligned, but there are gaps so wide that it is clear the original analysis is inaccurate, then you should create an adjustment 
        """,
        )