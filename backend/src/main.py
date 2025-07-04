from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

tarefas = []
contador_id = 1

@app.route('/')
def hello_world():
    return jsonify(message='API de Gerenciamento de Tarefas funcionando!')

@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    return jsonify(tarefas)

@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    global contador_id
    dados = request.get_json()
    
    nova_tarefa = {
        'id': contador_id,
        'titulo': dados.get('titulo', ''),
        'descricao': dados.get('descricao', ''),
        'concluida': False
    }
    
    tarefas.append(nova_tarefa)
    contador_id += 1
    
    return jsonify(nova_tarefa), 201

@app.route('/tarefas/<int:tarefa_id>', methods=['PUT'])
def atualizar_tarefa(tarefa_id):
    dados = request.get_json()
    
    for tarefa in tarefas:
        if tarefa['id'] == tarefa_id:
            tarefa['titulo'] = dados.get('titulo', tarefa['titulo'])
            tarefa['descricao'] = dados.get('descricao', tarefa['descricao'])
            tarefa['concluida'] = dados.get('concluida', tarefa['concluida'])
            return jsonify(tarefa)
    
    return jsonify({'erro': 'Tarefa não encontrada'}), 404

@app.route('/tarefas/<int:tarefa_id>', methods=['DELETE'])
def deletar_tarefa(tarefa_id):
    global tarefas
    tarefas = [tarefa for tarefa in tarefas if tarefa['id'] != tarefa_id]
    return jsonify({'mensagem': 'Tarefa deletada com sucesso'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')