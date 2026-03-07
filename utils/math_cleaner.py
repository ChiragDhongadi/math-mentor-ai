import re

def clean_math_text(text):

    # normalize spaces
    text = re.sub(r"\s+", " ", text)

    # fix superscripts
    text = text.replace("²", "^2")
    text = text.replace("³", "^3")

    # fix missing equals
    text = text.replace("g(t) t", "g(t) = t")

    # fix common OCR math mistakes
    text = text.replace("t^cos", "t^3 cos")
    text = text.replace("x^cos", "x^3 cos")

    # fix x2 -> x^2
    text = re.sub(r'([a-zA-Z])2', r'\1^2', text)

    return text.strip()