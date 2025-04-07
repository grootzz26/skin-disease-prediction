import os

# Base directory of the application
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Configuration class
class Config:
    # Flask app configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DEBUG = False
    TESTING = False

    # Upload configuration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'jfif'}

    # Model configuration
    MODEL_JSON_PATH = os.path.join(BASE_DIR, 'model.json')
    MODEL_WEIGHTS_PATH = os.path.join(BASE_DIR, 'model.h5')
    INPUT_SHAPE = (224, 224, 3)

    # Classes
    CLASSES = [
        'Actinic Keratoses',
        'Basal Cell Carcinoma',
        'Benign Keratosis',
        'Dermatofibroma',
        'Melanoma',
        'Melanocytic Nevi',
        'Vascular naevus'
    ]


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
    # In production, you might want to use a more secure secret key
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'


# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}