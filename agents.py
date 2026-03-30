import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

from crewai import Agent
from tools import PolicySearchTool

# CrewAI uses litellm under the hood, so passing the model string works natively
gemini_llm = "gemini/gemini-2.5-flash"

policy_tool = PolicySearchTool()

fraud_redactor_agent = Agent(
    role="Fraud and PII Redactor",
    goal="Scan the customer ticket and redact any sensitive personal information such as credit card numbers, passwords, or explicit fraud indicators.",
    backstory="You are a strict security and privacy guard. You scrub all incoming communications to protect customer data before it hits the support system.",
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

triage_agent = Agent(
    role="Support Ticket Triage Agent",
    goal="Classify the incoming customer ticket issue type (e.g. refund, shipping, payment, promo, fraud). Identify if vital order context is missing (like order date or order status).",
    backstory="You are the first line of defense. You categorize tickets accurately and ensure the customer provided enough context to process their request.",
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

retriever_agent = Agent(
    role="Policy Retriever Agent",
    goal="Search the internal policy knowledge base to find rules that apply to the customer's issue. You MUST return exact excerpts and their [Source | Section] markers.",
    backstory="You are a meticulous policy wonk. You don't make assumptions. You only provide text found in the official guidelines using your search tool.",
    tools=[policy_tool],
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

writer_agent = Agent(
    role="Resolution Writer Agent",
    goal="Draft the final customer-facing response to the ticket. You must completely base your decision on the policies handed to you by the Retriever.",
    backstory="You are a polite but firm customer support agent. You use empathy, but you NEVER invent policy or offer refunds that aren't grounded in the rules.",
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)

auditor_agent = Agent(
    role="Compliance and Safety Auditor",
    goal="Review the Resolution Writer's draft. Force a rewrite or trigger an 'Escalation' if the draft contains unsupported statements, hallucinates a refund, or is missing [Source | Section] citations.",
    backstory="You are an uncompromising auditor. Your sole job is to protect the company from agents who invent friendly policies. Any unsupported policy claim must be blocked.",
    llm=gemini_llm,
    verbose=True,
    allow_delegation=False
)
