
from enum import Enum
from agents import Agent, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from pydantic import BaseModel


class ResearchQuestionCategories(Enum):
    MARKET = "MARKET"
    SECTOR = "SECTOR"
    INDUSTRY = "INDUSTRY"
    COMPANY = "COMPANY"
    SECURITY = "SECURITY"
    COMMODITY = "COMMODITY"
    CURRENCY = "CURRENCY"
    MACROECONOMIC = "MACROECONOMIC"

class ResearchQuestionType(BaseModel):
    """
    Enum for the type of research question.
    """
    category: ResearchQuestionCategories
    is_nuanced: bool
    reasoning: str
    
    
agent = Agent(
    name="Intake Triage Agent",
    model=OpenAIChatCompletionsModel(
        model="o4-mini",
        openai_client=AsyncOpenAI()
    ),
    output_type=ResearchQuestionType,
    instructions="You are a senior financial research analyst at a Market Research firm. You will be given a market research related question and you will classify the question into one of the following categories: 1) Market 2) Sector 3) Industry 4) Company 5) Security 6) Commodity 7) Currency 8) Macroeconomic. If the question is about a security or ticker, but the security or ticker is a specific company such as AAPL, return COMPANY and not SECURITY. Determine if the question is simple and straightforward, or if it will require careful analysis and nuance. You will also provide a brief reasoning for your classification. If the question can be answered with some API calls to Alpha Vantage, the question is likely simple and straightforward."
)