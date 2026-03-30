from crewai import Task
from agents import triage_agent, retriever_agent, writer_agent, auditor_agent, fraud_redactor_agent

def create_tasks(ticket_text: str, order_context: dict):
    redaction_task = Task(
        description=f"Analyze the incoming ticket: '{ticket_text}'. Redact any sensitive personal information (like credit card numbers or passwords) by replacing them with [REDACTED]. If no PII is found, return the original text.",
        expected_output="The redacted ticket text.",
        agent=fraud_redactor_agent
    )
    
    triage_task = Task(
        description=f"Analyze the redacted ticket from the previous task.\nOrder Context: {order_context}\n\n1. Classify the issue type.\n2. Note any missing critical field (e.g. if a refund is requested but order_status is missing).\nOutput up to 3 Clarifying Questions if info is missing, else just output the classification.",
        expected_output="Classification: Issue Type + Confidence.\nClarifying Questions: 1,2,3 (or None).",
        agent=triage_agent
    )
    
    retrieval_task = Task(
        description="Using the Triage classification and the ticket details, search the policy database for relevant rules. Consider exceptions (like perishable items or region laws).",
        expected_output="A block of raw policy text with citations [Source | Section]. If no policy applies, declare 'Not in policy'.",
        agent=retriever_agent
    )
    
    writing_task = Task(
        description="Draft a response. Output format MUST be:\nClassification:\nClarifying Questions:\nDecision: approve/deny/partial/needs escalation\nRationale: (based strictly on policy)\nCitations: (bullet list [Source | Section])\nCustomer Response Draft:\nNext Steps/Internal Notes:",
        expected_output="A structured resolution strictly adhering to the output format, with no hallucinated policies.",
        agent=writer_agent
    )
    
    auditing_task = Task(
        description="Verify the structured resolution. Look at the Decision and Rationale. Does the cited policy actually support this? Are the [Source | Section] citations present? If it lies or invents rules, change the Decision to 'escalate' and fix the draft.",
        expected_output="The final, audited, perfectly formatted structured resolution.",
        agent=auditor_agent
    )
    
    return [redaction_task, triage_task, retrieval_task, writing_task, auditing_task]
