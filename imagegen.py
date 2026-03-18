import requests
from PIL import Image
from io import BytesIO
from datetime import datetime
from configure import HF_API_KEY
API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
def generate(prompt: str) -> Image.Image:
    headers = {
        "Authorization": f"Bearer {HF_API_KEY}",
        "Accept": "image/png"
    }
    payload = {
        "inputs": prompt,
        "options": {
            "wait_for_model": True
        }
    }
    response = requests.post(API_URL, headers=headers,json=payload,timeout=60)
    if response.status_code != 200:
        try:
            error_data = response.json()
            raise Exception(error_data.get("error", "Unknown API Error"))
        except ValueError:
            raise Exception(response.text)
    return Image.open(BytesIO(response.content))
def save_image(image: Image.Image) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"IMG_{timestamp}.png"
    image.save(file_name)
    return file_name
def main():
    print("Text-to-Image Generator")
    print("Type 'exit' to quit.\n")
    while True:
        prompt = input("Enter image dscription:\n").strip()
        if prompt.lower() == "exit":
            print("Session terminated")
            break
        print("\nGenerating image...")
        try:
            image = generate(prompt)
            saved_file = save_image(image)
            print(f"Image automatically saved as: {saved_file}\n")
        except Exception as e:
            print(f"Operational error: {e}\n")
if __name__ == "__main__":
    main()