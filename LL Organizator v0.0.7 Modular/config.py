ETRUSCAN_ALPHABET = ["a", "c", "e", "v", "z", "h", "0", "i", "l", "m", "n", "p", "S", "r", "s", "t", "u", "phi", "X", "f"]

NUMERALS = {
    "0u": 1, "tu": 1,
    "zal": 2,
    "ci": 3,
    "hu0": 4,
    "maX": 5,
    "Sa": 6,
    "Semphi": 7,
    "cezp": 8,
    "nurphi": 9,
    "Sar": 10,
    "za0rum": 20,
    "cealX": 30,
    "hu0alX": 40,
    "muvalX": 50,
    "SealX": 60,
    "SemphialX": 70,
    "cezpalX": 80,
    "nurphialX": 90,
    "Xim0": 100
}

FIRST_NUMERAL_SUFFIXES = {
    "S": "more than",
    "em": "less than",
    "nem": "less than",
    "iS": "more than",
    "niS": "more than"
}

SECOND_NUMERAL_SUFFIXES = {
    "iS": "superessive",
    "uS": "superessive"
}

ALL_NUMERAL_SUFFIXES = set(FIRST_NUMERAL_SUFFIXES) | set(SECOND_NUMERAL_SUFFIXES)

DATA_FILE = "etruscan_dictionary.json"
LL_FILE = "L.L. Complete.txt"
PROTECTED_PHRASES = ["flere.in.crapSti.un.mlaX.nun0en"]
