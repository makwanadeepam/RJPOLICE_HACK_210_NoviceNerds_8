from flask import Flask, render_template, request
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.inception_v3 import InceptionV3, preprocess_input, decode_predictions
import numpy as np

app = Flask(__name__)
model = InceptionV3(weights='imagenet')

def detect_deepfake(video_path):
    img = image.load_img(video_path, target_size=(299, 299))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)
    predictions = model.predict(img_array)
    decoded_predictions = decode_predictions(predictions)
    return decoded_predictions

@app.route('/upload', methods=['POST'])
def upload():
    result = None

    if 'video' not in request.files:
        return render_template('index.html', result='Error: No video file provided')

    video_file = request.files['video']

    if video_file.filename == '':
        return render_template('index.html', result='Error: No selected file')

    video_path = 'temp_video.mp4'
    video_file.save(video_path)

    predictions = detect_deepfake(video_path)
    result = 'Fake' if predictions else 'Real'

    return render_template('index.html', result=result)

@app.route('/')
def index():
    return render_template('index.html', result=None)

if __name__ == '__main__':
    app.run(debug=True)
