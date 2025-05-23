from agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from pydantic import BaseModel

from src.agent_tools.alpha_vantage_tool import (
    call_alpha_vantage
)

class AlphaVantageAPIRequest(BaseModel):
    alpha_vantage_api_uri: str
    answer: str
    reasoning: str

class QuestionOutput(BaseModel):
    alpha_vantage_lookups: list[AlphaVantageAPIRequest]

agent = Agent(
    name="Company Direct Question Agent",
    model=OpenAIChatCompletionsModel(
        model="o4-mini",
        openai_client=AsyncOpenAI()
    ),
    tools=[
        call_alpha_vantage,
    ],
    output_type=QuestionOutput,
    instructions="You are a senior financial research analyst at a Market Research firm. You have been given a direct question for a specific company that can be likely answered with one or more AlphaVantage API calls. Use the alpha vantage tool to make the api calls to answer the question. "
    )
