from agents import Agent, Runner, AsyncOpenAI,OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
import os
from dotenv import load_dotenv
from agents.mcp import MCPServerStdio ,MCPServer
import asyncio 
from typing import Any

load_dotenv()
set_tracing_disabled(disabled=True)
GH_TOKEN = os.getenv("GH_TOKEN")

provider = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key=os.getenv("API_KEY")
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client=provider
)


async def run_agent(mcp_server:MCPServer,prompt:str):
  automation_agent = Agent(
      name="Github agent",
      instructions = '''
      You are gitub automation agent , that automates github account and be friendly to the user.
      You have following tools to work with:

      Dont use tool create_webhook ok.

      #Repository Management Tools
- set_default_repo: Set a default owner and repository for subsequent commands to streamline your workflow.
Args: owner (string, required), repo (string, required)
- list_repos: List GitHub repositories for the authenticated user with advanced filtering.
Args: per_page (number, optional, default 10, max 100), visibility (string, optional, enum: "all", "public", "private", default "all"), sort (string, optional, enum: "created", "updated", "pushed", "full_name", default "updated")
- get_repo_info: Get comprehensive information about a specific repository including stats and metadata.
Args: owner (string, required if no default), repo (string, required if no default)
- search_repos: Search for repositories across GitHub with advanced sorting options.
Args: query (string, required), per_page (number, optional, default 10, max 100), sort (string, optional, enum: "stars", "forks", "help-wanted-issues", "updated", default "stars")
- get_repo_contents: Browse files and directories in any repository with branch/commit support.
Args: owner (string, required if no default), repo (string, required if no default), path (string, optional, default ""), ref (string, optional, e.g., branch name or commit SHA)

       ''',
      model = model,
      mcp_servers=[mcp_server]
    )
  
  result = await Runner.run(automation_agent,prompt)
  print(result.final_output)


async def main():
  try:
   async with MCPServerStdio(
       client_session_timeout_seconds= 35,
       params={
           "command":"node",
           "args":["D:\Python Course\AI_projects\Openai-Agents-SDK\mcp\github-repos-manager-mcp"],
           "env": {
               "GH_TOKEN":GH_TOKEN,
           },
           "cwd":"D:\Python Course\AI_projects\Openai-Agents-SDK\mcp\github-repos-manager-mcp"
       }
    ) as server:
         print(f"{server._name} started!")
         await run_agent(server,"Tell me about this repo")

  except Exception as e:
      print("Error occured!",e)  


if __name__ == "__main__":
  asyncio.run((main()))


