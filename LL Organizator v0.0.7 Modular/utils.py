from config import FIRST_NUMERAL_SUFFIXES, SECOND_NUMERAL_SUFFIXES

def normalize_word(word):
    w = word.strip()
    if w.startswith("Xi") or w.startswith("XI"):
        return w
    w = w.replace("0", "t").replace("S", "s").replace("X", "c")
    return w.lower()

def split_suffix(token, position="first"):
    suffixes = FIRST_NUMERAL_SUFFIXES if position == "first" else SECOND_NUMERAL_SUFFIXES
    for suf in sorted(suffixes, key=len, reverse=True):
        if token.endswith(suf):
            return token[:-len(suf)], suf
    return token, None
