from agents import Agent, Runner,set_tracing_disabled,AsyncOpenAI,OpenAIChatCompletionsModel,RunContextWrapper
from pydantic import BaseModel
import asyncio
import chainlit as cl
from agents import GuardrailFunctionOutput, input_guardrail, output_guardrail,InputGuardrailTripwireTriggered,OutputGuardrailTripwireTriggered
set_tracing_disabled(disabled=True)
import os
from dotenv import load_dotenv

load_dotenv()

external_client = AsyncOpenAI(
    api_key = os.getenv("API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
      model="gemini-1.5-flash",
      openai_client= external_client
)


class Education(BaseModel):
   is_educational:bool
   reason:str
  
class LlmOutput(BaseModel):
   is_aggressive:bool
   reason:str

education_guardraill = Agent(
    name="Educational guardraill agent",
    instructions="Your job is to determine whether a user input is related to educational topics such as science, math, technology, history, literature, language learning, or any academic subject.",
    output_type=Education,
    model=model
)

agent_output_guradraill = Agent(
    name="Output checking assistant",
    instructions = "Your job is to determine whether the message is written in a polite, soft, and non-aggressive tone.",
    output_type=LlmOutput,
    model=model
)


@input_guardrail
async def check_education(
  ctx:RunContextWrapper , agent:Agent, input:str )->GuardrailFunctionOutput:
    result = await Runner.run(education_guardraill,input,context=ctx.context)
    
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= not result.final_output.is_educational
    )


@output_guardrail
async def check_output(
    ctx:RunContextWrapper, agent:Agent , output:str)->GuardrailFunctionOutput:
    result = await Runner.run(agent_output_guradraill,output,context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered=result.final_output.is_aggressive
    )

  

agent = Agent(
    name="Educational Assistant",
    instructions="You are assitant that assists students for educational purposes.Your reponse must be short and concise.",
    input_guardrails=[check_education],
    output_guardrails= [check_output],
    model= model,
    )


@cl.on_chat_start
async def chat_start():
   await cl.Message(content="How can I assist you today!").send()


@cl.on_message
async def main(message:cl.Message):
   
   await cl.Message(content="Thinking!").send()

   try:
      result = await Runner.run(agent,message.content) 
      await cl.Message(content=result.final_output).send()
   
   except InputGuardrailTripwireTriggered:
     await cl.Message(content="Your question is not educational!").send()  

    
   except OutputGuardrailTripwireTriggered:
     await cl.Message(content="I am extreemly sorry for not giving answer to you.").send()

       


