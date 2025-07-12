from flask import Flask, jsonify, request
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

app = Flask(__name__)
CORS(app)

# Configuração do banco
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://meu_usuario:minha_senha@localhost:5432/meu_banco")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Modelo da tarefa
class Tarefa(Base):
    __tablename__ = 'tarefas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String)
    concluida = Column(Boolean, default=False)

# Cria as tabelas se não existirem
Base.metadata.create_all(engine)

@app.route('/')
def hello_world():
    return jsonify(message='API de Gerenciamento de Tarefas conectada ao PostgreSQL!')

@app.route('/tarefas', methods=['GET'])
def listar_tarefas():
    db = SessionLocal()
    tarefas = db.query(Tarefa).all()
    db.close()
    return jsonify([{
        'id': t.id,
        'titulo': t.titulo,
        'descricao': t.descricao,
        'concluida': t.concluida
    } for t in tarefas])

@app.route('/tarefas', methods=['POST'])
def criar_tarefa():
    dados = request.get_json()
    db = SessionLocal()
    nova_tarefa = Tarefa(
        titulo=dados.get('titulo', ''),
        descricao=dados.get('descricao', ''),
        concluida=False
    )
    db.add(nova_tarefa)
    db.commit()
    db.refresh(nova_tarefa)
    db.close()
    return jsonify({
        'id': nova_tarefa.id,
        'titulo': nova_tarefa.titulo,
        'descricao': nova_tarefa.descricao,
        'concluida': nova_tarefa.concluida
    }), 201

@app.route('/tarefas/<int:tarefa_id>', methods=['PUT'])
def atualizar_tarefa(tarefa_id):
    dados = request.get_json()
    db = SessionLocal()
    tarefa = db.query(Tarefa).get(tarefa_id)
    if not tarefa:
        db.close()
        return jsonify({'erro': 'Tarefa não encontrada'}), 404

    tarefa.titulo = dados.get('titulo', tarefa.titulo)
    tarefa.descricao = dados.get('descricao', tarefa.descricao)
    tarefa.concluida = dados.get('concluida', tarefa.concluida)
    db.commit()
    db.refresh(tarefa)
    db.close()
    return jsonify({
        'id': tarefa.id,
        'titulo': tarefa.titulo,
        'descricao': tarefa.descricao,
        'concluida': tarefa.concluida
    })

@app.route('/tarefas/<int:tarefa_id>', methods=['DELETE'])
def deletar_tarefa(tarefa_id):
    db = SessionLocal()
    tarefa = db.query(Tarefa).get(tarefa_id)
    if not tarefa:
        db.close()
        return jsonify({'erro': 'Tarefa não encontrada'}), 404

    db.delete(tarefa)
    db.commit()
    db.close()
    return jsonify({'mensagem': 'Tarefa deletada com sucesso'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
