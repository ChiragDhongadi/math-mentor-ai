import re

def clean_math_speech(text: str):

    text = text.lower()

    replacements = {

        # basic operators
        "plus": "+",
        "minus": "-",
        "times": "*",
        "multiplied by": "*",
        "divided by": "/",
        "forward slash": "/",

        # powers
        "squared": "^2",
        "cubed": "^3",
        "to the power of": "^",

        # parentheses
        "open parenthesis": "(",
        "close parenthesis": ")",
        "open bracket": "(",
        "close bracket": ")",

        # probability
        "probability of": "P(",
        "probability that": "P(",
        "prob of": "P(",
        "p of": "P(",
        "p open parenthesis": "P(",
        "p(": "P(",
        "p ": "P(",

        # intersection
        "intersection": "∩",
        "cap": "∩",

        # union
        "union": "∪",

        # conditional probability
        "given that": "|",
        "given": "|",

        # letters spacing
        " a ": " A ",
        " b ": " B ",
        " c ": " C ",
    }

    for key, value in replacements.items():
        text = text.replace(key, value)

    # remove duplicated spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()