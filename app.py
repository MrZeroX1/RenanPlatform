from flask import Flask, render_template, request, jsonify, send_file
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from Renan_run import load_model, generate_audio
import os
import warnings
import Paths as p

warnings.filterwarnings(action='ignore', category=FutureWarning)
warnings.filterwarnings(action='ignore', category=UserWarning)

app = Flask(__name__)

# Hasan's directories
config_path = p.sarah_config
checkpoint_dir = p.sarah_checkpoint
driver_dir = p.sarah_driver
Output = p.sarah_output

model = load_model(config_path, checkpoint_dir)

# Configure Selenium WebDriver
chrome_options = ChromeOptions()
chrome_options.add_argument('--headless')  # Run in headless mode
service = ChromeService(executable_path=driver_dir)

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

# API endpoint for generating text using Selenium
@app.route('/generate-text', methods=['POST'])
def generate_text():
    data = request.json
    user_input = data.get('input')

    # Set up Selenium options for headless browsing
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    try:
        # Navigate to the target website
        driver.get('https://toolbaz.com/writer/ai-story-generator')

        # Find the input field and enter the user text
        input_field = driver.find_element(By.ID, 'input')
        input_field.send_keys(user_input)

        # Wait until the generate button is clickable and then click it
        generate_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'main_btn'))
        )

        # Scroll into view and click the button
        driver.execute_script("arguments[0].scrollIntoView(true);", generate_button)
        driver.execute_script("arguments[0].click();", generate_button)

        # Wait for the output to appear
        WebDriverWait(driver, 15).until(
            EC.visibility_of_element_located((By.ID, 'output'))
        )

        # Get the output text
        output_div = driver.find_element(By.ID, 'output')
        output_html = output_div.get_attribute('innerHTML')

        # Use BeautifulSoup to parse the HTML and extract the text
        soup = BeautifulSoup(output_html, 'html.parser')
        output_text = ''.join(p.get_text() for p in soup.find_all('p'))

    finally:
        driver.quit()

    # Return the sanitized text as JSON
    return jsonify({'generated_text': output_text})


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
        file_path = os.path.join(p.sarah_speaker, "new.wav")
        file.save(file_path)
        return jsonify({"message": "تم تحميل الملف بنجاح."}), 200
    else:
        return jsonify({"message": "يرجى تحميل ملف بصيغة wav فقط."}), 400

if __name__ == '__main__':
    app.run(debug=True)
