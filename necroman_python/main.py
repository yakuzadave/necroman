import os
from typing import List

from fastapi import FastAPI

# from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema import BaseOutputParser
from langserve import add_routes
from dotenv import load_dotenv
load_dotenv()
# OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
OPENAI_API_KEY= os.getenv("OPENAI_API_KEY")
# 1. Chain definition

import json
import openai
import requests
from tenacity import retry, wait_random_exponential, stop_after_attempt
from termcolor import colored


static_files_dir = Path(__file__).parent / "static"


GPT_MODEL = "gpt-3.5-turbo-0613"


class CommaSeparatedListOutputParser(BaseOutputParser[List[str]]):
  """Parse the output of an LLM call to a comma-separated list."""

  def parse(self, text: str) -> List[str]:
    """Parse the output of an LLM call."""
    return text.strip().split(", ")


def get_home_page():
  template = """You are a helpful assistant who greets new users visiting the website. Generate a welcome message for a user visiting the home page of a website for the first time."""
  human_template = """Hello, my name is Dave"""
  chat_prompt = ChatPromptTemplate.from_messages([
      ("system", template),
      ("human", human_template),
  ])
  return chat_prompt


def get_example_prompts():
  template = """You are a helpful assistant who generates comma separated lists.  A user will pass in a category, and you should generate 5 objects in that category in a comma separated list.  ONLY return a comma separated list, and nothing more."""
  human_template = "{text}"
  chat_prompt = ChatPromptTemplate.from_messages([
      ("system", template),
      ("human", human_template),
  ])
  return chat_prompt


def generate_gang_list_prompt(faction: str, points: int):
  template = """You are a helpful assistant who generates a gang list for the tabletop game of Necromunda ny Games Workshop. Ylu will be provided with the point value and the faction of the desired Necromunda gang and you will return the generated gang, including, members, skills, stats and equipment in JSON format."""
  human_template = f"I would like you to create a gang list for the {faction} faction using {points} points"
  chat_prompt = ChatPromptTemplate.from_messages([
      ("system", template),
      ("human", human_template),
  ])
  return chat_prompt


home_chain = get_home_page() | ChatOpenAI()

category_chain = get_example_prompts() | ChatOpenAI(
) | CommaSeparatedListOutputParser()

# 2. App definition
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces",
)

app.mount("/static", StaticFiles(directory=static_files_dir), name="static")



# @app.get("/")
@app.get("/", response_class=HTMLResponse)
def home_page():
    html_file = static_files_dir / "index.html"
    return HTMLResponse(html_file.read_text())
    
  # return "Server is running"
    


# 3. Adding chain routes

# add_routes(app, home_chain, path="")

add_routes(
    app,
    category_chain,
    path="/category_chain",
)

if __name__ == "__main__":
  import uvicorn
  uvicorn.run(app, host="0.0.0.0", port=8000)
# uvicorn.run(app, host="localhost", port=8000)
