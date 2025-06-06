from agents import Agent, Runner, AsyncOpenAI,OpenAIChatCompletionsModel, set_tracing_disabled, function_tool
import requests
from bs4 import BeautifulSoup
import streamlit as st

set_tracing_disabled(disabled=True)

API_KEY = st.secrets["API_KEY"]

provider = AsyncOpenAI(
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    api_key= API_KEY
)

model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client=provider
)


@function_tool
def portfolio_scraper(url):
  '''
   This tool visits on potfolio website based on url and scrapes the content

   Args:
   url: str -> Link to scrape then content from

   return:
   text: str -> text of scraped content
  '''
  response = requests.get(url)
  soup = BeautifulSoup(response.text,"html.parser")
  return soup.text



@function_tool
def scrape_github_profile(username):
    '''
     This tool scrapes content from github profile based on username and return scraped data
     in dictionary.

     Args:
      username: str -> github profile username

     Return:
      scraped_data: dict -> scraped data from github profile

    '''
    url = f"https://github.com/{username}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return {"error": f"Failed to fetch profile: {response.status_code}"}

    soup = BeautifulSoup(response.text, "html.parser")

    name_tag = soup.select_one("h1.vcard-names span.p-name")
    name = name_tag.text.strip() if name_tag else None

    bio_tag = soup.select_one("div.p-note")
    bio = bio_tag.text.strip() if bio_tag else None


    website_tag = soup.select_one('li[itemprop="url"] a')
    website = website_tag.get("href") if website_tag else None


    location_tag = soup.select_one('li[itemprop="homeLocation"] span')
    location = location_tag.text.strip() if location_tag else None


    repo_count_tag = soup.select_one("a[href$='?tab=repositories'] span.Counter")
    repo_count = repo_count_tag.text.strip() if repo_count_tag else "0"

    stars_tag = soup.select_one("a[href$='?tab=stars'] span.Counter")
    stars = stars_tag.text.strip() if stars_tag else "0"

    projects_tag = soup.select_one("a[href$='?tab=projects'] span.Counter")
    projects = projects_tag.text.strip() if projects_tag else "0"

    following = soup.select_one("a[href$='?tab=following'] span.color-fg-default")

    followers = soup.select_one("a[href$='?tab=followers'] span.color-fg-default")

    poupular_repos = soup.select("span.repo")
    repos = [repo.text.strip() for repo in poupular_repos]


    social_links = []
    social_items = soup.select("ul.vcard-details li a[href]")
    for item in social_items:
        href = item.get("href", "")
        if href.startswith("http"):
            social_links.append(href)

    return {
        "username": username,
        "name": name,
        "bio": bio,
        "website": website,
        "location": location,
        "repositories": repo_count,
        "stars": stars,
        "projects": projects,
        "followers":followers.text,
        "following":following.text,
        "links":social_links[1:],
        "popular_repos":repos,
    }  

profile_agent = Agent(
    name="Profile Analyzer Agent",
    instructions='''
You are a professional Profile Analyzer Agent created by Alyan Ali, designed to evaluate individuals' professional presence and generate personalized suggestions.

-Only give suggestions, no extra messages or explanations.

-You can be given one or more of the following inputs:
A portfolio website URL
A GitHub username
The content of a CV file

-You have access to the following tools:
portfolio_scraper(url) – Extracts text content from portfolio websites
scrape_github_profile(username) – Retrieves public data from a GitHub profile
Never mention or display which tool was used.


-Output must include:
Brief Summary
Strengths
Areas of Improvement
Tips and Recommendations in bullet format

-Use the following headings:
GitHub Profile Analysis
Portfolio Website Feedback
CV Evaluation

-General Recommendations
Use only ASCII-compatible characters such as hyphens (-) and asterisks (*)
Do not use Unicode characters (like • \u2022)
Ensure full Latin-1 (ISO-8859-1) compatibility
Be concise but insightful
Do not guess, assume, or generate content if no input was provided
If an input is missing or unreadable, mention it briefly and continue with available data

-Sample Output:
GitHub Profile Analysis  
- Strengths:  
  - Good commit frequency across multiple repos  
  - Clear project descriptions  
- Suggestions:  
  - Add README files for key repositories  
  - Pin most relevant repos to showcase skills

Portfolio Website Feedback  
- Strengths:  
  - Clean layout and easy navigation  
- Suggestions:  
  - Include case studies or project breakdowns  
  - Add downloadable resume or contact form

CV Evaluation  
- Strengths:  
  - Well-structured experience timeline  
- Suggestions:  
  - Avoid long paragraphs and use of bullet points  
  - Add metrics to demonstrate impact

-Extra suggestion may be added briefly:
     Technical_Skills
     Projects_Quality
     GitHub_Activity 
     Portfolio_Presentation
     Resume_Strength
   ''',
   model=model
)


async def run_agent(prompt):
    result =await Runner.run(profile_agent,prompt)
    return result.final_output