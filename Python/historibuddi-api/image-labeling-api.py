import numpy as np
from flask import Flask, request, jsonify
from PIL import Image
import os
import io
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import tensorflow as tf

app = Flask(__name__)

def load_labels(label_file_path):
    """Load class labels from text file"""
    try:
        with open(label_file_path, 'r', encoding='utf-8') as f:
            labels = [line.strip() for line in f.readlines() if line.strip()]
        return labels
    except FileNotFoundError:
        print(f"Warning: Label file '{label_file_path}' not found!")
        return [
            "pecinan di jalan pintu kecil",
            "pembantaian orang cina di batavia tahun 1740",
            "perempuan penenun",
            "tuan tanah cina di tandu"
        ]
    except Exception as e:
        print(f"Error reading label file: {e}")
        return []

classname = load_labels("label.txt")

interpreter = tf.lite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

def load_image_from_bytes(image_bytes, size):
    """Load and preprocess image from bytes"""
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    image = image.resize(size)
    image = np.array(image, dtype=np.float32) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

@app.route('/predict', methods=["POST"])
def predict():
    try:
        if 'image' not in request.files:
            return jsonify({
                'error': 'No image file provided',
                'message': 'Please upload an image file with key "image"'
            }), 400
                
        file = request.files['image']
        if file.filename == '':
            return jsonify({
                'error': 'No file selected',
                'message': 'Please select an image file'
            }), 400

        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}
        if not ('.' in file.filename and 
                file.filename.rsplit('.', 1)[1].lower() in allowed_extensions):
            return jsonify({
                'error': 'Invalid file format',
                'message': 'Please upload a valid image file (PNG, JPG, JPEG, GIF, BMP, WEBP)'
            }), 400

        image_bytes = file.read()
        input_shape = input_details[0]['shape']
        height, width = input_shape[1], input_shape[2]
        
        processed_image = load_image_from_bytes(image_bytes, (width, height))
        interpreter.set_tensor(input_details[0]['index'], processed_image)
        interpreter.invoke()
        
        predictions = interpreter.get_tensor(output_details[0]['index'])[0]
        top_index = np.argmax(predictions)

        confidence = float(predictions[top_index])

        if confidence < 0.6:
            return jsonify({
            'success': True,
            'filename': file.filename,
            'predicted_class': 'tidak terdeteksi',
            'confidence': confidence,
            'probability': f"{confidence * 100:.2f}%",
            'model_info': {
                'input_shape': input_shape.tolist(),
                'total_classes': len(classname)
                }
            }), 200

        if top_index >= len(classname):
            return jsonify({
                'success': False,
                'error': 'Invalid prediction index',
                'message': 'Model prediction index out of range'
            }), 500
        response = {
            'success': True,
            'filename': file.filename,
            'predicted_class': classname[top_index],
            'confidence': float(predictions[top_index]),
            'probability': f"{float(predictions[top_index]) * 100:.2f}%",
            'model_info': {
                'input_shape': input_shape.tolist(),
                'total_classes': len(classname)
            }
        }
                
        return jsonify(response), 200
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Prediction failed',
            'message': str(e)
        }), 500

@app.route('/info', methods=['GET'])
def model_info():
    """Get model information"""
    return jsonify({
        'model_path': 'model.tflite',
        'input_details': {
            'shape': input_details[0]['shape'].tolist(),
            'dtype': str(input_details[0]['dtype'])
        },
        'output_details': {
            'shape': output_details[0]['shape'].tolist(),
            'dtype': str(output_details[0]['dtype'])
        },
        'classes': classname,
        'total_classes': len(classname)
    }), 200

if __name__ == '__main__':
    print(f"Model loaded successfully!")
    print(f"Available classes: {len(classname)}")
    print(f"Input shape: {input_details[0]['shape']}")
    print(f"Starting Flask server...")
    app.run(debug=True, host='0.0.0.0', port=5003)

    