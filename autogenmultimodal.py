import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv
from autogen_agentchat.messages import TextMessage
from autogen_core.models import UserMessage
import PIL
import requests
from autogen_agentchat.messages import MultiModalMessage
from autogen_core import Image
from io import BytesIO

load_dotenv()

openapikey = os.getenv("OPENAI_API_KEY")

model_client = OpenAIChatCompletionClient(model = 'gpt-4o', api_key=openapikey)

firstagent = AssistantAgent(model_client=model_client, name="FirstAgent", description="An agent that takes multimodal input and answers questions about the input")


# Create a multi-modal message with random image and text.
pil_image = PIL.Image.open(BytesIO(requests.get("https://picsum.photos/id/243/300/200").content))
img = Image(pil_image)
pil_image.show()
 


async def main():
    response = await firstagent.run(
        task=MultiModalMessage(content=["Can you describe the content of this image?", img], source="user")
    )
    print(response)

asyncio.run(main())    

