# Skin Disease Prediction System

A web application for predicting skin diseases from uploaded images using a pre-trained deep learning model.

## Features

- Upload skin lesion images via a user-friendly interface
- Real-time image preprocessing and analysis
- Display top 3 prediction results with confidence scores
- Support for multiple image formats (JPG, JPEG, PNG, JFIF)
- Responsive design for desktop and mobile devices

## Technologies Used

- **Backend:** Flask (Python)
- **Deep Learning:** TensorFlow/Keras
- **Frontend:** HTML, CSS, JavaScript, Bootstrap
- **Image Processing:** Pillow, NumPy

## Project Structure

```
skin_disease_prediction/
│
├── app.py                      # Main Flask application file
├── model.json                  # Model architecture
├── model.h5                    # Model weights
├── requirements.txt            # Project dependencies
│
├── static/                     # Static files
│   ├── css/
│   │   └── style.css           # Custom CSS styles
│   ├── js/
│   │   └── main.js             # JavaScript for frontend functionality
│   └── images/                 # Images for UI
│
├── templates/                  # Flask HTML templates
│   ├── index.html              # Main page with upload form
│   ├── layout.html             # Base template layout
│   └── result.html             # Optional separate result page
│
├── uploads/                    # Directory for uploaded images
│
├── utils/                      # Utility modules
│   ├── __init__.py             # Make utils a proper package
│   ├── model_utils.py          # Functions for model loading and prediction
│   └── image_utils.py          # Image processing functions
│
├── config.py                   # Configuration settings
└── README.md                   # Project documentation
```

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd skin_disease_prediction
   ```

2. Create and activate a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Ensure you have the model files:
   - `model.json` - Model architecture
   - `model.h5` - Model weights

   Place these files in the root directory of the project.

### Running the Application

1. Start the Flask application:
   ```
   python app.py
   ```

2. Open a web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Model Information

The prediction model is a Convolutional Neural Network (CNN) trained to classify skin lesions into seven categories:

1. Actinic Keratoses
2. Basal Cell Carcinoma
3. Benign Keratosis
4. Dermatofibroma
5. Melanoma
6. Melanocytic Nevi
7. Vascular naevus

## Deployment

For production deployment:

1. Set the environment variable:
   ```
   export FLASK_ENV=production
   ```

2. Consider using a production WSGI server like Gunicorn:
   ```
   gunicorn app:app
   ```

## Disclaimer

This application is intended for educational and demonstration purposes only. It should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare provider for medical concerns.

## License

[MIT License](LICENSE)