import os
from openai import OpenAI
from dotenv import load_dotenv
from scraper import fetch_website_contents
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


openai = OpenAI(api_key=api_key)


tani = fetch_website_contents("https://edwarddonner.com")

system_prompt = """
You are a snarky assistant that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""
user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.

"""
def messages_for(website):
    return [{"role":"system","content":system_prompt},{"role":"user","content":user_prompt_prefix + website}]
    

def summarize(url):
    website = fetch_website_contents(url)
    response = openai.chat.completions.create(
        model = "gpt-4.1-mini",
        messages = messages_for(website)
    )
    return response.choices[0].message.content
print(summarize("https://cnn.com"))