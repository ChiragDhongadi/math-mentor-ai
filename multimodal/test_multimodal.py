from multimodal.input_router import solve_from_text, solve_from_image, solve_from_audio


print("TEXT TEST")
result = solve_from_text("Find derivative of x^2 + 3x")
print(result["solution"])


print("\nIMAGE TEST")
result = solve_from_image("image.png")
print(result["solution"])


print("\nAUDIO TEST")
result = solve_from_audio("sumit_tts_audio.mp3")
print(result["solution"])