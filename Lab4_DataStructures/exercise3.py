LAST_NAME = "Villamor"
STUDENT_ID = "TUPM-26-3469"
FAVORITE_ARTIST = "Steve Lacy"

SEED_NUM = int(STUDENT_ID[-1])

ARTIST_POSITIONS = [ord(c) - 64 for c in FAVORITE_ARTIST.upper() if c.isalpha()]

print(f"LAST_NAME        : {LAST_NAME}")
print(f"STUDENT_ID       : {STUDENT_ID}")
print(f"FAVORITE_ARTIST  : {FAVORITE_ARTIST}")
print(f"SEED_NUM         : {SEED_NUM}")
print(f"ARTIST_POSITIONS : {ARTIST_POSITIONS}")

from collections import defaultdict, Counter


def value_stream():
    i = 0
    while True:
        yield SEED_NUM + ARTIST_POSITIONS[i % len(ARTIST_POSITIONS)]
        i += 1


print("\n" + "=" * 60)
print("EXERCISE 3: TRANSACTION HISTORY ANALYZER")
print("=" * 60)

customers = [f"{LAST_NAME}_C{n}" for n in range(1, 6)]
product_prices = {
    "NOTEBOOK": 45.00,
    "PEN": 15.00,
    "USB": 350.00,
    "HEADPHONES": 899.00,
    "CALCULATOR": 650.00,
}
products = list(product_prices)
vals = value_stream()


def make_qty():
    return 1 + next(vals) % 9


transactions = []
for i in range(8):
    transactions.append((customers[i % 5], products[(i * 2) % 5], make_qty()))

transactions.append((transactions[0][0], transactions[0][1], make_qty()))
transactions.append((transactions[3][0], transactions[3][1], make_qty()))

print("\n[1] Generated Transaction Records")
for i, (c, p, q) in enumerate(transactions, 1):
    print(f"  {i:>2}. {c:<14} {p:<11} Qty={q}")

organized_tx = []
for c, p, q in transactions:
    price = product_prices[p]
    organized_tx.append({"customer": c, "product": p, "qty": q, "price": price, "total": q * price})

print("\n[2] Organized Transaction Data")
print(f"  {'Customer':<14} {'Product':<11} {'Qty':>3} {'Price':>8} {'Total':>10}")
for t in organized_tx:
    print(f"  {t['customer']:<14} {t['product']:<11} {t['qty']:>3} {t['price']:>8.2f} {t['total']:>10.2f}")

pair_counts = Counter((t["customer"], t["product"]) for t in organized_tx)
repeated_purchases = {pair: n for pair, n in pair_counts.items() if n > 1}
distinct_products = set(t["product"] for t in organized_tx)
distinct_customers = set(t["customer"] for t in organized_tx)

print("\n[3] Repeated / Distinct Transactions")
print(f"  Repeated customer-product purchases: {repeated_purchases}")
print(f"  Distinct products  ({len(distinct_products)}): {sorted(distinct_products)}")
print(f"  Distinct customers ({len(distinct_customers)}): {sorted(distinct_customers)}")

grand_total = sum(t["total"] for t in organized_tx)
print("\n[4] Transaction Values")
for i, t in enumerate(organized_tx, 1):
    print(f"  Transaction {i:>2}: {t['qty']} x {t['price']:.2f} = {t['total']:.2f}")
print(f"  Overall dataset value: {grand_total:.2f}")

cust_summary = defaultdict(lambda: {"transactions": 0, "items": 0, "spent": 0.0})
for t in organized_tx:
    s = cust_summary[t["customer"]]
    s["transactions"] += 1
    s["items"] += t["qty"]
    s["spent"] += t["total"]

print("\n[5] Customer Summaries")
print(f"  {'Customer':<14} {'Txns':>4} {'Items':>5} {'Spent':>10}")
for c, s in cust_summary.items():
    print(f"  {c:<14} {s['transactions']:>4} {s['items']:>5} {s['spent']:>10.2f}")

prod_summary = defaultdict(lambda: {"transactions": 0, "units": 0, "revenue": 0.0})
for t in organized_tx:
    s = prod_summary[t["product"]]
    s["transactions"] += 1
    s["units"] += t["qty"]
    s["revenue"] += t["total"]

print("\n[6] Product Summaries")
print(f"  {'Product':<11} {'Txns':>4} {'Units':>5} {'Revenue':>10}")
for p, s in prod_summary.items():
    print(f"  {p:<11} {s['transactions']:>4} {s['units']:>5} {s['revenue']:>10.2f}")

ranked_customers = sorted(cust_summary.items(), key=lambda kv: kv[1]["spent"], reverse=True)
ranked_products = sorted(prod_summary.items(), key=lambda kv: kv[1]["revenue"], reverse=True)
ranked_tx = sorted(organized_tx, key=lambda t: t["total"], reverse=True)

print("\n[7] Ordered Results")
print("  Customers by total spent:")
for rank, (c, s) in enumerate(ranked_customers, 1):
    print(f"    {rank}. {c:<14} {s['spent']:.2f}")
print("  Products by revenue:")
for rank, (p, s) in enumerate(ranked_products, 1):
    print(f"    {rank}. {p:<11} {s['revenue']:.2f}")
print("  Largest transaction:", f"{ranked_tx[0]['customer']} - {ranked_tx[0]['product']} ({ranked_tx[0]['total']:.2f})")

print("\n[8] FINAL CONSOLIDATED TRANSACTION REPORT")
print(f"  Total transactions      : {len(organized_tx)}")
print(f"  Total units sold        : {sum(t['qty'] for t in organized_tx)}")
print(f"  Total transaction value : {grand_total:.2f}")
print(f"  Average per transaction : {grand_total / len(organized_tx):.2f}")
print(f"  Repeated purchases      : {len(repeated_purchases)}")
print(f"  Top customer            : {ranked_customers[0][0]} ({ranked_customers[0][1]['spent']:.2f})")
print(f"  Top product             : {ranked_products[0][0]} ({ranked_products[0][1]['revenue']:.2f})")