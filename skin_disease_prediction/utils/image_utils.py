import os
import uuid
import numpy as np
from PIL import Image
from werkzeug.utils import secure_filename

# Set of allowed file extensions
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'jfif'}


def allowed_file(filename):
    """
    Check if a file has allowed extension

    Args:
        filename (str): Name of the file to check

    Returns:
        bool: True if file has allowed extension, False otherwise
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_upload_file(file, upload_folder):
    """
    Save uploaded file with a unique name to prevent filename conflicts

    Args:
        file: Flask file object
        upload_folder (str): Directory to save the file

    Returns:
        str: Path to the saved file
    """
    # Create upload folder if it doesn't exist
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # Generate a secure filename
    filename = secure_filename(file.filename)

    # Add a UUID to make filename unique
    unique_filename = f"{uuid.uuid4()}_{filename}"

    # Full path for saving the file
    filepath = os.path.join(upload_folder, unique_filename)

    # Save the file
    file.save(filepath)

    return filepath


def preprocess_image(image_path, target_size=(224, 224)):
    """
    Preprocess image for model prediction

    Args:
        image_path (str): Path to the image file
        target_size (tuple): Target size for resizing (height, width)

    Returns:
        numpy.ndarray: Preprocessed image array
    """
    try:
        # Open the image
        img = Image.open(image_path)

        # Resize image to target size
        img = img.resize(target_size)

        # Convert image to array
        img_array = np.array(img)

        # Check if image is grayscale and convert to RGB if needed
        if len(img_array.shape) == 2:
            img_array = np.stack((img_array,) * 3, axis=-1)
        elif img_array.shape[2] == 1:
            img_array = np.repeat(img_array, 3, axis=2)
        elif img_array.shape[2] == 4:  # Handle RGBA
            img_array = img_array[:, :, :3]

        # Add batch dimension and normalize
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array.astype('float32') / 255.0

        return img_array

    except Exception as e:
        print(f"Error preprocessing image: {e}")
        return None