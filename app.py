from flask import Flask, render_template, request, jsonify, send_file
from ibm_watsonx_ai.foundation_models import Model
import json
from Renan_run import load_model, generate_audio
import os
import warnings
import Paths as p

warnings.filterwarnings(action='ignore', category=FutureWarning)
warnings.filterwarnings(action='ignore', category=UserWarning)

app = Flask(__name__)

# Hasan's directories
config_path = p.sultan_config
checkpoint_dir = p.sultan_checkpoint
driver_dir = p.sultan_driver
Output = p.sultan_output

model = load_model(config_path, checkpoint_dir)

# Set up IBM Watson Model
def get_credentials():
    return {
        "url": "https://eu-de.ml.cloud.ibm.com",
        "apikey": "N8X3zjj2i-jl0WFwLnjW9iERaI75O4XG8uFSaN_bt44M"
    }

model_id = "sdaia/allam-1-13b-instruct"
project_id = "dfecab4f-ecf4-44ab-999d-1e5a330df2fb"
parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 500,
    "stop_sequences": ["\n"],
    "repetition_penalty": 1
}

model = Model(
    model_id=model_id,
    params=parameters,
    credentials=get_credentials(),
    project_id=project_id
)

# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')

# Route for the "About" page
@app.route('/about')
def about():
    return render_template('about.html')

# Route for the "Services" page
@app.route('/services')
def services():
    return render_template('services.html')

# Route for the "Model" page
@app.route('/model')
def model_page():
    return render_template('model.html')

# Route for the "speech-only-gen" page
@app.route('/speech-only-gen')
def speech_only_gen_page():
    return render_template('speech-only-gen.html')

# Route for the "text-speech-gen" page
@app.route('/text-speech-gen')
def text_speech_gen_page():
    return render_template('text-speech-gen.html')

# Route for the "Contact" page
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Route for the "Header" page
@app.route('/header')
def header():
    return render_template('header.html')

# Route for the "Footer" page
@app.route('/footer')
def footer():
    return render_template('footer.html')

# API endpoint for generating text
@app.route('/generate-text', methods=['POST'])
def generate_text():
    data = request.json
    user_input = data.get('input')

    # Generate the response using IBM Watson model
    try:
        generated_response = model.generate_text(prompt=user_input)
        output_text = generated_response.get('generated_text', '')

        # Return the generated text as JSON
        return jsonify({'generated_text': output_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API endpoint for generating audio using the pre-trained model
@app.route('/generate-audio', methods=['POST'])
def generate_audio_route():
    data = request.json
    text = data.get('text', '')
    speaker_id = data.get('speaker_id')
    speed = data.get('speed')
    bg_music_filename = data.get('bg_music_filename')
    
    output_dir = Output
    
    # Generate audio
    generate_audio(model, speaker_id, [text], output_dir, bg_music_filename, speed)
    
    # Find the latest generated file
    files = [f for f in os.listdir(output_dir) if f.endswith('.wav')]
    latest_file = max(files, key=lambda x: os.path.getctime(os.path.join(output_dir, x)))
    output_path = os.path.join(output_dir, latest_file)
    
    return send_file(output_path, as_attachment=True, download_name="generated_audio.wav")

@app.route('/upload-voice', methods=['POST'])
def upload_voice():
    file = request.files.get('file')
    
    if file and file.filename.endswith('.wav'):
        file_path = os.path.join(p.sulatn_speaker, "new.wav")
        file.save(file_path)
        return jsonify({"message": "تم تحميل الملف بنجاح."}), 200
    else:
        return jsonify({"message": "يرجى تحميل ملف بصيغة wav فقط."}), 400

if __name__ == '__main__':
    app.run(debug=True)
