from agents import Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled,exceptions,RunContextWrapper
from agents import set_default_openai_key,function_tool,RunHooks
from google.colab import userdata
from pydantic import BaseModel
from agents.extensions.models.litellm_model import LitellmModel
from typing import Any

set_tracing_disabled(disabled=True)


class UserInfo(BaseModel):
    name:str
    vip:bool

def custom_instructions(ctx:RunContextWrapper[UserInfo], agent:Agent):
   is_vip = ctx.context.vip
   if is_vip:
    return ('''You are developer agent that has access of two tools designer and builder tool based on you
    user query you can use these tools.''')
   else:
    return ('''
     You are developer agent that has access of only one tool designer tool , you cant use builder tool,
     if user ask to build any thing you just say "please purchase our plan first"
    ''')

class CustomHooks(RunHooks):
  async def on_agent_start(self, context: RunContextWrapper[UserInfo], agent: Agent):
      messsage = ""
      is_vip = context.context.vip
      u_name = context.context.name
      if is_vip:
        message = f"{agent.name} is started working for {u_name} and is vip user.\n"
      else:
        message = f"{agent.name} is started working for {u_name} and not vip user.\n"
      print(message)
  

  async def on_agent_end(self, context: RunContextWrapper[UserInfo], agent: Agent, output:Any):
       message = ""
       is_vip = context.context.vip
       u_name = context.context.name
       if is_vip:
        message = f"Thanks {u_name} for using our service"
       else:
        message = f"Thanks {u_name} for using our service, for better tools by our plan."
        print(f"{output}\n{message}") 

  
  async def on_tool_start(self, context: RunContextWrapper[UserInfo], agent: Agent, tool):
      print(f"{tool.name} Tool started working...")     
 

@function_tool
def designer_tool(ctx:RunContextWrapper[UserInfo])->str:
   '''
   This tool design aything
   '''
   if ctx.context.vip:
     return f"UI is designed."
   else:
     return f"UI designed but with with less modern look."


@function_tool
def builder_tool()->str:
    '''
    This tool build aything
    '''
    return f"Application is  build."


developer = Agent(
    name="Devloper Agent",
    instructions=custom_instructions,
    model = model,
    tools=[designer_tool,builder_tool]
)

async def agent():
    user_name=input("Enter your name: ")
    user_info = UserInfo(name=user_name,vip=False)
    await Runner.run(developer,"Design ai application",context=user_info,hooks=CustomHooks())

await agent()