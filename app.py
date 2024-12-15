from flask import Flask, request, jsonify, render_template
import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.applications.vgg16 import preprocess_input
from PIL import Image
import io
import numpy as np

app = Flask(__name__)

# Load model (pastikan model sudah dilatih dan disimpan dalam format .h5)
model = tf.keras.models.load_model('model/training_efficiennet.h5')
model.compile(optimizer=Adam(), loss='categorical_crossentropy', metrics=['accuracy'])

# Folder untuk menyimpan file yang diupload
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Fungsi untuk memproses gambar dan melakukan prediksi
def predict_image(img_path):
    try:
        img = image.load_img(img_path, target_size=(224, 224))  # Sesuaikan ukuran input model
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)  # Membuat batch
        img_array /= 255.0  # Normalisasi (jika diperlukan)
        
        # Prediksi
        predictions = model.predict(img_array)
        # class_idx = np.argmax(predictions, axis=1)[0]
        
        # Cek apakah prediksi mengembalikan nilai
        if predictions is not None and predictions.size > 0:
            class_idx = np.argmax(predictions, axis=1)[0] 

            # Map hasil prediksi ke jenis tumor
            tumor_classes = ['glioma', 'meningioma', 'notumor', 'pituitary']
            predicted_class = tumor_classes[class_idx]
            return predicted_class
        else:
            return "Error: No predictions returned"
    except Exception as e:
        return str(e)
    
@app.route('/api/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        # Proses gambar dan lakukan prediksi
        result = predict_image(file)
        
        # Kirim hasil prediksi dalam format JSON
        return jsonify({'prediction': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
