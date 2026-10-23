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
 
 
print("=" * 60)
print("EXERCISE 1: ENGINEERING TEST DATA ORGANIZER")
print("=" * 60)
 
test_sources = [f"{LAST_NAME}_T{n}" for n in range(1, 6)]
categories = ["TEMPERATURE", "VOLTAGE", "CURRENT", "PRESSURE", "SPEED"]
vals = value_stream()
 
test_records = [(src, cat, next(vals)) for src, cat in zip(test_sources, categories)]
 
test_records.append((test_sources[0], "TEMPERATURE", next(vals)))
test_records.append((test_sources[1], "VOLTAGE", next(vals)))
test_records.append((test_sources[1], "VOLTAGE", next(vals)))
 
test_records.append(test_records[0])
 
print("\n[1] Generated Test Data")
for i, rec in enumerate(test_records, 1):
    print(f"  {i:>2}. Source={rec[0]:<14} Category={rec[1]:<12} Value={rec[2]}")
 
organized = defaultdict(lambda: defaultdict(list))
for src, cat, val in test_records:
    organized[src][cat].append(val)
 
print("\n[2] Organized Test Data (by Source and Category)")
for src in sorted(organized):
    for cat, values in organized[src].items():
        print(f"  {src:<14} {cat:<12} {values}")
 
record_counts = Counter(test_records)
repeated = {rec: n for rec, n in record_counts.items() if n > 1}
distinct_records = set(test_records)
distinct_values = set(r[2] for r in test_records)
 
print("\n[3] Repeated / Distinct Data")
print(f"  Total records     : {len(test_records)}")
print(f"  Distinct records  : {len(distinct_records)}")
print(f"  Repeated records  : {repeated}")
print(f"  Distinct values   : {sorted(distinct_values)}")
 
by_category = defaultdict(list)
for _, cat, val in test_records:
    by_category[cat].append(val)
 
category_summary = {
    cat: {
        "count": len(v),
        "min": min(v),
        "max": max(v),
        "sum": sum(v),
        "mean": round(sum(v) / len(v), 2),
    }
    for cat, v in by_category.items()
}
 
print("\n[4] Numerical and Categorical Summaries")
print(f"  {'Category':<12} {'Count':>5} {'Min':>5} {'Max':>5} {'Sum':>6} {'Mean':>7}")
for cat, s in category_summary.items():
    print(f"  {cat:<12} {s['count']:>5} {s['min']:>5} {s['max']:>5} {s['sum']:>6} {s['mean']:>7}")
 
source_counts = Counter(r[0] for r in test_records)
print("  Records per source :", dict(source_counts))
print("  Records per category:", dict(Counter(r[1] for r in test_records)))
 
processed = list(dict.fromkeys(test_records))
source_totals = defaultdict(int)
for src, _, val in processed:
    source_totals[src] += val
 
print("\n[5] Processed Results (duplicates removed)")
print(f"  Unique records kept: {len(processed)}")
for src, total in source_totals.items():
    print(f"  {src:<14} total value = {total}")
 
ordered_by_value = sorted(processed, key=lambda r: r[2], reverse=True)
ordered_categories = sorted(category_summary.items(), key=lambda kv: kv[1]["mean"], reverse=True)
 
print("\n[6] Ordered Results")
print("  Records by value (descending):")
for rec in ordered_by_value:
    print(f"    {rec[2]:>4}  {rec[0]:<14} {rec[1]}")
print("  Categories by mean (descending):")
for cat, s in ordered_categories:
    print(f"    {cat:<12} mean={s['mean']}")
 
all_values = [r[2] for r in processed]
print("\n[7] FINAL ORGANIZED AND SUMMARIZED TEST DATASET")
print(f"  Sources            : {len(source_totals)}")
print(f"  Categories         : {len(by_category)}")
print(f"  Total records      : {len(test_records)} (unique: {len(processed)})")
print(f"  Overall min / max  : {min(all_values)} / {max(all_values)}")
print(f"  Overall mean       : {round(sum(all_values) / len(all_values), 2)}")
print(f"  Highest-mean cat.  : {ordered_categories[0][0]}")
print(f"  Lowest-mean cat.   : {ordered_categories[-1][0]}")