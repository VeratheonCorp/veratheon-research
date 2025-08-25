from agents.extensions.models.litellm_model import LitellmModel
import os

MODEL_SELECTED = os.getenv("MODEL_SELECTED")
LOCAL_OLLAMA_URL = os.getenv("LOCAL_OLLAMA_URL")
NORD_OLLAMA_URL = os.getenv("NORD_OLLAMA_URL")

local_gemma27b_model = LitellmModel(model="ollama/gemma3:27b-it-qat", api_key="ollama", base_url=LOCAL_OLLAMA_URL)
local_gemma12b_model = LitellmModel(model="ollama/gemma3:12b-it-qat", api_key="ollama", base_url=LOCAL_OLLAMA_URL)
local_gemma4b_model = LitellmModel(model="ollama/gemma3:4b-it-qat", api_key="ollama", base_url=LOCAL_OLLAMA_URL)
nord_gemma27b_model = LitellmModel(model="ollama/gemma3:27b-it-qat", api_key="ollama", base_url=NORD_OLLAMA_URL)
nord_gemma12b_model = LitellmModel(model="ollama/gemma3:12b-it-qat", api_key="ollama", base_url=NORD_OLLAMA_URL)
nord_gemma4b_model = LitellmModel(model="ollama/gemma3:4b-it-qat", api_key="ollama", base_url=NORD_OLLAMA_URL)
local_gptoss_model = LitellmModel(model="ollama/gpt-oss:20b", api_key="ollama", base_url=LOCAL_OLLAMA_URL)
nord_gptoss_model = LitellmModel(model="ollama/gpt-oss:20b", api_key="ollama", base_url=NORD_OLLAMA_URL)

def get_model():
    if MODEL_SELECTED == "local_gemma27b":
        model = local_gemma27b_model
    elif MODEL_SELECTED == "nord_gemma27b":
        model = nord_gemma27b_model
    elif MODEL_SELECTED == "local_gemma12b":
        model = local_gemma12b_model
    elif MODEL_SELECTED == "nord_gemma12b":
        model = nord_gemma12b_model
    elif MODEL_SELECTED == "local_gemma4b":
        model = local_gemma4b_model
    elif MODEL_SELECTED == "nord_gemma4b":
        model = nord_gemma4b_model
    elif MODEL_SELECTED == "local_gptoss":
        model = local_gptoss_model
    elif MODEL_SELECTED == "nord_gptoss":
        model = nord_gptoss_model
    elif MODEL_SELECTED == "o4_mini":
        model = "o4-mini"
    else:
        raise ValueError("No valid model selected")
    return model