import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'finance_data')