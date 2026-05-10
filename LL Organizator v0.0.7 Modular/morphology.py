# morphology.py

import csv
from utils import normalize_word
from ll_file import load_ll_file

STEMS_FILE = "stems.csv"

VOWELS = {"a", "e", "i", "u"}

# --------------------------------------------------
# Load Stems
# --------------------------------------------------

def load_stems():
    """
    Loads stems from stems.csv,
    normalizes them,
    removes duplicates,
    and generates variant forms.
    """

    exact = {}
    variants = {}

    try:
        with open(STEMS_FILE, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)

            for row in reader:
                raw_stem = row["stem"].strip()
                source = row.get("source", "").strip()

                if not raw_stem:
                    continue

                normalized = normalize_word(raw_stem)

                # Deduplicate normalized stems
                if normalized in exact:
                    continue

                exact[normalized] = {
                    "canonical": raw_stem,
                    "source": source,
                    "variants": []
                }

        # Generate variants
        for norm_stem in exact:
            generated = generate_variants(norm_stem)

            for variant in generated:
                if variant == norm_stem:
                    continue

                if variant not in variants:
                    variants[variant] = norm_stem
                    exact[norm_stem]["variants"].append(variant)

    except FileNotFoundError:
        print("Could not find stems.csv")

    return {
        "exact": exact,
        "variants": variants
    }

# --------------------------------------------------
# Variant Generation
# --------------------------------------------------

def generate_variants(stem):
    """
    Generates probable inflectional / phonetic variants.
    """

    forms = set()
    forms.add(stem)

    # ----------------------------------------------
    # Rule A: Final vowel deletion
    # sacni -> sacn
    # tura -> tur
    # ----------------------------------------------
    if len(stem) > 3 and stem[-1] in VOWELS:
        forms.add(stem[:-1])

    # ----------------------------------------------
    # Rule B: Internal vowel syncopation
    # avil -> avl
    # ----------------------------------------------
    for i in range(1, len(stem) - 1):
        if stem[i] in VOWELS:
            sync = stem[:i] + stem[i+1:]
            if len(sync) >= 3:
                forms.add(sync)

    # ----------------------------------------------
    # Rule C: a/e interchange
    # clan -> clen
    # ----------------------------------------------
    if "a" in stem:
        forms.add(stem.replace("a", "e", 1))

    if "e" in stem:
        forms.add(stem.replace("e", "a", 1))

    # ----------------------------------------------
    # Rule D: terminal s
    # tin -> tins
    # ----------------------------------------------
    forms.add(stem + "s")

    return sorted(forms)

# --------------------------------------------------
# Longest Prefix Match
# --------------------------------------------------

def find_longest_match(word, stem_dict):
    """
    Returns the longest matching prefix stem.
    """

    best_match = None

    for stem in stem_dict:
        if word.startswith(stem):

            if best_match is None:
                best_match = stem

            elif len(stem) > len(best_match):
                best_match = stem

    if not best_match:
        return None, None

    suffix = word[len(best_match):]

    return best_match, suffix

# --------------------------------------------------
# Statistical Guess
# --------------------------------------------------

def guess_stem(word):
    """
    Very primitive fallback guessing.
    """

    candidates = []

    for i in range(3, len(word) - 1):

        stem = word[:i]
        suffix = word[i:]

        score = 0

        # Prefer longer stems
        score += len(stem)

        # Penalize huge suffixes
        score -= len(suffix)

        # Penalize ugly consonant clusters
        if len(stem) >= 2:
            if stem[-1] not in VOWELS and stem[-2] not in VOWELS:
                score -= 2

        candidates.append((score, stem, suffix))

    if not candidates:
        return None

    candidates.sort(reverse=True)

    best = candidates[0]

    return {
        "stem": best[1],
        "suffix": best[2],
        "method": "guess",
        "confidence": 0.4
    }

# --------------------------------------------------
# Word Analysis
# --------------------------------------------------

def analyze_word(word, stem_data):

    normalized = normalize_word(word)

    exact = stem_data["exact"]
    variants = stem_data["variants"]

    # ----------------------------------------------
    # EXACT MATCH
    # ----------------------------------------------

    match, suffix = find_longest_match(normalized, exact)

    if match:

        entry = exact[match]

        return {
            "surface": word,
            "normalized": normalized,
            "stem": entry["canonical"],
            "matched_as": match,
            "suffix": suffix,
            "method": "exact",
            "confidence": 1.0
        }

    # ----------------------------------------------
    # VARIANT MATCH
    # ----------------------------------------------

    match, suffix = find_longest_match(normalized, variants)

    if match:

        canonical_norm = variants[match]
        entry = exact[canonical_norm]

        return {
            "surface": word,
            "normalized": normalized,
            "stem": entry["canonical"],
            "matched_as": match,
            "suffix": suffix,
            "method": "variant",
            "confidence": 0.9
        }

    # ----------------------------------------------
    # FALLBACK GUESS
    # ----------------------------------------------

    guessed = guess_stem(normalized)

    if guessed:

        return {
            "surface": word,
            "normalized": normalized,
            "stem": guessed["stem"],
            "matched_as": guessed["stem"],
            "suffix": guessed["suffix"],
            "method": "guess",
            "confidence": guessed["confidence"]
        }

    return None

# --------------------------------------------------
# CLI Interface
# --------------------------------------------------

# --------------------------------------------------
# Column Lexical Parsing
# --------------------------------------------------

def parse_lexical():

    stem_data = load_stems()

    columns = load_ll_file()

    if not columns:
        print("Could not read L.L. Complete.txt")
        return

    col = input("\nEnter column number: ").strip()

    if col not in columns:
        print(f"Column {col} not found.")
        return

    print(f"\n=== Column {col} Lexical Parsing ===\n")

    lines = columns[col]

    for line in lines:

        stripped = line.strip()

        # ------------------------------------------
        # Preserve structural markers
        # ------------------------------------------

        if stripped == "{missing}":
            print("{missing}")
            continue

        if "|" in stripped:
            print("|")
            continue

        # ------------------------------------------
        # Split punctuation
        # ------------------------------------------

        line = line.replace("!", ".")

        tokens = [w.strip() for w in line.split(".") if w.strip()]

        if not tokens:
            continue

        # ------------------------------------------
        # Parse each token
        # ------------------------------------------

        for token in tokens:

            result = analyze_word(token, stem_data)

            if not result:
                print(f"{token} -> [unparsed]")
                continue

            print(
                f"{result['surface']} "
                f"-> stem: {result['stem']} "
                f"| suffix: {result['suffix']} "
                f"| method: {result['method']} "
                f"| confidence: {result['confidence']}"
            )
