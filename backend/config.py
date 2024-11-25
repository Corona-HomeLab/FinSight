import os

class Config:
    SECRET_KEY = 'your-secret-key-here'
    DEBUG = True
    DATA_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'finance_data')