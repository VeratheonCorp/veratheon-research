"""
Define available Alpha Vantage client methods and build a prompt
that can be sent to an LLM to inform it of these resources.
"""

API_RESOURCES = {
    "get_daily_closing_price": "Retrieves the most recent daily closing price for a symbol.",
    "get_news": "Obtains recent news sentiment for a symbol via the NEWS_SENTIMENT endpoint.",
    "get_company_overview": "Fetches fundamental company data (P/E, EPS, etc.) via the OVERVIEW endpoint."
}

API_RESOURCE_PARAMS = {
    "get_daily_closing_price": ["symbol"],
    "get_news": ["symbol"],
    "get_company_overview": ["symbol"]
}

def build_alpha_vantage_resources_prompt() -> str:
    """
    Returns instructions for JSON-only tool invocations with examples.
    """
    prompt_lines = [
        "When you need to invoke a tool, output ONLY a valid JSON object matching this schema:",
        "{",
        '  \"tool\": \"<tool_name>\",',
        '  \"params\": { \"<param_name>\": <value>, ... }',
        "}",
        "",
        "Available tools and required parameters:"
    ]
    for name, params in API_RESOURCE_PARAMS.items():
        prompt_lines.append(f"- {name}: {', '.join(params)}")
    prompt_lines.extend([
        "",
        "Examples:",
        "{\"tool\":\"get_daily_closing_price\",\"params\":{\"symbol\":\"AAPL\"}}",
        "{\"tool\":\"get_news\",\"params\":{\"symbol\":\"GOOGL\"}}",
        "{\"tool\":\"get_company_overview\",\"params\":{\"symbol\":\"MSFT\"}}"
    ])
    return "\n".join(prompt_lines)
