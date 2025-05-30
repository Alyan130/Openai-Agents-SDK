from agents import Agent,function_tool,Runner,set_tracing_disabled,AsyncOpenAI,OpenAIChatCompletionsModel,RunContextWrapper
import dotenv
import os
import chainlit as cl
import requests

dotenv.load_dotenv()
API_KEY = os.getenv("GEMINI_KEY")

set_tracing_disabled(disabled=True)

client = AsyncOpenAI(
    api_key=API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=client
)


@function_tool
def user_info():
   '''This tool returns user details other wise returns no details found.

  output: 
  user_data - > user details
  '''
   response = requests.get("https://6782dda2c51d092c3dd10b28.mockapi.io/categories")
   users = response.json()
   my_user = cl.user_session.get("user")
   for user in users:
     if user["user_name"].lower() == my_user.identifier.lower():
        user_data = f'''
        Name = {user["user_name"]}
        Card Name = {user["card_name"]}
        Account Name = {user["account_number"]}
        CNIC = {user["cnic_number"]}
        Account Type = {user["account_type"]}
        ''' 
        cl.user_session.set("balance",user["account_balance"])
        return user_data
   else:
      return "No user found with that name"
   


@function_tool
def check_balance():
   "This tool checks the balance of user and returns it, if balance is none it said you have no cash"
   balance = cl.user_session.get("balance")
   print(balance)
   return f"Your current balance is {balance}."


@function_tool
def transaction(amount:int):
  '''This tool takes amount by the user and makes transaction from available balance if available balance is enough for transaction then it shows transaction succesfull with remaining balance otherwise unsuccessfull 
  '''
  balance = cl.user_session.get("balance")
  if balance >= amount:
     balance-=amount

     return f"Transaction Successfull your current balance is {balance}"
  else:
    return f"Transation Unsuccessfull"


@function_tool
def about_bank():
  '''This tool provides bank information to the user'''
  return f"Our Bank ENVO is a the top ranked bank in Pakistan."


banking_agent=Agent(
    name="Banking agent",
    instructions='''Your are Bank assistant that chat with bank user and respons their queries
    Your have three tools 
    1) check_balance : that checks the balance of user and returns it
    2)transaction : that performs transactions based on user given amount
    3) about_bank : that provides information about bank 
    4) user_info : that check user from list of available user and provide user details such as user_name, card_number, account_name, cnic_number and account_type,account_balance ,if the balance is not set or is None, always call <function_call>user_info</function_call> first to fetch the balance dont ask from user. 
    user details must be in a format like this:
        Name = 
        Card Name = 
        Account Name = 
        CNIC = 
        Account Type =
    You have access to past conversations and tell user previous messages.
    ''',
    model=model,
    tools=[check_balance,transaction,about_bank,user_info]
)

@cl.password_auth_callback
def authentication(email:str, password:str):
   response = requests.get("https://6782dda2c51d092c3dd10b28.mockapi.io/categories")
   users = response.json()
   
   for user in users:
     if email.lower() == user["email"].lower() and password == user["password"]:
          return cl.User(
             identifier=user["user_name"],
             metadata={"role":"user","provider":"credentials"}
          )
   else:
      return None

          

@cl.on_chat_start
async def start_chat():
   cl.user_session.set("history",[])
   authenticated_user = cl.user_session.get("user")
   
   if authenticated_user: 
     await cl.Message(content=f"Hello {authenticated_user.identifier}, weclome to ENVO bank how can i help you today?").send()
   else:
     await cl.Message(content="Authenticated falied!").send()



@cl.on_message
async def run_agent(message:cl.Message):

 history = cl.user_session.get("history")
 history.append({"role":"user","content":message.content})

 msg= cl.Message(content="🤔 Thinking!")
 await msg.send()

 result = await Runner.run(
   banking_agent,
   input=history
 )

 history.append({"role":"assistant","content":result.final_output})
 await cl.Message(content=result.final_output).send()
 

