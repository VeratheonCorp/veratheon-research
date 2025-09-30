"""
Utility functions for cleaning EPS validation data.
"""


def remove_historical_eps_estimates(data):
    """
    Recursively remove any EPS estimate fields from data structures to prevent LLM confusion.

    Args:
        data: Any data structure (dict, list, object)
    Returns:
        Cleaned data structure with EPS estimates removed
    """
    if isinstance(data, dict):
        cleaned_data = {}
        for key, value in data.items():
            # Skip any keys that might contain EPS estimates
            skip_keys = [
                'estimates', 'earnings_estimates', 'earnings_calendar',
                'eps_estimate', 'consensus_eps', 'reported_eps',
                'historical_estimates', 'analyst_estimates'
            ]

            if key.lower() in [k.lower() for k in skip_keys]:
                continue  # Skip this field entirely

            # Recursively clean nested structures
            cleaned_data[key] = remove_historical_eps_estimates(value)

        return cleaned_data

    elif isinstance(data, list):
        return [remove_historical_eps_estimates(item) for item in data]

    elif hasattr(data, 'model_dump'):
        # Handle Pydantic models
        dict_data = data.model_dump()
        cleaned_dict = remove_historical_eps_estimates(dict_data)
        return cleaned_dict

    else:
        # Return primitive types as-is
        return data