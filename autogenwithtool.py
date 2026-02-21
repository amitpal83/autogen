import asyncio

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.http import HttpTool
import os
from dotenv import load_dotenv
from json_schema_to_pydantic import create_model 
from autogen_core.tools import Tool
import logging


load_dotenv()

openapikey = os.getenv("OPENAI_API_KEY")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("agent")

model = OpenAIChatCompletionClient(model = 'gpt-4o', api_key=openapikey)

# Define a JSON schema for a base64 decode tool
base64_schema = {
    "type": "object",
    "properties": {
        "value": {"type": "string", "description": "The base64 value to decode"},
    },
    "required": ["value"],
}

# Create an HTTP tool for the httpbin API
base64_tool = HttpTool(
    name="base64_decode",
    description="base64 decode a value",
    scheme="https",
    host="httpbin.org",
    port=443,
    path="/base64/{value}",
    method="GET",
    json_schema=base64_schema,
)

original_run = base64_tool.run

async def logged_run(*args, **kwargs):
    logger.info(f"Tool called: {base64_tool.name}")
    logger.info(f"Arguments: {kwargs}")
    result = await original_run(*args, **kwargs)
    logger.info(f"Result: {result}")
    return result

base64_tool.run = logged_run



async def main():
    # Create an assistant with the base64 tool
   
    assistant = AssistantAgent("base64_assistant", model_client=model, tools=[base64_tool ])

    # The assistant can now use the base64 tool to decode the string
    response = await assistant.on_messages(
        [TextMessage(content="Can you base64 decode the value 'YWJjZGU=', please?", source="user")],
        CancellationToken(),
    )
    print(response.chat_message)


asyncio.run(main())