from profile_agent import model
from agents import Runner , Agent
from pydantic import BaseModel


class ChartValues(BaseModel):
  Technical_Skills:int
  Projects_Quality:int
  GitHub_Activity:int
  Portfolio_Presentation:int
  Resume_Strength:int


chart_agent = Agent(
     name="Chart Agent",
     instructions='''
     Analyze the feedback suggestions from user profile report and assign a score (0-10) to the following aspects:
     1. Technical_Skills
     2. Projects_Quality
     3. GitHub_Activity 
     4. Portfolio_Presentation
     5. Resume_Strength

     Must give score to all of them.
     ''',
    model=model,
    output_type=ChartValues
)

async def run_chart_agent(suggestions):
  result = await Runner.run(chart_agent,suggestions)
  output = {
  "Technical_Skills":result.final_output.Technical_Skills,
  "Projects_Quality":result.final_output.Projects_Quality,
  "GitHub_Activity":result.final_output.GitHub_Activity,
  "Portfolio_Presentation":result.final_output.Portfolio_Presentation,
  "Resume_Strength":result.final_output.Resume_Strength,
  }
  return output
    