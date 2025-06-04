from agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from pydantic import BaseModel
from src.company_research.models.diligence import Diligence


class PriceTargetIntakeOutput(BaseModel):
  summary: str
  reasoning: str


agent = Agent(
    name="Price Target Intake Agent",
    model=OpenAIChatCompletionsModel(
        model="o4-mini",
        openai_client=AsyncOpenAI()
    ),
    output_type=PriceTargetIntakeOutput,
    instructions="You are a senior financial research analyst at a Market Research firm. You will be given a price target and you need to generate short summary report, no more than two sentences, on the information provided in the financials and macroeconomics of the Diligence object. Provide your reasoning for your summary."
)

