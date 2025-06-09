from agents import Runner , Agent , set_tracing_disabled , function_tool,AsyncOpenAI,OpenAIChatCompletionsModel
from pydantic import BaseModel
from google.colab import userdata
import asyncio


set_tracing_disabled(disabled=True)
API_KEY = userdata.get("GEMINI_KEY")

external_client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


class ScrapeDetails(BaseModel):
   news:str
   ecommerce:str
   sport:str

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

scraper_1 = Agent(
    name = "scraper_1",
    instructions = "you just output news scrapped dont ask anything more",
    model=model 
)


scraper_2 = Agent(
    name = "scraper_2",
    instructions = "you just output ecommerce web scrapped not ask anything more",
    model=model 
)

scraper_3 = Agent(
    name = "scraper_3",
    instructions = "you just output crciket details scrapped not ask anything more",
    model=model 
)

manager_agent = Agent(
    name = "manger agent",
    instructions = "You are maanger agent that returns scrape details",
    model=model,
    output_type=ScrapeDetails
)


async def run_agents():
    print("Started working...")

    res1, res2, res3 = await asyncio.gather(
         Runner.run(
             scraper_1,
             "scrape news"
         ),
           Runner.run(
             scraper_2,
             "scrape ecommerce"
         ),
           Runner.run(
             scraper_3,
             "scrape sports"
         ),
     )
    
    scrape_responses = f'''
     {res1}/n
     {res2}/n
     {res3}/n
    '''

    details = await Runner.run(manager_agent,scrape_responses)
    print(details.final_output)

await run_agents()
   
