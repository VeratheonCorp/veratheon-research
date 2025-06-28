from agents import Agent, AgentOutputSchema, OpenAIChatCompletionsModel
from openai import AsyncOpenAI
from src.company_research.models.reports import MacroEconomicReport



agent = Agent(
    name="Macro Industry Analysis Agent",
    model=OpenAIChatCompletionsModel(
        model="o4-mini",
        openai_client=AsyncOpenAI()
    ),
    output_type=AgentOutputSchema(MacroEconomicReport, strict_json_schema=False),
    instructions=(
        "You are a senior financial research analyst. You will be given macro data (GDP, inflation, unemployment, yields, etc.). "
        "Produce a MacroIndustryReport with these fields: "
        "economic_cycle, economic_outlook, interest_rate_forecast, inflation_forecast, "
        "industry_lifecycle, unemployment_forecast, unemployment_outlook. "
        "All percentages must be in string format (e.g., '0.0%')."
    ),   
)