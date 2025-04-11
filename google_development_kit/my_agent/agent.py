# my_agent/agent.py
import os
from google.adk.agents import Agent
from google.adk.tools import google_search

# Get the API key from environment variables
api_key = os.environ.get("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(
        "The GOOGLE_API_KEY environment variable must be set. "
        "Get an API key from the Google Cloud AI Platform or MakerSuite."
    )

root_agent = Agent(
    name="search_assistant",
    model="gemini-2.0-flash-exp", # Or your preferred Gemini model
    instruction="You are a helpful assistant. Answer user questions using Google Search when needed.",
    description="An assistant that can search the web.",
    tools=[google_search]
)