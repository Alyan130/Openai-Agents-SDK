from agents import Agent, Runner, AsyncOpenAI,OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
import os
import dotenv
from models import TripPlan, CheckDetails , TripSuccess
import random

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
def hotels():
   '''This tool return hotel'''
   my_hotels = ["vegas","newLife","openWorld"]
   hotel= random.choice(my_hotels)
   return hotel
  

plan_agent=Agent(
    name="Trip planning agent",
    instructions='''
    You plan the trip based on user details\n
    You have one tool <hotels> that helps you to select hotels in trip 
    Your task is to add route in trip planning details you can either add [flight,byroad,train] anyone of them 
    following
    ''',
    tools=[hotels],
    model=model,
    output_type=TripPlan
)

check_flight_agent = Agent(
   name = "flight check agent",
   instructions='''
   Your task is to check whether all the details like city ,hotel and route provided or not and answer in structured output.
   ''',
   model=model,
   output_type=CheckDetails
)

trip_succes_agent= Agent(
  name="You task is to give friendly message to the user that trip has been planned with trip details",
  model=model,
  output_type=TripSuccess
)


async def run_agents():
    print("Plan your trip now!")
    uinput = input("Enter your trip details")

   trip_details = await Runner.run(plan_agent,)


