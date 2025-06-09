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
