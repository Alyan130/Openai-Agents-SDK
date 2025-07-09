from agents import Agent, Runner, AsyncOpenAI,OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
import os
from agents import RunContextWrapper
from dotenv import load_dotenv
from agents.mcp import MCPServerStdio ,MCPServer
import asyncio 
from typing import Any

load_dotenv()
set_tracing_disabled(disabled=True)

provider = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("API_KEY")
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client=provider
)


async def run_agent(mcp_server:MCPServer,prompt:str):
  calculator_agent = Agent(
      name="Calculator agent",
      instructions = "You are calculator agent that calculates question based on serveral tools.",
      model = model,
      mcp_servers=[mcp_server]
    )
  
  result = await Runner.run(calculator_agent,prompt)
  print(result.final_output)



async def main():
   async with MCPServerStdio(
       params={
          "command":"uv",
          "args":["run","server.py"]
       }
    ) as server:
         print(f"{server._name} started!")
         await run_agent(server,"muliply 10 and 20")
    

     
asyncio.run((main()))

