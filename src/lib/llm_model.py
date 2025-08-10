from agents.extensions.models.litellm_model import LitellmModel
import os

MODEL_SELECTED = os.getenv("MODEL_SELECTED")
LOCAL_OLLAMA_URL = os.getenv("LOCAL_OLLAMA_URL")
NORD_OLLAMA_URL = os.getenv("NORD_OLLAMA_URL")

local_ollama_model = LitellmModel(model="ollama/gemma3:27b-it-qat", api_key="ollama", base_url=LOCAL_OLLAMA_URL)
nord_ollama_model = LitellmModel(model="ollama/gemma3:27b-it-qat", api_key="ollama", base_url=NORD_OLLAMA_URL)
o4_mini_model = LitellmModel(model="openai/o4-mini", api_key="openai")

def get_model():
    if MODEL_SELECTED == "local_ollama":
        model = local_ollama_model
    elif MODEL_SELECTED == "nord_ollama":
        model = nord_ollama_model
    elif MODEL_SELECTED == "o4_mini":
        model = o4_mini_model
    else:
        raise ValueError("No valid model selected")
    return model