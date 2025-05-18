"""
Define available Alpha Vantage client methods and build a prompt
that can be sent to an LLM to inform it of these resources.
"""

API_RESOURCES = {
    "get_daily_closing_price": "Retrieves the most recent daily closing price for a symbol.",
    "get_news": "Obtains recent news sentiment for a symbol via the NEWS_SENTIMENT endpoint.",
    "get_company_overview": "Fetches fundamental company data (P/E, EPS, etc.) via the OVERVIEW endpoint."
}

def build_alpha_vantage_resources_prompt() -> str:
    """
    Returns a formatted prompt string listing all available
    Alpha Vantage client API methods and their descriptions.
    """
    prompt_lines = ["You have access to the following Alpha Vantage API resources:"]
    for name, desc in API_RESOURCES.items():
        prompt_lines.append(f"- {name}: {desc}")
    prompt_lines.append("\nWhen you need to call one of these, reference its name and provide required parameters.")
    return "\n".join(prompt_lines)
