import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
import os
from dotenv import load_dotenv
from autogen_agentchat.messages import TextMessage
from autogen_core.models import UserMessage


load_dotenv()

openapikey = os.getenv("OPENAI_API_KEY")

model_client = OpenAIChatCompletionClient(model = 'gpt-4o', api_key=openapikey)

firstagent = AssistantAgent(model_client=model_client, name="FirstAgent", description="An agent that answers questions about world capitals.")

async def astest():
    result = await model_client.create(
        messages=[
            UserMessage(content="What is the capital of Zimbabwe?", source="user")
        ]
    )
    print(result)







# Async runner

async def beforemain():
    response = await firstagent.run(
        task=TextMessage(content="What is the Capital of South Africa?", source="user")
    )
    print(response)

async def main():
    response = await firstagent.run(
        task=TextMessage(content="What is the Capital of Greece?", source="user")
    )
    print(response)

async def secondquestion():
    response = await firstagent.run(
        task=TextMessage(content="What is the last 2 questions i asked?", source="user")
    )
    print(response)    

async def saveState( firstagent: AssistantAgent):
    agentStatejson = await firstagent.save_state()
    print(f"Agent state is",agentStatejson)    

asyncio.run(astest())
asyncio.run(beforemain())
asyncio.run(main())
asyncio.run(secondquestion())
asyncio.run(saveState(firstagent))



