from dotenv import load_dotenv
import os
from tavily import TavilyClient  # type: ignore

_ = load_dotenv()

client = TavilyClient(api_key=os.environ.get("TAVILY_API_KEY"))

result = client.search("What's Nvidia's new Blackwell GPU?", include_answer=True)

print(result['answer'])

# Regular Search

city = "Tbilisi"

query = f"""
    What is the current weather in {city}?
    Should I travel there today?
    "weather.com"
"""

import requests
from bs4 import BeautifulSoup
from ddgs import DDGS
import re

ddg = DDGS()

def search(query, max_results=3):
    results = ddg.text(query, max_results=max_results)
    return [i['href'] for i in results]

for i in search(query):
    print(i)

def scrape_weather_info(url):
    """Scrape content from the given URL"""
    if not url:
        return "Weather information could not be found."

    headers = {'User-Agent': 'Mozila/5.0'}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return "Failed to retrieve the webpage"

    soup = BeautifulSoup(response.text, "html.parser")
    return soup

url = search(query)[0]

soup =  scrape_weather_info(url)

print(f"Website: {url}\n\n")
print(soup)

# parse HTML for better understanding

weather_data = []
for tag in soup.find_all(['h1', 'h2', 'h3', 'p']):
    text = tag.get_text(" ", strip=True)
    weather_data.append(text)

weather_data = '\n'.join(weather_data)

print(f"Website: {url}\n\n")
print(weather_data)

# ----- Agentic Search

import json, ast
from pygments import highlight, lexers, formatters

result = client.search(query, max_results=1)

if not result['results']:
    print("No results")
else:
    data = result['results'][0]['content']

    # handle both cases: already a dict, or a string
    parsed = ast.literal_eval(data) if isinstance(data, str) else data

    formatted = json.dumps(parsed, indent=4)
    print(highlight(formatted, lexers.JsonLexer(), formatters.TerminalFormatter()))