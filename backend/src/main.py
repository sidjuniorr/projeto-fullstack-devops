import os
import psycopg2
from flask import Flask, request, jsonify
from flask_cors import CORS

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)

    if test_config:
        app.config.update(test_config)

    DATABASE_URL = os.getenv("DATABASE_URL") or app.config.get("DATABASE_URL", "postgresql://postgres:postgres123@postgres-service:5432/tarefas_db")
    app.config["DATABASE_URL"] = DATABASE_URL

    def get_db_connection():
        return psycopg2.connect(app.config["DATABASE_URL"])

    def init_db():
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tarefas (
                    id SERIAL PRIMARY KEY,
                    titulo VARCHAR(200) NOT NULL,
                    descricao TEXT,
                    concluida BOOLEAN DEFAULT FALSE,
                    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            cur.close()
            conn.close()
        except Exception as e:
            print(f"Erro ao inicializar banco: {e}")

    app.get_db_connection = get_db_connection
    app.init_db = init_db

    if not app.config.get("TESTING"):
        init_db()

    @app.route("/")
    def home():
        return jsonify({"message": "API de Tarefas com PostgreSQL"})

    @app.route("/tarefas", methods=["GET"])
    def listar_tarefas():
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT id, titulo, descricao, concluida, data_criacao FROM tarefas")
            tarefas = cur.fetchall()
            cur.close()
            conn.close()

            result = []
            for tarefa in tarefas:
                result.append({
                    "id": tarefa[0],
                    "titulo": tarefa[1],
                    "descricao": tarefa[2],
                    "concluida": tarefa[3],
                    "data_criacao": tarefa[4].isoformat() if tarefa[4] else None
                })
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/tarefas", methods=["POST"])
    def criar_tarefa():
        try:
            data = request.get_json()
            if not data or "titulo" not in data:
                return jsonify({"error": "Título é obrigatório"}), 400

            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO tarefas (titulo, descricao, concluida) VALUES (%s, %s, %s) RETURNING id",
                (data["titulo"], data.get("descricao", ""), data.get("concluida", False))
            )
            tarefa_id = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()

            return jsonify({"id": tarefa_id, "message": "Tarefa criada com sucesso"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/tarefas/<int:tarefa_id>", methods=["PUT"])
    def atualizar_tarefa(tarefa_id):
        try:
            data = request.get_json()
            conn = get_db_connection()
            cur = conn.cursor()

            updates = []
            values = []

            if "titulo" in data:
                updates.append("titulo = %s")
                values.append(data["titulo"])
            if "descricao" in data:
                updates.append("descricao = %s")
                values.append(data["descricao"])
            if "concluida" in data:
                updates.append("concluida = %s")
                values.append(data["concluida"])

            if updates:
                values.append(tarefa_id)
                query = f"UPDATE tarefas SET {', '.join(updates)} WHERE id = %s"
                cur.execute(query, values)
                conn.commit()

            cur.close()
            conn.close()
            return jsonify({"message": "Tarefa atualizada com sucesso"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/tarefas/<int:tarefa_id>", methods=["DELETE"])
    def deletar_tarefa(tarefa_id):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM tarefas WHERE id = %s", (tarefa_id,))
            conn.commit()
            cur.close()
            conn.close()
            return jsonify({"message": "Tarefa deletada com sucesso"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/health")
    def health_check():
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.close()
            conn.close()
            return jsonify({"status": "healthy", "database": "connected"})
        except Exception as e:
            return jsonify({"status": "unhealthy", "database": "disconnected", "error": str(e)}), 500

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
