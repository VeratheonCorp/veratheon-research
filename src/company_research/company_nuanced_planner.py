import json
from agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from pydantic import BaseModel
from typing import Optional

class CompanyNuancedPlanningOutput(BaseModel):
    """
    This class is used to define the output of the company planning agent.
    It contains the following attributes:
    - research_plan: A JSON string that describes the research plan.
    """
    research_plan_json: str


agent = Agent(
    name="Initial Planning Agent",
    model=OpenAIChatCompletionsModel(
        model="o4-mini",
        openai_client=AsyncOpenAI()
    ),
    output_type=CompanyNuancedPlanningOutput,
    instructions="You are a senior financial research analyst at a Market Research firm. You will be given a nuanced research related question for a specific company or companies and you need to generate a research plan. You will create JSON object that contains a numbered list. The first item should be a summary of the key insights needed to answer the question. The remaining items should be how to obtain those insights.")

