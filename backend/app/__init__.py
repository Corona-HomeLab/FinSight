from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    from app.routes.main import main
    from app.routes.api import api
    
    app.register_blueprint(main)
    app.register_blueprint(api)
    
    return app