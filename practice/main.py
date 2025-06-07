from agents import Agent, Runner, AsyncOpenAI,OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
import os
import dotenv
from models import TripPlan, FlightCheck , TripSuccess

dotenv.load_dotenv()

set_tracing_disabled(disabled=True)
API_KEY = os.getenv("API_KEY")


provider = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key= API_KEY
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client=provider
)


