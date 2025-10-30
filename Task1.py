from flask import Flask, request, send_file, jsonify
import io
from pydub import AudioSegment
import numpy as np
import noisereduce as nr

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "🎧 Audio Denoising Backend is running!"})

@app.route('/denoise', methods=['POST'])
def denoise_audio():
    # ✅ Check if the request has the 'file' part
    if 'file' not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    file = request.files['file']

    # Load the audio
    sound = AudioSegment.from_file(file)
    samples = np.array(sound.get_array_of_samples())

    # Simple noise reduction
    reduced = nr.reduce_noise(y=samples, sr=sound.frame_rate)

    # Convert back to AudioSegment
    clean_audio = AudioSegment(
        reduced.tobytes(),
        frame_rate=sound.frame_rate,
        sample_width=sound.sample_width,
        channels=sound.channels
    )

    # Return cleaned file
    output = io.BytesIO()
    clean_audio.export(output, format="wav")
    output.seek(0)
    return send_file(output, mimetype="audio/wav")

if __name__ == '__main__':
    app.run(debug=True)
