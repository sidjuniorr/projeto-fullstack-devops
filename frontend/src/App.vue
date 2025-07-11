<template>
  <div id="app">
    <h1>Gerenciador de Tarefas</h1>
    
    <div class="form-container">
      <h2>Adicionar Nova Tarefa</h2>
      <form @submit.prevent="adicionarTarefa">
        <input 
          v-model="novaTarefa.titulo" 
          type="text" 
          placeholder="Título da tarefa" 
          required
        />
        <textarea 
          v-model="novaTarefa.descricao" 
          placeholder="Descrição da tarefa"
          rows="3"
        ></textarea>
        <button type="submit">Adicionar Tarefa</button>
      </form>
    </div>

    <div class="tarefas-container">
      <h2>Minhas Tarefas</h2>
      <div v-if="tarefas.length === 0" class="no-tasks">
        Nenhuma tarefa encontrada. Adicione uma nova tarefa acima!
      </div>
      <div v-else>
        <div 
          v-for="tarefa in tarefas" 
          :key="tarefa.id" 
          class="tarefa-item"
          :class="{ 'concluida': tarefa.concluida }"
        >
          <div class="tarefa-content">
            <h3>{{ tarefa.titulo }}</h3>
            <p>{{ tarefa.descricao }}</p>
          </div>
          <div class="tarefa-actions">
            <button 
              @click="alternarConclusao(tarefa)"
              :class="tarefa.concluida ? 'btn-desfazer' : 'btn-concluir'"
            >
              {{ tarefa.concluida ? 'Desfazer' : 'Concluir' }}
            </button>
            <button @click="excluirTarefa(tarefa.id)" class="btn-excluir">
              Excluir
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

const API_URL = 'http://localhost:5000'

export default {
  name: 'App',
  data() {
    return {
      tarefas: [],
      novaTarefa: {
        titulo: '',
        descricao: ''
      }
    }
  },
  async mounted() {
    await this.carregarTarefas()
  },
  methods: {
    async carregarTarefas() {
      try {
        const response = await axios.get(`${API_URL}/tarefas`)
        this.tarefas = response.data
      } catch (error) {
        console.error('Erro ao carregar tarefas:', error)
        alert('Erro ao carregar tarefas. Verifique se o backend está rodando.')
      }
    },
    
    async adicionarTarefa() {
      if (!this.novaTarefa.titulo.trim()) {
        alert('Por favor, insira um título para a tarefa.')
        return
      }
      
      try {
        const response = await axios.post(`${API_URL}/tarefas`, this.novaTarefa)
        this.tarefas.push(response.data)
        this.novaTarefa = { titulo: '', descricao: '' }
      } catch (error) {
        console.error('Erro ao adicionar tarefa:', error)
        alert('Erro ao adicionar tarefa.')
      }
    },
    
    async alternarConclusao(tarefa) {
      try {
        const tarefaAtualizada = { ...tarefa, concluida: !tarefa.concluida }
        await axios.put(`${API_URL}/tarefas/${tarefa.id}`, tarefaAtualizada)
        tarefa.concluida = !tarefa.concluida
      } catch (error) {
        console.error('Erro ao atualizar tarefa:', error)
        alert('Erro ao atualizar tarefa.')
      }
    },
    
    async excluirTarefa(tarefaId) {
      if (!confirm('Tem certeza que deseja excluir esta tarefa?')) {
        return
      }
      
      try {
        await axios.delete(`${API_URL}/tarefas/${tarefaId}`)
        this.tarefas = this.tarefas.filter(tarefa => tarefa.id !== tarefaId)
      } catch (error) {
        console.error('Erro ao excluir tarefa:', error)
        alert('Erro ao excluir tarefa.')
      }
    }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Arial', sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f5f5f5;
  min-height: 100vh;
}

h1 {
  text-align: center;
  color: #333;
  margin-bottom: 30px;
  font-size: 2.5em;
}

.form-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
  margin-bottom: 30px;
}

.form-container h2 {
  color: #333;
  margin-bottom: 15px;
}

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

input, textarea {
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

input:focus, textarea:focus {
  outline: none;
  border-color: #66a6f0;
}

button {
  padding: 12px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
  transition: background-color 0.3s;
}

button[type="submit"] {
  background-color: #66a6f0;
  color: white;
}

button[type="submit"]:hover {
  background-color: #66a6f0;
}

.tarefas-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.tarefas-container h2 {
  color: #333;
  margin-bottom: 20px;
}

.no-tasks {
  text-align: center;
  color: #666;
  font-style: italic;
  padding: 40px;
}

.tarefa-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 4px;
  margin-bottom: 10px;
  background-color: #fafafa;
}

.tarefa-item.concluida {
  opacity: 0.7;
  background-color: #e8f5e8;
}

.tarefa-item.concluida .tarefa-content {
  text-decoration: line-through;
}

.tarefa-content {
  flex: 1;
}

.tarefa-content h3 {
  color: #333;
  margin-bottom: 5px;
}

.tarefa-content p {
  color: #666;
  font-size: 14px;
}

.tarefa-actions {
  display: flex;
  gap: 10px;
}

.btn-concluir {
  background-color: #4CAF50;
  color: white;
}

.btn-concluir:hover {
  background-color: #45a049;
}

.btn-desfazer {
  background-color: #ff9800;
  color: white;
}

.btn-desfazer:hover {
  background-color: #e68900;
}

.btn-excluir {
  background-color: #f44336;
  color: white;
}

.btn-excluir:hover {
  background-color: #da190b;
}

@media (max-width: 600px) {
  .tarefa-item {
    flex-direction: column;
    align-items: stretch;
  }
  
  .tarefa-actions {
    margin-top: 10px;
    justify-content: center;
  }
}
</style>