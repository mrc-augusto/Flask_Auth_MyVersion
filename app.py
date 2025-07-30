from flask import Flask, request, jsonify
from flask_login import LoginManager, logout_user, login_required, current_user
from database import db
from models.users import User

app = Flask(__name__)

#Configurações Banco de DADOS
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)

#Configurações do Login
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)


if __name__ == '__main__':
  app.run(debug=True)