from config import LL_FILE

def load_ll_file():
    columns = {}
    current_col = None
    try:
        with open(LL_FILE, "r", encoding="utf-8") as f:
            for raw in f:
                line = raw.strip()
                if not line:
                    continue
                if line.startswith("Column"):
                    current_col = line.split()[-1]
                    columns[current_col] = []
                    continue
                if current_col:
                    columns[current_col].append(line)
    except FileNotFoundError:
        return None
    return columns

# compute_global_sentence_stats

# -----------------------------
# Global Sentence Statistics
# -----------------------------

def compute_global_sentence_stats(columns):
    sentence_lengths = []

    for lines in columns.values():
        inside_known = False
        current_len = 0

        for line in lines:
            if "{missing}" in line or line.startswith("Column"):
                continue

            if "|" in line:
                inside_known = False
                current_len = 0
                continue

            parts = line.split("!")

            for i, part in enumerate(parts):
                words = [w for w in part.split(".") if w]

                if inside_known:
                    current_len += len(words)

                # Toggle sentence state at every "!"
                if i < len(parts) - 1:
                    if inside_known:
                        sentence_lengths.append(current_len)
                        current_len = 0
                        inside_known = False
                    else:
                        inside_known = True

        # Safety flush
        if inside_known and current_len > 0:
            sentence_lengths.append(current_len)

    if not sentence_lengths:
        return 16, (15, 17)

    avg = sum(sentence_lengths) / len(sentence_lengths)
    lo = max(5, int(avg - 3))
    hi = int(avg + 3)

    return int(avg), (lo, hi)
