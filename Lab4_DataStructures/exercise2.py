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
print("EXERCISE 2: STUDENT PERFORMANCE DATA ANALYZER")
print("=" * 60)


def performance_category(score):
    if score >= 90:
        return "Outstanding"
    elif score >= 85:
        return "Very Good"
    elif score >= 75:
        return "Satisfactory"
    return "Needs Improvement"


students = [f"{LAST_NAME}_S{n}" for n in range(1, 6)]
subjects = ["PROGRAMMING", "MATHEMATICS", "ELECTRONICS", "PHYSICS", "ENGLISH"]
vals = value_stream()


def make_score():
    return 60 + (next(vals) * 3) % 41


perf_records = []
for st in students:
    for sub in subjects:
        perf_records.append((st, sub, make_score()))

perf_records.append((students[0], subjects[0], make_score()))

perf_records[-2] = (perf_records[-2][0], perf_records[-2][1], None)

print("\n[1] Generated Performance Records")
for i, (st, sub, sc) in enumerate(perf_records, 1):
    print(f"  {i:>2}. {st:<14} {sub:<12} Score={sc}")

organized_perf = defaultdict(dict)
pair_counts = Counter((st, sub) for st, sub, _ in perf_records)
for st, sub, sc in perf_records:
    if sc is not None and sub not in organized_perf[st]:
        organized_perf[st][sub] = sc

print("\n[2] Organized Student/Subject Data")
for st in students:
    print(f"  {st:<14} {organized_perf[st]}")

repeated_pairs = {pair: n for pair, n in pair_counts.items() if n > 1}
incomplete = [(st, sub) for st, sub, sc in perf_records if sc is None]

print("\n[3] Repeated / Incomplete Records")
print(f"  Repeated (student, subject): {repeated_pairs}")
print(f"  Incomplete (missing score) : {incomplete}")

print("\n[4] Performance Categories")
category_table = {}
for st in students:
    for sub, sc in organized_perf[st].items():
        category_table[(st, sub)] = performance_category(sc)
        print(f"  {st:<14} {sub:<12} {sc:>3} -> {category_table[(st, sub)]}")

student_avg = {st: round(sum(d.values()) / len(d), 2) for st, d in organized_perf.items() if d}
subject_scores = defaultdict(list)
for st in organized_perf:
    for sub, sc in organized_perf[st].items():
        subject_scores[sub].append(sc)
subject_avg = {sub: round(sum(v) / len(v), 2) for sub, v in subject_scores.items()}
category_counts = Counter(category_table.values())

print("\n[5] Student and Subject Summaries")
print("  Student averages:")
for st, avg in student_avg.items():
    print(f"    {st:<14} {avg}")
print("  Subject averages (highest / lowest score):")
for sub, avg in subject_avg.items():
    print(f"    {sub:<12} avg={avg}  high={max(subject_scores[sub])}  low={min(subject_scores[sub])}")
print("  Category distribution:", dict(category_counts))

ranked_students = sorted(student_avg.items(), key=lambda kv: kv[1], reverse=True)
ranked_subjects = sorted(subject_avg.items(), key=lambda kv: kv[1], reverse=True)

print("\n[6] Ordered Results")
print("  Student ranking:")
for rank, (st, avg) in enumerate(ranked_students, 1):
    print(f"    {rank}. {st:<14} {avg}")
print("  Subject ranking:")
for rank, (sub, avg) in enumerate(ranked_subjects, 1):
    print(f"    {rank}. {sub:<12} {avg}")

print("\nFINAL STUDENT PERFORMANCE REPORT")
print(f"  Students evaluated      : {len(students)}")
print(f"  Subjects evaluated      : {len(subjects)}")
print(f"  Total raw records       : {len(perf_records)}")
print(f"  Valid records used      : {len(category_table)}")
print(f"  Repeated records        : {len(repeated_pairs)}")
print(f"  Incomplete records      : {len(incomplete)}")
print(f"  Top student             : {ranked_students[0][0]} ({ranked_students[0][1]})")
print(f"  Top subject             : {ranked_subjects[0][0]} ({ranked_subjects[0][1]})")
print(f"  Weakest subject         : {ranked_subjects[-1][0]} ({ranked_subjects[-1][1]})")