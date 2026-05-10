from config import NUMERALS, FIRST_NUMERAL_SUFFIXES, SECOND_NUMERAL_SUFFIXES
from utils import split_suffix

def valid_numeral_suffix_pair(first_suffix, first_core, second_suffix):
    if first_suffix == "niS" and first_core != "0u":
        return False

    # iS on first numeral forbidden if second also uses iS
    if first_suffix == "iS" and second_suffix == "iS":
        return False

    return True

# -----------------------------
# Numeral Suffix Splitting
# -----------------------------

def split_suffix(token, position="single"):
    if position == "first":
        suffixes = FIRST_NUMERAL_SUFFIXES
    else:
        suffixes = SECOND_NUMERAL_SUFFIXES

    for suf in sorted(suffixes, key=len, reverse=True):
        if token.endswith(suf):
            return token[:-len(suf)], suf

    return token, None

def resolve_numeral_stem(stem):
    # Direct atomic numerals
    if stem in NUMERALS:
        return {
            "value": NUMERALS[stem],
            "type": "atomic"
        }

    # Tens
    if stem.endswith("alX"):
        base = stem[:-3]
        if base in NUMERALS and NUMERALS[base] < 10:
            return {
                "value": NUMERALS[base] * 10,
                "type": "tens",
                "base": base
            }

    return None

# -----------------------------
# Numeral Detection
# -----------------------------

def is_numeral(token):
    core, _ = split_suffix(token)
    return core in NUMERALS

# -----------------------------
# Numeral Display
# -----------------------------

def view_numerals(dictionary):
    print("\n=== Numerals ===\n")

    numerals = dictionary.get("numerals", {})
    if not numerals:
        print("No numerals recorded.")
        return

    for word, data in sorted(
        numerals.items(),
        key=lambda x: x[1]["value"] if isinstance(x[1]["value"], int) else float("inf")
    ):
        segments = []


        for column, lines in data["attestations"].items():
            line_labels = []
            positions = []

            for line, pos_list in lines.items():
                line_labels.append(line)
                positions.extend(pos_list)

            segment = (
                f"C{column}, L"
                + ", ".join(line_labels)
                + ", "
                + ", ".join(str(p) for p in positions)
            )

            segments.append(segment)

        print(f"{word} ({'. '.join(segments)})")

# -----------------------------
# Numeral Parse Handler
# -----------------------------

def parse_numerals():
    text = input("\nEnter numeral expression: ").strip()

    analysis = analyze_numeral_expression(text)

    if not analysis:
        print("Could not parse numeral expression.")
        return

    print("\n=== Numeral Analysis ===")
    for part in analysis:
        line = f"{part['token']} = {part['stem']} (stem, {part['value']})"

        if "suffix" in part:
            line += f" +{part['suffix']} (suffix, {part['suffix_meaning']})"

        print(line)

# -----------------------------
# Numeral Phrase Parsing
# -----------------------------

def parse_numeral_phrase(tokens, start_index):
    # FIRST token → first-position rules
    first = parse_single_numeral(tokens[start_index], position="first")
    if not first:
        return None, 0

    if start_index + 1 >= len(tokens):
        return None, 0

    # SECOND token → second-position rules
    second_token = tokens[start_index + 1]
    second_core, second_suffix = split_suffix(second_token, position="second")

    if second_core not in NUMERALS:
        return None, 0

    high_value = NUMERALS[second_core]

    # Resolve numerical modifier on FIRST token
    if first.get("modifier") == "less":
        value = high_value - first["base"]
    elif first.get("modifier") == "more":
        value = high_value + first["base"]
    else:
        return None, 0

    # Core numeral form (normalized)
    core = f"{tokens[start_index]} {second_core}"

    # Surface forms:
    # a) stripped grammatical suffix
    # b) original full form
    surface_a = f"{tokens[start_index]} {second_core}"
    surface_b = f"{tokens[start_index]} {second_token}"

    return {
        "core": core,
        "value": value,
        "surface_forms": [surface_a, surface_b]
    }, 2

def parse_single_numeral(token, position):
    """
    Parses a single numeral token.
    Returns dict or None if not numeric.
    """
    core, suffix = split_suffix(token, position)

    # Check simple numeral
    if core in NUMERALS:
        return {
            "value": NUMERALS[core],
            "core": core,
            "suffix": suffix
        }

    # Check modified numeral
    for base, val in NUMERALS.items():
        if core.startswith(base):
            remainder = core[len(base):]

            if remainder == LESS_THAN_SUFFIX:
                return {
                    "value": None,  # Will be resolved in phrase
                    "modifier": "less",
                    "base": val,
                    "suffix": suffix
                }

            if remainder == MORE_THAN_SUFFIX:
                return {
                    "value": None,
                    "modifier": "more",
                    "base": val,
                    "suffix": suffix
                }

    return None

# -----------------------------
# Numeral Structure Parsing
# -----------------------------

def analyze_numeral_expression(text):
    tokens = text.replace(".", " ").split()
    parts = []

    for i, token in enumerate(tokens):
        position = "first" if i == 0 else "second"

        stem, suffix = split_suffix(token, position)

        if stem not in NUMERALS:
            return None

        entry = {
            "token": token,
            "stem": stem,
            "value": NUMERALS[stem],
            "position": position
        }

        if suffix:
            entry["suffix"] = suffix
            if position == "first":
                entry["suffix_meaning"] = FIRST_NUMERAL_SUFFIXES.get(suffix, "unknown")
            else:
                entry["suffix_meaning"] = SECOND_NUMERAL_SUFFIXES.get(suffix, "unknown")

        parts.append(entry)

    return parts
