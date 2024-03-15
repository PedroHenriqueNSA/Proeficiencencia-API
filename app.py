from flask import Flask, jsonify, request
import jwt
import datetime

app = Flask(__name__)

# Chave secreta para assinar o token JWT
app.config['SECRET_KEY'] = '12345678'

usuarios = [
    {
        'id': 1,
        'nome':'Pedro Henrique',
        'empresa': 'Sony',
        'telefone': '12345678',
        'email': 'pedro.santos14@estudante.ifb.edu.br',
        'senha': '12345678'
    },
    {
        'id': 2,
        'nome':'Otavio Davilla',
        'empresa': 'Sony',
        'telefone': '12345678',
        'email': 'otavio@gmail.com',
        'senha': '12345678'
    },
    {
        'id': 3,
        'nome':'Pedro de Carvalho',
        'empresa': 'Sony',
        'telefone': '12345678',
        'email': 'pedro@gmail.com',
        'senha': '12345678'
    },
]

# Consultar(todos)
@app.route('/usuarios',methods=['GET'])
def obter_usuarios():
    return jsonify(usuarios)

# Consultar(id)
@app.route('/usuarios/<int:id>',methods=['GET'])
def obter_usuarios_por_id(id):
    for usuario in usuarios:
        if usuario.get('id') == id:
            return jsonify(usuario)
    return jsonify({'erro': 'Usuário não encontrado'}), 404

# Rota para recuperar usuário logado
@app.route('/perfis/<int:id>', methods=['GET'])
def obter_perfil_por_id(id):
    for usuario in usuarios:
        if usuario['id'] == id:
            return jsonify({'id': usuario['id'], 'nome': usuario['nome'], 'email': usuario['email']})
    return jsonify({'erro': 'Usuário não encontrado'}), 404

# Editar
@app.route('/usuarios/<int:id>',methods=['PUT'])
def editar_usuarios_por_id(id):
    usuarios_alterado = request.get_json()
    for indice, usuario in enumerate(usuarios):
        if usuario.get('id') == id:
            usuarios[indice].update(usuarios_alterado)
            return jsonify(usuarios[indice])
    return jsonify({'erro': 'Usuário não encontrado'}), 404

# Criar
@app.route('/usuarios',methods=['POST'])
def incluir_novo_usuarios():
    novo_usuario = {'id': len(usuarios) + 1, **request.get_json()}
    usuarios.append(novo_usuario)
    return jsonify(novo_usuario)

# Autenticação
@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Falha na autenticação'}), 401

    usuario = next((usuario for usuario in usuarios if usuario['email'] == auth.username and usuario['senha'] == auth.password), None)

    if not usuario:
        return jsonify({'message': 'Falha na autenticação'}), 401

    token = jwt.encode({'email': usuario['email'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])

    return jsonify({'token': token})

# Excluir
@app.route('/usuarios/<int:id>',methods=['DELETE'])
def excluir_usuarios(id):
    for indice, usuario in enumerate(usuarios):
        if usuario.get('id') == id:
            del usuarios[indice]
            break
    else:
        return jsonify({'erro': 'Usuário não encontrado'}), 404
    return jsonify(usuarios)

if __name__ == '__main__':
    app.run(port=5000,host='localhost',debug=True)
