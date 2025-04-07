import numpy as np
from tensorflow.keras.models import model_from_json
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Define disease classes
CLASSES = [
    'Actinic Keratoses',
    'Basal Cell Carcinoma',
    'Benign Keratosis',
    'Dermatofibroma',
    'Melanoma',
    'Melanocytic Nevi',
    'Vascular naevus'
]


def load_model_from_file(model_json_path, model_weights_path):
    """
    Load model architecture from JSON file and weights from H5 file

    Args:
        model_json_path (str): Path to model architecture JSON file
        model_weights_path (str): Path to model weights H5 file

    Returns:
        model: Loaded Keras model
    """
    try:
        # Load model architecture from JSON file
        with open(model_json_path, 'r') as json_file:
            loaded_model_json = json_file.read()

        # Create model from JSON
        model = model_from_json(loaded_model_json)

        # Load weights
        model.load_weights(model_weights_path)

        # Compile the model
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )

        print("Model loaded successfully.")
        return model
    except Exception as e:
        print(f"Error loading model: {e}")
        return None


def predict_disease(filepath, model, top_n=3):
    """
    Predict disease from image file

    Args:
        filepath (str): Path to image file
        model: Loaded Keras model
        top_n (int): Number of top predictions to return

    Returns:
        tuple: (list of predicted classes, list of prediction probabilities)
    """
    try:
        # Load and preprocess image
        img = load_img(filepath, target_size=(224, 224))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array.astype('float32') / 255.0

        # Make prediction
        prediction = model.predict(img_array)

        # Process results
        result_dict = {}
        for i, prob in enumerate(prediction[0]):
            result_dict[prob] = CLASSES[i]

        # Sort probabilities in descending order
        sorted_probs = sorted(prediction[0], reverse=True)

        # Get top predictions
        top_classes = []
        top_probs = []

        for i in range(min(top_n, len(sorted_probs))):
            prob = sorted_probs[i]
            top_classes.append(result_dict[prob])
            top_probs.append(round(float(prob * 100), 2))

        return top_classes, top_probs
    except Exception as e:
        print(f"Error in prediction: {e}")
        return None, None