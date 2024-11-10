from flask import Flask, render_template, request, redirect, url_for, session
import openai
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, AudioConfig
import os
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Configure OpenAI API and Azure TTS
openai.api_key = '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'
speech_config = SpeechConfig(subscription="8xv0nkacjMKKNsYOYpi22YvFEi9Td8yLV8kvrKNqPhMMUF5sOuXbJQQJ99AKACYeBjFXJ3w3AAAYACOGuDU6", region="eastus")
speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"  # Sweet, natural voice

# Utility functions
def generate_comic_panels(story_title, story_outline, num_panels=10):
    prompt = f"""
    Create a detailed comic strip for the story titled '{story_title}'.
    Story Outline: {story_outline}
    Generate {num_panels} comic panels. Each panel should include:
    - Scene Description: A vivid portrayal of the setting and atmosphere.
    Character Actions: Specific actions or expressions that drive the story forward.
    Narration: Engaging text that enhances the storytelling, adding depth and intrigue to each scene.
    Ensure the narration aligns with the mood and pacing of the story, making the comic strip captivating and dynamic.
    Return the result as a JSON array with each panel containing 'scene', 'dialogue', and 'actions'.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a creative assistant."},
                  {"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=3000
    )
    return json.loads(response['choices'][0]['message']['content'])

def generate_comic_images_from_panels(panels, style_reference=None):
    images = {}
    for idx, panel in enumerate(panels):
        prompt = (
            f"Create a comic panel in a consistent art style. "
            f"Scene: {panel['scene']} "
            f"Actions: {panel['actions']} "
            f"Do not include any text or dialogue in the image. "
            f"Focus on visual consistency across all panels. "
        )
        if style_reference:
            prompt += f"Maintain this specific art style: {style_reference}. "

        try:
            image_response = openai.Image.create(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                n=1
            )
            images[f"Panel {idx + 1}"] = image_response['data'][0]['url']
            print('a')
        except Exception as e:
            images[f"Panel {idx + 1}"] = f"Error: {e}"
    return images

def generate_tts_audio(panels):
    audio_files = []
    for idx, panel in enumerate(panels):
        audio_output = AudioConfig(filename=f"static/panel_{idx+1}.wav")
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_output)
        synthesizer.speak_text(panel['dialogue'])
        audio_files.append(f"static/panel_{idx+1}.wav")
    return audio_files

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        story_title = request.form['story_title']
        story_outline = request.form['story_outline']
        style_reference = request.form.get('style_reference', None)

        panels = generate_comic_panels(story_title, story_outline)
        print(panels)
        images = generate_comic_images_from_panels(panels, style_reference=style_reference)
        audio_files = generate_tts_audio(panels)

        session['panels'] = panels
        session['images'] = images
        session['audio_files'] = audio_files
        session['current_panel'] = 0

        return redirect(url_for('index.html'))

    return render_template('index.html')

@app.route('/comic_panel', methods=['GET', 'POST'])
def comic_panel():
    if 'panels' not in session:
        return redirect(url_for('index'))

    current_panel = session['current_panel']
    panels = session['panels']
    images = session['images']
    audio_files = session['audio_files']

    if request.method == 'POST':
        if 'next' in request.form:
            session['current_panel'] += 1
        return redirect(url_for('comic_panel'))

    return render_template('comic_panel.html', 
                           panel=panels[current_panel], 
                           image=images[f"Panel {current_panel + 1}"], 
                           audio=audio_files[current_panel],
                           panel_number=current_panel + 1,
                           total_panels=len(panels))

if __name__ == '__main__':
    app.run(debug=True)