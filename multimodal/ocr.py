import easyocr
import cv2
import re

# initialize reader
reader = easyocr.Reader(['en'])


def clean_math_text(text):
    text = text.replace("²", "^2")
    text = text.replace("³", "^3")
    text = re.sub(r'([a-zA-Z])2', r'\1^2', text)
    text = text.replace("?", "^")
    return text


def extract_text_from_image(image_path):
    """
    Extract text and OCR confidence from image
    """

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError(f"Image not found: {image_path}")

    results = reader.readtext(image)

    extracted_text = []
    confidences = []

    for (_, text, confidence) in results:
        extracted_text.append(text)
        confidences.append(confidence)

    # Combine text
    text = " ".join(extracted_text)

    # Compute average confidence
    if confidences:
        avg_confidence = sum(confidences) / len(confidences)
    else:
        avg_confidence = 0.0

    cleaned_text = clean_math_text(text)

    return cleaned_text, avg_confidence


if __name__ == "__main__":

    image_path = r"D:\Math Mentor application\image.png"

    text = extract_text_from_image(image_path)

    print("\nExtracted text:")
    print(text)