import os
from flask import Flask, request, render_template, redirect, url_for
from pydub import AudioSegment
import requests
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'m4a', 'wav'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def upload_to_assemblyai(filename, api_key):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    session = requests.Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)

    headers = {
        'authorization': api_key,
        'content-type': 'application/json'
    }

    response = session.post('https://api.assemblyai.com/v2/upload',
                            headers=headers,
                            data=read_file(filename),
                            verify=True)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.json()['upload_url']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Convert the uploaded file to .wav
            audio = AudioSegment.from_file(file_path, format="m4a")
            wav_path = os.path.join(app.config['UPLOAD_FOLDER'], 'converted.wav')
            audio.export(wav_path, format="wav")

            # Transcribe the audio file using AssemblyAI
            api_key = 'your_assemblyai_api_key'  # Replace with your AssemblyAI API key

            try:
                upload_url = upload_to_assemblyai(wav_path, api_key)
                transcript_request = {
                    'audio_url': upload_url
                }

                transcript_response = requests.post('https://api.assemblyai.com/v2/transcript',
                                                    json=transcript_request,
                                                    headers={
                                                        'authorization': api_key,
                                                        'content-type': 'application/json'
                                                    })
                transcript_id = transcript_response.json()['id']

                # Poll the API until transcription is complete
                while True:
                    transcript_result = requests.get(f'https://api.assemblyai.com/v2/transcript/{transcript_id}',
                                                     headers={
                                                         'authorization': api_key
                                                     })
                    result = transcript_result.json()

                    if result['status'] == 'completed':
                        text = result['text']
                        return render_template('index.html', transcription=text)
                    elif result['status'] == 'failed':
                        return render_template('index.html', transcription='Transcription failed.')

                    time.sleep(5)  # Wait for 5 seconds before checking the status again

            except requests.exceptions.RequestException as e:
                return render_template('index.html', transcription=f'Error: {e}')

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
