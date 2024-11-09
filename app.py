import json
import requests
import os
from dotenv import load_dotenv

from flask import Flask, request, render_template, redirect, url_for, flash
# Load environment variables from .env file
load_dotenv()

# Azure OpenAI and DALL·E configuration
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
DEPLOYMENT_NAME = os.getenv("DEPLOYMENT_NAME")
API_KEY = os.getenv("AZURE_API_KEY")

DALL_E_API_ENDPOINT = os.getenv("DALL_E_API_ENDPOINT")  # Replace with your DALL·E endpoint
DALL_E_API_KEY = os.getenv("DALL_E_API_KEY")  # Replace with your DALL·E API key
print(API_KEY)
# Headers for Azure OpenAI API
openai_headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}

# Headers for DALL·E API
dalle_headers = {
    "Authorization": f"Bearer {DALL_E_API_KEY}",
    "Content-Type": "application/json"
}

# Flask application
app = Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html')

# Route to generate comic panels using GPT-4
@app.route('/generate_panels', methods=['POST'])
def generate_panels():
    try:
        data = request.json
        story_title = data.get("title", "")
        story_outline = data.get("outline", "")

        # GPT-4 prompt for generating comic panels
        prompt = f"""
        Create a detailed comic strip for the story titled '{story_title}'.
        Story Outline: {story_outline}
        Generate 12 comic panels. Each panel should include:
        - Scene description
        - Character actions
        - Dialogues

        Return the result as a JSON array with each panel containing 'scene', 'dialogue', and 'actions'.
        """

        payload = {
            "prompt": prompt,
            "max_tokens": 1000,
            "temperature": 0.7,
            "top_p": 0.9,
            "n": 1
        }

        response = requests.post(
            f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{DEPLOYMENT_NAME}/completions?api-version=2022-12-01",
            headers=openai_headers,
            json=payload
        )

        if response.status_code == 200:
            panels = response.json()['choices'][0]['text'].strip()
            return jsonify({"panels": panels})
        else:
            return jsonify({"error": f"Error {response.status_code}: {response.text}"}), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to generate images using DALL·E
@app.route('/generate_images', methods=['POST'])
def generate_images():
    try:
        data = request.json
        panel_descriptions = data.get("panel_descriptions", [])

        generated_images = []
        for description in panel_descriptions:
            payload = {
                "prompt": description,
                "n": 1,
                "size": "512x512"
            }

            response = requests.post(
                DALL_E_API_ENDPOINT,
                headers=dalle_headers,
                json=payload
            )

            if response.status_code == 200:
                image_url = response.json()['data'][0]['url']  # Assuming response contains 'url'
                generated_images.append({"description": description, "image_url": image_url})
            else:
                generated_images.append({"description": description, "error": response.text})

        return jsonify({"generated_images": generated_images})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(debug=True)
