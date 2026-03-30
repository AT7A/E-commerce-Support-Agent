# Example Agent Resolutions

Below are 3 representative outputs from the e-commerce agent system detailing their reasoning pathways for exception handling, conflict escalation, and absent policy logic (abstention).

## Example 1: Exception Handled Correctly
*Ticket*: "The cookies arrived melted. I want a refund."
*Context*: Perishable Item. Delivered Nov 5th. 
```text
=== AGENT OUTPUT ===
Classification: Refund Request (Exception) | Confidence: 95%
Clarifying Questions: None

Decision: Deny
Rationale: According to the Perishable Goods policy, food and flowers are explicitly Final Sale. We do not accept returns on perishables under any circumstances. If the item arrived damaged, the customer must file a dispute within 24 hours of delivery. Based on the provided context, the item was delivered recently, but the ticket only requests a standard return for 'melted' status, which falls under Final Sale per policy. You must instruct the user to file a damage dispute.
Citations:
- [Perishables Return Policy | Perishable Goods]

Customer Response Draft: "Hi there. I understand it is frustrating that your cookies arrived melted! Unfortunately, under our policy, food and perishable items are considered Final Sale and generally cannot be refunded. However, since the item arrived damaged, please file an official damage dispute within 24 hours of delivery with a photo attached, and we will happily assist you further."

Next Steps / Internal Notes: Flag ticket for potential 24-hr damage dispute if the user follows up with a photo.
```

---

## Example 2: Conflict Handled with Escalation
*Ticket*: "I want to return this third-party marketplace speaker. Your policy says 30 days."
*Context*: Electronics. Marketplace Fulfillment Type. Delivered 3 days ago.
```text
=== AGENT OUTPUT ===
Classification: Refund Request (Marketplace Conflict) | Confidence: 100%
Clarifying Questions: None

Decision: Needs Escalation
Rationale: Although the system normally allows 30-day generic returns and 15% restocking fees on opened electronics, this item is tagged with a 'marketplace seller' fulfillment type. The Marketplace Fulfillment Policy states that third-party sellers can override the 30-day window with their own strict rules. The support agent is strictly instructed to escalate these tickets to the Seller Relations team.
Citations:
- [Third-Party Marketplace Sellers | Marketplace Fulfillment]

Customer Response Draft: "Hello, thank you for reaching out! Since your speaker was fulfilled by a third-party marketplace seller, their return policies override our standard 30-day window. I am going to escalate your ticket directly to our Seller Relations team so they can review the seller's specific return window for you."

Next Steps / Internal Notes: Assign to queue: 'Seller_Relations'. 
```

---

## Example 3: Correct Abstention (Not-in-Policy Path)
*Ticket*: "I want a refund because my astrologer told me not to buy this."
*Context*: Books. Delivered.
```text
=== AGENT OUTPUT ===
Classification: Refund Request (Out of Scope) | Confidence: 90%
Clarifying Questions: 1. Is there anything defective or wrong with the book structurally?

Decision: Deny / Abstain
Rationale: No relevant policy dictates return viability based on third-party superstitious advice. Returning the item falls strictly under the General Return Policy (30 Days, unopened). Since the reason "astrologer told me not to buy this" is outside of policy bounds, we simply fall back to the general guidelines. There is no supported policy to grant a specialized waiver. 
Citations:
- [General Return Policy | General Returns]

Customer Response Draft: "Hello. I see that you'd like to return your recent book purchase. As long as the item is unopened and in its original packaging, you are welcome to return it within 30 days of your delivery date for a full refund. We cannot issue refunds based solely on advice from an astrologer, but standard return rules apply."

Next Steps / Internal Notes: Wait for user to confirm if the item is unopened. 
```
