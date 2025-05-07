from langchain.agents import AgentExecutor, create_react_agent
from langchain import hub
from app.core.config import settings
import os

# LLM Setup
def get_llm():
    if settings.LLM_TYPE.lower() == "gpt-4":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="gpt-4-turbo-preview",  # or "gpt-4"
            temperature=0.3,
            openai_api_key=settings.OPENAI_API_KEY
        )
    else:
        raise ValueError(f"Unsupported LLM type: {settings.LLM_TYPE}")

# Agent Setup
def create_agent_executor():
    from .tools import get_price_estimate, fetch_technical_specs
    
    tools = [get_price_estimate, fetch_technical_specs]
    llm = get_llm()
    
    prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm, tools, prompt)
    
    return AgentExecutor(agent=agent, tools=tools, verbose=True)