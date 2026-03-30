import os
from dotenv import load_dotenv
from crewai import Crew, Process
from tasks import create_tasks
from agents import triage_agent, retriever_agent, writer_agent, auditor_agent, fraud_redactor_agent

class SupportBotCrew:
    def __init__(self, ticket_text: str, order_context: dict):
        dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
        load_dotenv(dotenv_path=dotenv_path)
        self.ticket_text = ticket_text
        self.order_context = order_context
        
    def kickoff(self):
        tasks_list = create_tasks(self.ticket_text, self.order_context)
        crew = Crew(
            agents=[fraud_redactor_agent, triage_agent, retriever_agent, writer_agent, auditor_agent],
            tasks=tasks_list,
            verbose=True,
            process=Process.sequential
        )
        return crew.kickoff()

if __name__ == "__main__":
    test_ticket = "My order arrived late and the cookies are melted. I want a full refund and to keep the item."
    test_context = {
        "order_date": "2023-10-01",
        "delivery_date": "2023-10-08",
        "item_category": "perishable",
        "fulfillment_type": "first-party",
        "shipping_region": "New York",
        "order_status": "delivered",
        "payment_method": "credit_card"
    }
    
    crew_instance = SupportBotCrew(test_ticket, test_context)
    result = crew_instance.kickoff()
    print("=== FINAL RESOLUTION ===")
    print(result)
