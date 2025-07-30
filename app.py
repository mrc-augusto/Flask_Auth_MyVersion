from flask import Flask, request, jsonify
from flask_login import LoginManager, logout_user, login_required, current_user
from database import db

app = Flask(__name__)


if __name__ == '__main__':
  app.run(debug=True)