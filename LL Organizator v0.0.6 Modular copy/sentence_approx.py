from config import PROTECTED_PHRASES
from utils import split_suffix
from ll_file import load_ll_file, compute_global_sentence_stats

# -----------------------------
# Statistical Subject/Predicate Estimation
# -----------------------------
def estimate_subject_predicate(columns):
    """
    Returns per-token subject and predicate probabilities
    based on first vs later token positions in sentences.
    """
    from collections import defaultdict

    token_stats = defaultdict(lambda: {"first": 0, "later": 0, "total": 0})

    for lines in columns.values():
        for line in lines:
            if line.strip() in ("{missing}", "|"):
                continue

            sentences = line.split("!")
            for sent in sentences:
                words = [w for w in sent.split(".") if w]
                for i, w in enumerate(words):
                    token_stats[w]["total"] += 1
                    if i == 0:
                        token_stats[w]["first"] += 1
                    else:
                        token_stats[w]["later"] += 1

    subject_prob = {}
    predicate_prob = {}
    for token, counts in token_stats.items():
        subject_prob[token] = counts["first"] / counts["total"]
        predicate_prob[token] = counts["later"] / counts["total"]

    return subject_prob, predicate_prob

# -----------------------------
# Sentence Tagging
# -----------------------------
def tag_sentence(sentence_tokens, subject_prob, predicate_prob):
    """
    Mark probable subject (*) and predicate (") in a list of tokens.
    Returns tagged_tokens and sentence-level confidence.
    """
    n = len(sentence_tokens)
    if n == 0:
        return sentence_tokens, 0

    # Candidate subject: first half
    first_half = sentence_tokens[: max(1, n // 2)]
    sub_idx = max(range(len(first_half)), key=lambda i: subject_prob.get(first_half[i], 0))

    # Candidate predicate: second half
    second_half = sentence_tokens[n // 2 :]
    pred_idx = max(range(len(second_half)), key=lambda i: predicate_prob.get(second_half[i], 0)) + n // 2

    tagged = sentence_tokens[:]
    tagged[sub_idx] = f"*{tagged[sub_idx]}*"
    tagged[pred_idx] = f'"{tagged[pred_idx]}"'

    # Sentence confidence: average probability
    conf = (subject_prob.get(sentence_tokens[sub_idx], 0) + predicate_prob.get(sentence_tokens[pred_idx], 0)) / 2

    return tagged, conf

# -----------------------------
# Sentence Grouping Logic
# -----------------------------

def group_words(words, avg_len, length_range):
    groups = []
    current = []
    i = 0

    # Map protected phrases to placeholders
    protected_map = {f"_PROTECTED{idx}_": phrase for idx, phrase in enumerate(PROTECTED_PHRASES)}

    # Preprocess: replace phrases with placeholders
    preprocessed = []
    while i < len(words):
        matched = False
        for idx, phrase in enumerate(PROTECTED_PHRASES):
            phrase_tokens = phrase.split(".")
            if words[i:i + len(phrase_tokens)] == phrase_tokens:
                preprocessed.append(f"_PROTECTED{idx}_")
                i += len(phrase_tokens)
                matched = True
                break
        if not matched:
            preprocessed.append(words[i])
            i += 1

    # Group words by avg_len
    current = []
    for w in preprocessed:
        current.append(w)
        if len(current) >= avg_len:
            groups.append(current)
            current = []
    if current:
        groups.append(current)

    # Replace placeholders back to full phrases
    final_groups = []
    for g in groups:
        restored = []
        for token in g:
            if token in protected_map:
                restored.extend(protected_map[token].split("."))
            else:
                restored.append(token)
        final_groups.append(restored)

    return final_groups

# -----------------------------
# Column Approximation
# -----------------------------
def approximate_column(lines, avg_len, length_range, subject_prob, predicate_prob):
    output = []
    buffer = []
    inside_known = False
    confidences = []

    def flush_buffer():
        nonlocal buffer, confidences
        if not buffer:
            return
        grouped = group_words(buffer, avg_len, length_range)
        for g in grouped:
            tagged_tokens, conf = tag_sentence(g, subject_prob, predicate_prob)
            output.append("/" + ".".join(tagged_tokens) + "/")
            confidences.append(conf)
        buffer = []

    for line in lines:
        if line.strip() == "{missing}":
            flush_buffer()
            output.append("{missing}")
            continue
        if "|" in line:
            flush_buffer()
            output.append("|")
            inside_known = False
            continue

        parts = line.split("!")
        for i, part in enumerate(parts):
            words = [w for w in part.split(".") if w]
            if inside_known:
                # Known sentences output directly
                output.append(".".join(words))
            else:
                buffer.extend(words)
            if i < len(parts) - 1:
                flush_buffer()
                output.append("!")
                inside_known = not inside_known

    flush_buffer()

    # Column-level confidence
    if confidences:
        column_confidence = int(sum(confidences) / len(confidences) * 100)
    else:
        column_confidence = 0

    return output, column_confidence

# -----------------------------
# Sentence Approximation
# -----------------------------

LL_FILE = "L.L. Complete.txt"

def sentence_approximation():
    columns = load_ll_file()
    if not columns:
        print("Could not read L.L. Complete.txt")
        return

    col = input("Enter column number: ").strip()
    if col not in columns:
        print(f"Column {col} not found in file.")
        return

    # Compute global stats
    global_avg, global_range = compute_global_sentence_stats(columns)

    # Estimate subjects/predicates
    subject_prob, predicate_prob = estimate_subject_predicate(columns)

    # Approximate column
    output, confidence = approximate_column(
        columns[col],
        global_avg,
        global_range,
        subject_prob,
        predicate_prob
    )

    # Display
    print(f"\n=== Column {col} (Sentence Approximation) ===\n")
    for line in output:
        print(line)
    print(f"\nConfidence: {confidence}%")
