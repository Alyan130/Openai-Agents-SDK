from agents import Agent, Runner, AsyncOpenAI,OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
import os
import dotenv
from models import TripPlan, CheckDetails , TripSuccess
import random
import asyncio

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

check_details_agent = Agent(
   name = "Check details agent",
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


def run_agents():
    print("Plan your trip now!")
    city = input('Enter city in which you want to plan a trip.')

    trip_details = Runner.run_sync(plan_agent,city)
    
    print("passing details")

    details = Runner.run_sync(check_details_agent,trip_details.final_output)
     

    if details.final_output.isCity and details.final_output.isHotel and details.final_output.isRoute:
        exit(0)
    
    print("details are valid now i succesfylly plans trip")

    trip =  Runner.run_sync(trip_succes_agent,trip_details.final_output)
    
    print(trip.final_output)


run_agents()