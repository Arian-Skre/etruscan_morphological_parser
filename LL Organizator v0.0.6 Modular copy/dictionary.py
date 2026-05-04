import json, os
from config import DATA_FILE, ETRUSCAN_ALPHABET
from utils import normalize_word
from numerals import parse_numeral_phrase, parse_single_numeral, is_numeral

def create_empty_dictionary():
    return {"lexical": {letter: {} for letter in ETRUSCAN_ALPHABET}, "numerals": {}}

def load_dictionary():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}
    if "lexical" not in data:
        data = {"lexical": data, "numerals": {}}
    if "numerals" not in data:
        data["numerals"] = {}
    return data

def save_dictionary(dictionary):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, indent=2, ensure_ascii=False)

# -----------------------------
# Add New Entries
# -----------------------------

def add_new_entries(dictionary):
    print("\n[Add New Entries]")

    numerals = dictionary["numerals"]
    lexical = dictionary["lexical"]

    column = input("Enter column number: ").strip()
    line = input("Enter line number: ").strip()
    text = input("Enter dot-separated words: ").strip()

    if not text:
        print("No input given. Returning to menu.")
        return

    words = text.split(".")

    i = 0
    while i < len(words):
        word = words[i].strip()
        word_position = i + 1
        if not word:
            i += 1
            continue

        # -----------------------------
        # Multi-token numeral
        # -----------------------------
        
        numeral_result, consumed = parse_numeral_phrase(words, i)

        if numeral_result:
            key = numeral_result["core"]

            if key not in numerals:
                numerals[key] = {
                    "surface_forms": [],
                    "value": numeral_result["value"],
                    "attestations": {}
                }
            for form in numeral_result["surface_forms"]:
                if form not in numerals[key]["surface_forms"]:
                    numerals[key]["surface_forms"].append(form)

            
            numerals[key]["attestations"] \
                .setdefault(column, {}) \
                .setdefault(line, []) \
                .append(i + 1)

            i += consumed
            continue
        # -----------------------------
        # Single-token numeral
        # -----------------------------
    
        single = parse_single_numeral(word, position="single")
        if single:
            if word not in numerals:
                numerals[word] = {
                    "surface_forms": [word],
                    "value": single.get("value"),
                    "attestations": {}
                }

            numerals[word]["attestations"] \
                .setdefault(column, {}) \
                .setdefault(line, []) \
                .append(i + 1)

            i += 1
            continue

        # -----------------------------
        # Lexical word (fallback)
        # -----------------------------
        
        if word.startswith("phi"):
            first_letter = "phi"
        else:
            first_letter = word[0]

        if first_letter not in lexical:
            i += 1
            continue

        letter_bucket = lexical[first_letter]
        normalized = normalize_word(word)

        if normalized not in letter_bucket:
            letter_bucket[normalized] = {"_variants": []}

        if word not in letter_bucket[normalized]["_variants"]:
            letter_bucket[normalized]["_variants"].append(word)

        letter_bucket[normalized] \
            .setdefault(column, {}) \
            .setdefault(line, []) \
            .append(i + 1)

        i += 1

         # -----------------------------
        # NUMERAL ROUTING
        # -----------------------------
        if is_numeral(word):
            if word not in numerals:
                numerals[word] = {
                    "value": NUMERALS[word],
                    "attestations": {}
                }

            if column not in numerals[word]["attestations"]:
                numerals[word]["attestations"][column] = {}

            if line not in numerals[word]["attestations"][column]:
                numerals[word]["attestations"][column][line] = []

            numerals[word]["attestations"][column][line].append(index)
            continue

        # -----------------------------
        # LEXICAL ROUTING
        # -----------------------------
        
        if word.startswith("phi"):
            first_letter = "phi"
        else:
            first_letter = word[0]

        if first_letter not in lexical:
            print(f"Skipping invalid word '{word}' (invalid first letter).")
            continue

        letter_bucket = lexical[first_letter]
        normalized = normalize_word(word)

        if normalized not in letter_bucket:
            letter_bucket[normalized] = {"_variants": []}

        if word not in letter_bucket[normalized]["_variants"]:
            letter_bucket[normalized]["_variants"].append(word)

        if column not in letter_bucket[normalized]:
            letter_bucket[normalized][column] = {}

        if line not in letter_bucket[normalized][column]:
            letter_bucket[normalized][column][line] = []

        letter_bucket[normalized][column][line]

    save_dictionary(dictionary)
    print("Entries added and saved successfully.")

# -----------------------------
# Open Dictionary
# -----------------------------

def open_dictionary(dictionary):
    print("\n[Open Dictionary]")

    print("Available letters:")
    print(", ".join(ETRUSCAN_ALPHABET))

    letter = input("Select a letter: ").strip()

    if letter not in dictionary["lexical"]:
        print("Invalid letter selection.")
        return

    letter_bucket = dictionary["lexical"][letter]

    if not letter_bucket:
        print(f"No entries for letter '{letter}'.")
        return

    print(f"\n=== Entries for '{letter}' ===\n")

    for word in sorted(letter_bucket.keys()):
        entry = letter_bucket[word]

        variants = entry.get("_variants", [])
        header = " / ".join(variants) if variants else word

        segments = []

        for column, lines in entry.items():
            if column == "_variants":
                continue  

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

        print(f"{header} (" + ". ".join(segments) + ")")

    print()

