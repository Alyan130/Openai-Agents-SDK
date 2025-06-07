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

@function_tool


plan_agent=Agent(
    name="Trip planning agent",
    instructions='''
    You plan the trip based on user details\n
    You have one tool <hotels> that helps you to select hotels in trip 
    Your task is to add route in trip planning details you can either add [flight,byroad,train] anyone of them 
    ''',
    tools=[hotels],
    model=model,
    output_type=TripPlan
)

