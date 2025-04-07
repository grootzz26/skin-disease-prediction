import os
from flask import Flask, render_template, request, jsonify

# Import configuration
from config import config_by_name

# Import utility functions
from utils.model_utils import load_model_from_file, predict_disease
from utils.image_utils import allowed_file, save_upload_file

# Get environment setting, default to 'development'
env = os.environ.get('FLASK_ENV', 'development')
config = config_by_name[env]

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config)

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Load the model at startup
model = load_model_from_file(app.config['MODEL_JSON_PATH'], app.config['MODEL_WEIGHTS_PATH'])


@app.route('/', methods=['GET'])
def home():
    """Render the home page"""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle image upload and prediction

    Returns:
        JSON response with prediction results or error message
    """
    if model is None:
        return jsonify({'error': 'Model not loaded properly'}), 500

    # Check if the post request has the file part
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']

    # If user does not select file, browser might also submit an empty part without filename
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if file and allowed_file(file.filename):
        # Save the uploaded file
        filepath = save_upload_file(file, app.config['UPLOAD_FOLDER'])

        # Make prediction
        class_results, prob_results = predict_disease(filepath, model)

        if class_results is None:
            return jsonify({'error': 'Error processing image'}), 500

        # Format results
        results = []
        for i in range(len(class_results)):
            results.append({
                'disease': class_results[i],
                'probability': prob_results[i]
            })

        return jsonify({
            'success': True,
            'predictions': results,
            'top_prediction': {
                'disease': class_results[0],
                'probability': prob_results[0]
            }
        })

    return jsonify({'error': 'File type not allowed'}), 400


@app.route('/model-info', methods=['GET'])
def model_info():
    """
    Provide information about the model

    Returns:
        JSON response with model information
    """
    return jsonify({
        'model_type': 'CNN',
        'classes': app.config['CLASSES'],
        'input_shape': app.config['INPUT_SHAPE'],
        'allowed_formats': list(app.config['ALLOWED_EXTENSIONS'])
    })


if __name__ == '__main__':
    # Set host and port
    port = int(os.environ.get('PORT', 5000))

    # Run the Flask app
    app.run(host='0.0.0.0', port=port)