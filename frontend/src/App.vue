<template>
    <div id="app">
      <h1>Gerenciador de Tarefas</h1>
      <p>{{ message }}</p>
      <button @click="testConnection">Testar Conexão com Backend</button>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  
  export default {
    name: 'App',
    data() {
      return {
        message: 'Frontend Vue.js funcionando!'
      }
    },
    methods: {
      async testConnection() {
        try {
          const response = await axios.get('http://localhost:5000/')
          this.message = response.data.message
        } catch (error) {
          this.message = 'Erro ao conectar com o backend'
          console.error(error)
        }
      }
    }
  }
  </script>
  
  <style>
  #app {
    font-family: Arial, sans-serif;
    text-align: center;
    margin-top: 60px;
  }
  
  button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin-top: 20px;
  }
  
  button:hover {
    background-color: #45a049;
  }
  </style>