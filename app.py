import os
from flask import Flask, jsonify, g
from flask_cors import CORS
from flask_login import LoginManager, login_manager

import models
from resources.user import user
from resources.link import link

login_manager = LoginManager()

DEBUG = False
PORT = 5000

# print(__name__)
app = Flask(__name__)
CORS(app)

app.secret_key = 'IFYOUSTEALTHISINSERTGENERICTHREATHERE'
login_manager.init_app(app)
app.config['CORS_HEADERS'] = 'Content-Type'
@login_manager.user_loader

def load_user(user_id):
    try:
        return models.HMPUser.get(models.HMPUser.id == user_id)
    except models.DoesNotExist:
        return None

@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()

@app.after_request
def after_request(response):
    g.db.close()
    return response

@app.route('/')
def index():
    return 'Hello there'

CORS(user, origins =['http://localhost:3000'], supports_credentials=True)
app.register_blueprint(user, url_prefix='/api/v1/hmpusers')

if 'ON_HEROKU' in os.environ: 
  print('\non heroku!')
  models.initialize()

if __name__ == '__main__':
    models.initialize()
    app.run(debug=DEBUG, port=PORT)