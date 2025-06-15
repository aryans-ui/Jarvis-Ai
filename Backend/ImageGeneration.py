import asyncio
import os
from time import sleep
from PIL import Image
import requests
from dotenv import get_key

# Configs
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {
    "Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}",
    "Content-Type": "application/json"
}

# Ensure folder exists
if not os.path.exists("Data"):
    os.makedirs("Data")

def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for file in files:
        image_path = os.path.join(folder_path, file)
        try:
            img = Image.open(image_path)
            print(f"✅ Opening image: {image_path}")
            img.show()
            sleep(1)
        except Exception as e:
            print(f"❌ Unable to open {image_path}. Error: {e}")


async def query(prompt):
    try:
        res = await asyncio.to_thread(
            requests.post, API_URL, headers=HEADERS, json={"inputs": prompt}
        )
        res.raise_for_status()

        # Some Hugging Face models return raw image bytes directly
        content_type = res.headers.get("Content-Type", "")
        if "image" in content_type:
            return res.content

        # Otherwise it's a JSON response
        result = res.json()
        if isinstance(result, dict) and result.get("error"):
            print("❌ API returned error:", result["error"])
            return None

        print("⚠️ Unknown response type:", result)
        return None

    except requests.exceptions.RequestException as e:
        print(f"❌ API Request failed: {e}")
        return None

async def generate_images(prompt):
    prompt_clean = prompt.replace(" ", "_")
    payload_prompt = f"{prompt}, cinematic, ultra realistic, 8k, trending on artstation"

    tasks = [asyncio.create_task(query(payload_prompt)) for _ in range(4)]
    results = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(results):
        if image_bytes:
            file_path = os.path.join("Data", f"{prompt_clean}{i + 1}.jpg")
            with open(file_path, "wb") as f:
                f.write(image_bytes)
        else:
            print(f"❌ Image {i+1} generation failed.")

def GenerateImages(prompt):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

# Main runner
while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            data = f.read()

        prompt, status = data.split(",")
        prompt = prompt.strip()
        status = status.strip().lower()

        if status == "true":
            print("🎨 Generating Images...")
            GenerateImages(prompt)

            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False, False")
            break
        else:
            sleep(1)
    except:
        sleep(1)
