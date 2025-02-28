from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import io
from PIL import Image
import openai
import random

openai.api_key = "sk-..."  # Replace with your actual OpenAI API key or environment variable

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

funny_names = [
    "Meme-a-tron", "Dankinator 5000", "Lord Captionstein", 
    "RoastBot XL", "Caption Wizard", "Meme Supreme", "The Memefather"
]

def generate_meme_caption(image_bytes):
    image = Image.open(io.BytesIO(image_bytes))

    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {"role": "system", "content": "You are a meme expert who writes savage, funny, or clever captions for images."},
            {"role": "user", "content": "Here's an image. Give me 3 funny meme captions:"},
            {"role": "user", "content": {"image": image_bytes}}
        ],
        max_tokens=200,
    )

    captions = response['choices'][0]['message']['content'].strip().split('\n')
    return captions

@app.get("/intro")
def get_intro():
    name = random.choice(funny_names)
    return {"intro": f"Welcome to {name}, your personal meme overlord."}

@app.post("/generate-meme/")
async def generate_meme(file: UploadFile = File(...)):
    image_bytes = await file.read()
    captions = generate_meme_caption(image_bytes)
    return {"captions": captions}