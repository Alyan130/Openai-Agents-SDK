from typing import Literal
from agents import Runner, Agent, AsyncOpenAI, OpenAIChatCompletionsModel,set_tracing_disabled,exceptions,RunContextWrapper
from agents import set_default_openai_key,function_tool,GuardrailFunctionOutput,input_guardrail,output_guardrail
from openai.types.responses import ResponseTextDeltaEvent
from agents import ModelSettings
from pydantic import BaseModel
from dataclasses import dataclass

set_tracing_disabled(disabled=True)

external_client = AsyncOpenAI(
    api_key = ("OPENROUTER_API"),
    base_url="https://openrouter.ai/api/v1"
)

model = OpenAIChatCompletionsModel(
      model="mistralai/mistral-small-3.2-24b-instruct:free",
      openai_client= external_client
)


class Evaluation(BaseModel):
     quality:str

caption_generator = Agent(
     name = "Caption generator agent",
     instructions = "You are caption generator agent, that generates a caption based on social media post name.Caption must not exceed 20 words.",
     model = model
)

evaluator = Agent(
     name = "Evaluator agent",
     instructions = "You are evaluator agent, that evaluates a caption of social media post. Dont pass the caption in one try",
     model = model,
     output_type = Evaluation
)

async def run_agents(): 
     while True:

      result = await Runner.run(evaluator,"Create a caption about ai agents post")
      
      answer = await Runner.run(evaluator,result.final_output)
       
      if answer.final_output == "pass" or answer.final_output == "good":
         caption = result.final_output
         print(caption)
         break
             
    
await run_agents()