import os
from crewai import Agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

# Model Initialize
llm = ChatOpenAI(model=os.getenv("OPENAI_MODEL_NAME", "gpt-4o"), temperature=0.2)

# Agent 1: Scanner
scanner_agent = Agent(
    role="Senior Code Security and Bug Auditor",
    goal="Scan the given Python code file for logic errors, runtime bugs, and edge-case crashes.",
    backstory="You are an expert static analysis engine. You read code structural lines meticulously.",
    verbose=True,
    llm=llm,
    allow_code_execution=False  # <--- YEH LINE CHROMA CO CRASH HONE SE BACHAYEGI
)

# Agent 2: Patch Programmer
patch_agent = Agent(
    role="Principal Software Engineer",
    goal="Write robust, clean, and production-ready Python patches to fix identified bugs.",
    backstory="You are a veteran software engineer. You write highly optimized code.",
    verbose=True,
    llm=llm,
    allow_code_execution=False  # <--- YEH LINE CHROMA CO CRASH HONE SE BACHAYEGI
)
