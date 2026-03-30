import os
import re
import time
from crew import SupportBotCrew

cases = [
    # --- 8 Standard Cases ---
    {"type": "standard", "t": "I changed my mind and want to return this blender. Unopened.", "ctx": {"order_date": "2023-10-01", "delivery_date": "2023-10-05", "item_category": "Home Goods", "status": "delivered"}},
    {"type": "standard", "t": "Where is my package? It was supposed to be here 10 days ago.", "ctx": {"order_date": "2023-10-01", "delivery_date": "2023-10-05", "item_category": "Books", "status": "shipped"}},
    {"type": "standard", "t": "I received the wrong item in my box.", "ctx": {"order_date": "2023-11-01", "delivery_date": "2023-11-03", "item_category": "Electronics", "status": "delivered"}},
    {"type": "standard", "t": "I want to cancel my order before it ships.", "ctx": {"order_date": "2023-11-01", "delivery_date": "", "item_category": "Apparel", "status": "placed"}},
    {"type": "standard", "t": "The box arrived but it was crushed and the phone case inside is broken.", "ctx": {"order_date": "2023-11-01", "delivery_date": "2023-11-04", "item_category": "Accessories", "status": "delivered"}},
    {"type": "standard", "t": "Why didn't my coupon work? It said 20% off.", "ctx": {"order_date": "2023-11-01", "delivery_date": "", "item_category": "Apparel", "status": "placed", "coupon_used": "EXPIRED20"}},
    {"type": "standard", "t": "I want to return these jeans. Still have tags.", "ctx": {"order_date": "2023-11-01", "delivery_date": "2023-11-05", "item_category": "Apparel", "status": "delivered"}},
    {"type": "standard", "t": "Return request for an unopened laptop.", "ctx": {"order_date": "2023-11-01", "delivery_date": "2023-11-05", "item_category": "Electronics", "status": "delivered"}},

    # --- 6 Exception-Heavy Cases ---
    {"type": "exception", "t": "The cookies arrived melted. I want a refund.", "ctx": {"order_date": "2023-11-01", "delivery_date": "2023-11-05", "item_category": "Perishable", "status": "delivered"}},
    {"type": "exception", "t": "I opened this TV but I don't like the picture quality. I want to return it.", "ctx": {"order_date": "2023-11-01", "delivery_date": "2023-11-05", "item_category": "Electronics", "status": "delivered"}},
    {"type": "exception", "t": "Returning these underwear, they don't fit.", "ctx": {"order_date": "2023-11-01", "delivery_date": "2023-11-05", "item_category": "Apparel", "status": "delivered"}},
    {"type": "exception", "t": "I bought this shirt on Final Sale clearance. Can I exchange for a different color?", "ctx": {"order_date": "2023-11-01", "delivery_date": "2023-11-05", "item_category": "Apparel", "status": "delivered", "sale_type": "Final Sale"}},
    {"type": "exception", "t": "Please refund the $5 California electronics fee. I'm returning the item.", "ctx": {"order_date": "2023-11-01", "delivery_date": "2023-11-05", "item_category": "Electronics", "shipping_region": "California", "status": "delivered"}},
    {"type": "exception", "t": "Cancel my order from yesterday. It says shipped but I don't want it.", "ctx": {"order_date": "2023-11-01", "item_category": "Home Goods", "status": "shipped"}},

    # --- 3 Conflict Cases (Marketplace / Regional rules override general rules) ---
    {"type": "conflict", "t": "I live in France (EU) and I opened this laptop. I want to return it within 10 days.", "ctx": {"order_date": "2023-11-01", "delivery_date": "2023-11-05", "item_category": "Electronics", "shipping_region": "EU", "status": "delivered"}},
    {"type": "conflict", "t": "I want to return this third-party marketplace speaker. Your policy says 30 days.", "ctx": {"order_date": "2023-11-01", "delivery_date": "2023-11-05", "item_category": "Electronics", "fulfillment_type": "marketplace seller", "status": "delivered"}},
    {"type": "conflict", "t": "I'm returning an opened monitor. Oh also, I'm an EU citizen living in California right now.", "ctx": {"order_date": "2023-11-01", "delivery_date": "2023-11-05", "item_category": "Electronics", "shipping_region": "California", "status": "delivered"}},

    # --- 3 Not In Policy / Out of bounds ---
    {"type": "not_in_policy", "t": "I want a refund because my astrologer told me not to buy this.", "ctx": {"status": "delivered", "item_category": "Books"}},
    {"type": "not_in_policy", "t": "Do you sell dog food? I want to buy some with my refund.", "ctx": {"status": "delivered"}},
    {"type": "not_in_policy", "t": "Can I return this laptop I bought 5 years ago?", "ctx": {"delivery_date": "2018-01-01", "status": "delivered", "item_category": "Electronics"}}
]

def run_evaluation():
    print(f"Running Evaluation over 2 Support Tickets...")
    
    citations_present = 0
    escalation_correct = 0
    total = 2

    if not os.environ.get("GEMINI_API_KEY"):
         print("Warning: No GEMINI_API_KEY provided. Ensure you have your Google Gemini API key set in your .env file.")

    reports = []
    
    for i, test in enumerate(cases[:2]):
        print(f"\n--- Running Ticket {i+1}/{total} [{test['type']}] ---")
        try:
            crew = SupportBotCrew(test['t'], test['ctx'])
            output = str(crew.kickoff())
            
            has_citation = bool(re.search(r"\[.*?\|.*?\]", output))
            if has_citation:
                citations_present += 1
                
            has_escalation = "escalat" in output.lower() or "deny" in output.lower()
            if test['type'] in ["conflict", "not_in_policy"] and has_escalation:
                escalation_correct += 1

            reports.append(f"Ticket {i+1} ({test['type']})\nTicket: {test['t']}\nContext: {test['ctx']}\nOutput:\n{output}\nHas Citation: {has_citation}\n{'-'*40}")
            
        except Exception as e:
            print(f"Error on Test {i+1}: {e}")
            reports.append(f"Error on Test {i+1}: {e}")
        
        # Adding a comprehensive 60-second sleep to prevent hitting Gemini's strict 5 RPM free tier limit
        if i < total - 1:
            print(f"Sleeping for 60 seconds to respect Google API rate limits...")
            time.sleep(60)

    coverage_rate = (citations_present / total) * 100
    expected_escalations = len([c for c in cases if c['type'] in ['conflict', 'not_in_policy']])
    escalation_rate = (escalation_correct / expected_escalations) * 100

    summary = f"""
=============================================
SUPPORT BOT EVALUATION REPORT
=============================================
Total Tickets Processed: {total}
Citation Coverage Rate: {coverage_rate:.2f}% ({citations_present}/{total})
Correct Escalation/Denial Rate (Exceptions & Conflicts): {escalation_rate:.2f}% ({escalation_correct}/{expected_escalations})
=============================================
"""
    print(summary)
    with open("evaluation_report.txt", "w") as f:
        f.write(summary)
        for r in reports:
             f.write(f"\n{r}")
             
    print("Report saved to evaluation_report.txt")

if __name__ == "__main__":
    run_evaluation()
