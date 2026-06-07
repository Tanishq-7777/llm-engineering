import os
import json
from dotenv import load_dotenv
from scraper import fetch_website_contents, fetch_website_links
from openai import OpenAI
from fastapi import FastAPI

app = FastAPI()

load_dotenv()

apikey = os.getenv("OPENAI_API_KEY")

if not apikey:
    print("No API key found")
openai = OpenAI()
model = "gpt-4.1"






link_system_prompt = """
You are provided with a list of links found on a webpage.
You are able to decide which of the links would be most relevant to include in a brochure about the company,
such as links to an About page, or a Company page, or Careers/Jobs pages.

You should response in a JSON as in this example:

{
    "links":[
        {
            "type":"about page",
            "url":"https://full.url/goes/here/about"
        },
        {
            "type":"contact page",
            "url":"https://another.full.url/careers"
        }
    ]
}

"""

def get_links_user_prompt(url):
    user_prompt = f""" 
    Here is the list of links on the website {url} -
    Please decide which of these are relevant web links for a brochure about the company, 
    respond with the full https URL in JSON format.
    Do not include Terms of Service, Privacy, email links.

    Links  (some might be relevant links):
    """
    links = fetch_website_links(url)
    user_prompt += "\n".join(links)
    return user_prompt


def select_relevant_links(url):
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {
                "role":"system","content":link_system_prompt
            },
            {
                "role":"user","content":get_links_user_prompt(url)
            }
        ],
        response_format={"type":"json_object"}
    )
    result =  response.choices[0].message.content
    links = json.loads(result)
    return links;


def fetch_page_and_all_relevant_links(url):
    content = fetch_website_contents(url)
    relevant_links = select_relevant_links(url)
    result = f"## Landing Page:\n\n{content}\n## Relevant Links:\n"


    for link in relevant_links["links"]:
        result += f"\n\n### Link: {link['type']}\n"
        result += fetch_website_contents(link["url"])
    
    return result

brochure_system_prompt = """
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
Include details of company culture, customers and careers/jobs if you have the information.
"""
brochure_system_prompt = """
You are an assistant that analyzes the contents of several relevant pages from a company website
and creates a short brochure about the company for prospective customers, investors and recruits.
Respond in markdown without code blocks.
Include details of company culture, customers and careers/jobs if you have the information.
"""

        
def get_brochure_user_prompt(company_name, url):
    user_prompt = f"""
    You are looking at a company called: {company_name}
    Here are the contents of its landing page and other relevant pages;
    use this information to build a short brochure of the company in markdown without code blocks.\n\n
    """
    user_prompt += fetch_page_and_all_relevant_links(url)
    user_prompt = user_prompt[:4000]
    return user_prompt

def create_brochure(company_name,url):
    response = openai.chat.completions.create(
        model="gpt-5-nano",
        messages = [{"role":"system","content":brochure_system_prompt},
                    {"role":"user","content":get_brochure_user_prompt(company_name,url)}],
        # use stream and try that line by line feature
        stream=True
    )

    for chunk in response:
        token = chunk.choices[0].delta.content
        if token:
            yield token 

# print(create_brochure("huggingface","https://huggingface.co"))



def open_ai_call():
    response = openai.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "hey."}
        ],
        stream=True
    )
    for chunk in response:
        token = chunk.choices[0].delta.content
        if token:
            yield token
