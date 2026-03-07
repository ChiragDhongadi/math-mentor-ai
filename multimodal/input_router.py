from multimodal.ocr import extract_text_from_image
from multimodal.audio import transcribe_audio
from pipeline.math_graph import graph


def solve_from_text(text):

    result = graph.invoke({
        "input_type": "text",
        "text_input": text
    })

    return result


def solve_from_image(image_path):

    text, conf = extract_text_from_image(image_path)

    print(f"\nOCR Extracted Text ({conf}):")
    print(text)

    # We bypass the image_node here since we already extracted text
    result = graph.invoke({
        "input_type": "text",
        "text_input": text
    })

    return result


def solve_from_audio(audio_path):

    text, conf = transcribe_audio(audio_path)

    print(f"\nAudio Transcript ({conf}):")
    print(text)

    result = graph.invoke({
        "input_type": "text",
        "text_input": text
    })

    return result
