from flask import Flask 
app = Flask(__name__)


from flask_wtf.csrf import CSRFProtect
import os
app.secret_key = os.urandom(24)  # Generates a random key for Flask
csrf = CSRFProtect(app) # A CSRF token is a random string that is used to prevent cross-site request forgery attacks, which are a type of web security vulnerability where an attacker can trick a user into submitting a malicious request to a web application

