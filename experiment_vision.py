import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai.errors import APIError
from PIL import Image

load_dotenv()

target_img = os.path.join("samples", "class_photo.jpeg")
print(f"Testing Gemini Vision on: {target_img}")

client = genai.Client()
pil_img = Image.open(target_img)

prompt = (
    "Count the exact number of students sitting in this university classroom. "
    "Ignore the lecturer if standing at the front. Return ONLY the integer number first, "
    "followed by a short 1-sentence explanation of visibility."
)

# רשימת מודלים לגיבוי למקרה של עומס 503 בשרת
candidate_models = ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3.8-pro"]

for model_name in candidate_models:
    try:
        print(f"Trying {model_name}...")
        response = client.models.generate_content(
            model=model_name,
            contents=[pil_img, prompt]
        )
        print(f"\n[Gemini Vision - {model_name}] {response.text.strip()}")
        break
    except APIError as e:
        print(f"Model {model_name} unavailable ({e.code}), falling back...")
        time.sleep(1)