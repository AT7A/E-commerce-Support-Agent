import os

os.makedirs("data/html", exist_ok=True)

# Generate 15 Policy Documents covering Returns, Cancellations, Shipping, Promotions, Disputes
policies = [
    {"id": "policy_returns_general", "title": "General Return Policy", "content": "<h1>General Returns</h1><h2>Window</h2><p>Items may be returned within 30 days of the delivery date for a full refund back to the original payment method.</p><h2>Condition</h2><p>Items must be unopened and in original packaging.</p>"},
    {"id": "policy_returns_apparel", "title": "Apparel Returns", "content": "<h1>Apparel Returns</h1><p>Clothing and apparel can be returned within 14 days. Tags must remain attached. Undergarments are Final Sale due to hygiene reasons.</p>"},
    {"id": "policy_returns_electronics", "title": "Electronics Returns", "content": "<h1>Electronics Returns</h1><h2>Open Box Policy</h2><p>Opened electronics face a 15% restocking fee unless proven defective upon arrival.</p>"},
    {"id": "policy_returns_perishables", "title": "Perishables Return Policy", "content": "<h1>Perishable Goods</h1><p>Food, flowers, and other perishable items are explicitly Final Sale. We do not accept returns on perishables under any circumstances. If an item arrives damaged, the customer must file a dispute within 24 hours.</p>"},
    {"id": "policy_cancellations", "title": "Cancellation Policy", "content": "<h1>Cancellations</h1><h2>Order Status</h2><p>Orders can only be cancelled if the status is strictly 'Placed'. Once the status changes to 'Shipped', the user must wait for delivery and initiate a standard return.</p>"},
    {"id": "policy_shipping_lost", "title": "Lost Package Policy", "content": "<h1>Lost Packages</h1><h2>Timeline</h2><p>A package is considered lost if tracking shows no movement for 7 days past the expected delivery date. In this scenario, we will issue a full refund or replacement immediately.</p>"},
    {"id": "policy_shipping_damaged", "title": "Damaged Package Policy", "content": "<h1>Damaged Packages</h1><p>If an item arrives damaged, the user must provide a photo. Support agents may offer a 20% partial refund if the item is usable, or a full refund if destroyed.</p>"},
    {"id": "policy_promotions_coupons", "title": "Coupon Code Policy", "content": "<h1>Coupon Rules</h1><h2>Stacking</h2><p>Coupons cannot be stacked. Only one promotion code per order is allowed.</p><h2>Expired</h2><p>We do not honor expired coupon codes retroactively.</p>"},
    {"id": "policy_marketplace_sellers", "title": "Third-Party Marketplace Sellers", "content": "<h1>Marketplace Fulfillment</h1><h2>Override Policy</h2><p>For items explicitly marked as fulfillment_type 'marketplace seller', the seller's return window overrides our General 30-day policy. Sellers may enforce a strict 'No Returns' policy. Support must escalate these tickets to the Seller Relations team.</p>"},
    {"id": "policy_regional_california", "title": "California Electronics Fee", "content": "<h1>California Residents</h1><p>Due to state law, electronics shipped to California include a non-refundable $5 recycling fee. This fee cannot be refunded even if the item is returned.</p>"},
    {"id": "policy_regional_eu", "title": "EU Right of Withdrawal", "content": "<h1>EU Customers</h1><p>Customers in the EU have a mandatory 14-day right of withdrawal for any item (including opened electronics without restocking fees). Exceptions: Perishables and Hygiene items (Undergarments) remain Final Sale.</p>"},
    {"id": "policy_disputes", "title": "Order Disputes", "content": "<h1>Missing Items</h1><p>If an order was marked 'Delivered' but an item is missing from the box, agents must ask for a photo of the packing slip. After review, issue a partial refund for the missing item only.</p>"},
    {"id": "policy_fraud", "title": "Fraud Prevention Rules", "content": "<h1>Fraud Alerts</h1><p>If an account requests more than 3 high-value full refunds in a 6-month period, the ticket must be flagged as 'Fraud Risk' and escalated. Never promise a refund in this scenario.</p>"},
    {"id": "policy_final_sale", "title": "Final Sale Categories", "content": "<h1>Final Sale Rules</h1><p>Any item purchased during a 'Clearance Event' or marked as 'Final Sale' cannot be returned or exchanged. No exceptions unless the wrong item was shipped.</p>"},
    {"id": "policy_agent_guidelines", "title": "Support Agent Conduct", "content": "<h1>Tone and Style</h1><p>Always respond to customers with empathy. Start with 'I completely understand your frustration.' However, never bend a Final Sale policy to appease an angry customer.</p>"}
]

for p in policies:
    html = f"<html><head><title>{p['title']}</title></head><body><article>{p['content']}</article></body></html>"
    with open(f"data/html/{p['id']}.html", "w", encoding="utf-8") as f:
        f.write(html)

print("Mock Policy Data Generated Successfully! Total files:", len(policies))
