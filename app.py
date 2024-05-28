from flask import Flask 
from flask_wtf.csrf import CSRFProtect
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
csrf = CSRFProtect(app)
