from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db
from models.users import User

app = Flask(__name__)

#Configurações Banco de DADOS
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

#Configurações do Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@app.route('/login', methods=['POST'])
def login():
  data = request.json
  username = data.get('username')
  password = data.get('password')

  if username and password:
    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
      login_user(user)
    return jsonify({'message': 'Login realizado com sucesso!'})
  return jsonify({'message': 'Dados inválidos'}), 400

@app.route('/logout', methods=['GET'])
@login_required
def logout():
  logout_user()
  return jsonify({'message': 'Logout realizado com sucesso!'})

@app.route('/user', methods=['POST'])
@login_required
def create_user():
  data = request.json
  username = data.get('username')
  password = data.get('password')
  email = data.get('email')

  if username and password:
    new_user = User(username=username, password=password, email=email, role='user')
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Usuário criado com sucesso!'})
  return jsonify({'message': 'Dados inválidos'}), 400

@app.route('/user/<int:id>', methods=['GET'])
@login_required
def get_user(id):
  user_id = User.query.get(id)
  if user_id:
    return jsonify({
      'username': user_id.username, 
      'email': user_id.email, 
      'role': user_id.role
    })
  return jsonify({'message': 'Usuário não encontrado'}), 404

@app.route('/user/<int:id>', methods=['PUT'])
@login_required
def update_user(id):
  data = request.json
  user_id = User.query.get(id)

  if user_id != current_user.id and current_user.role != 'admin':
    return jsonify({'message': 'Você não tem permissão para atualizar este usuário'}), 403
  
  if user_id:
    user_id.password = data.get('password')
    user_id.email = data.get('email')
    user_id.role = data.get('role')
    db.session.commit()
    return jsonify({'message': f'Atualização do usuário {user_id.username} foi realizado com sucesso!'})
  return jsonify({'message': 'Usuário não encontrado'}), 404

@app.route('/user/<int:id>', methods=['DELETE'])
@login_required
def delete_user(id):
  user_id = User.query.get(id)

  if id == current_user.id:
    return jsonify({'message': 'Você não pode excluir sua própria conta'}), 403
  
  if current_user.role != 'admin':
    return jsonify({'message': 'Você não tem permissão para excluir este usuário'}), 403
  
  if user_id:
    db.session.delete(user_id)
    db.session.commit()
    return jsonify({'message': f'O usuário {user_id.username} foi excluído com sucesso!'})
  return jsonify({'message': 'Usuário não encontrado'}), 404
  
if __name__ == '__main__':
  app.run(debug=True)