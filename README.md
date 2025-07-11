# Projeto Fullstack de Gerenciamento de Tarefas

Este é um projeto fullstack simples para gerenciar tarefas, desenvolvido com Flask para o backend e Vue.js para o frontend.

## Funcionalidades

- Adicionar novas tarefas
- Listar todas as tarefas
- Marcar tarefas como concluídas/não concluídas
- Excluir tarefas
- Interface responsiva

## Como Rodar o Projeto

1. Backend (Flask)
   ```bash
   cd backend
   source venv/bin/activate
   python src/main.py
   ```
O backend estará rodando em http://localhost:5000

2. Frontend (Vue.js)
   ```bash
   cd frontend
   npm run dev
   ```
O frontend estará rodando em http://localhost:3000

### Testes de Backend (Pytest)

1. Certifique-se de ter o `pytest` instalado no ambiente virtual do backend:
   ```bash
   cd backend
   source venv/bin/activate
   pip install pytest
   cd ..
   ```

2. Execute os testes a partir da raiz do projeto:
   ```bash
   cd backend
   source venv/bin/activate
   python -m pytest tests/
   cd ..
   ```

### Testes de Frontend (Vitest)

1. Certifique-se de ter o `vitest` e as dependências instaladas no frontend:
   ```bash
   cd frontend
   npm install -D vitest @vue/test-utils @vitest/ui jsdom
   cd ..
   ```

2. Execute os testes a partir da raiz do projeto:
   ```bash
   cd frontend
   npm test
   cd ..
   ```

## API Endpoints

GET / - Mensagem de boas-vindas
GET /tarefas - Lista todas as tarefas
POST /tarefas - Cria uma nova tarefa
PUT /tarefas/<id> - Atualiza uma tarefa existente
DELETE /tarefas/<id> - Exclui uma tarefa

## Como Rodar o Projeto com Docker

1.  Navegue até a raiz do projeto (`projeto-fullstack`):
    ```bash
    cd projeto-fullstack
    ```

2.  Construa as imagens Docker:
    ```bash
    docker compose build
    ```

3.  Inicie os contêineres:
    ```bash
    docker compose up -d
    ```

4.  Acesse o frontend em seu navegador: `http://localhost:8080`

5.  Para parar e remover os contêineres:
    ```bash
    docker compose down
    ```

## Integração Contínua (CI/CD) com GitHub Actions

Este projeto utiliza GitHub Actions para automatizar o processo de CI/CD. Em cada `push` ou `pull_request` para a branch `master`, o workflow irá:

1.  Executar os testes de backend (Pytest).
2.  Executar os testes de frontend (Vitest).
3.  Construir e enviar as imagens Docker do backend e frontend para o Docker Hub.

## Orquestração com Kubernetes (Kind)

Este projeto pode ser implantado em um cluster Kubernetes local usando Kind (Kubernetes in Docker).

### Pré-requisitos

*   [Docker](https://docs.docker.com/)
*   [Kind](https://kind.sigs.k8s.io/docs/user/quick-start/)
*   [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl/)

### Passos para Implantação Local

1.  **Crie o cluster Kind:**
    ```bash
    kind create cluster --config kind-config.yaml --name fullstack-cluster
    ```

2.  **Carregue as imagens Docker no Kind (opcional, mas recomendado para desenvolvimento):**
    ```bash
    kind load docker-image YOUR_DOCKERHUB_USERNAME/fullstack-backend:latest --name fullstack-cluster
    kind load docker-image YOUR_DOCKERHUB_USERNAME/fullstack-frontend:latest --name fullstack-cluster
    ```
    (Substitua `YOUR_DOCKERHUB_USERNAME` pelo seu usuário do Docker Hub)

3.  **Aplique os manifests Kubernetes:**
    ```bash
    kubectl apply -f k8s/backend.yaml
    kubectl apply -f k8s/frontend.yaml
    ```

4.  **Acesse a aplicação:**
    *   Para acesso do frontend: `kubectl port-forward service/fullstack-frontend-service 8080:80` e acesse `http://localhost:8080`.
    *   Para acesso do backend: `kubectl port-forward service/fullstack-backend-service 5000:5000` e acesse `http://localhost:5000`.

5.  **Para remover o cluster:**
    ```bash
    kind delete cluster --name fullstack-cluster

## Entrega Contínua (CD) com ArgoCD

Este projeto utiliza o ArgoCD para realizar a entrega contínua (CD) das aplicações frontend e backend em um cluster Kubernetes local criado com o Kind.

### Pré-requisitos

*   Cluster Kubernetes local (Kind)
*   GitHub Actions configurado com: Secrets: DOCKERHUB_USERNAME, DOCKERHUB_TOKEN
*   Repositórios criados no Docker Hub: fullstack-backend, fullstack-frontend

### Etapas de Configuração

Instalação do ArgoCD no cluster
```bash
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```
Acessar o ArgoCD via navegador
```bash
kubectl port-forward svc/argocd-server -n argocd --address 0.0.0.0 8080:443
```
Acesse: `https://localhost:8080`
Usuário: `admin`

Para obter a senha:
```bash
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d; echo
```
### Criação do App no ArgoCD

*   **Application Name**: `fullstack-app`
*   **Repository URL**: seu repositório no GitHub
*   **Revision**: `HEAD`
*   **Path**: `k8s`
*   **Namespace**: `default`
*   **Sync Policy**: Manual ou Automática

### Manifests Kubernetes com Kustomize

Todos os arquivos de Deployment, Service e `kustomization.yaml` estão na pasta `k8s/`, com as imagens configuradas para serem atualizadas automaticamente com base no SHA do commit.

### CI/CD com GitHub Actions

O workflow do GitHub Actions:

1.  Roda os testes
2.  Constrói e envia as imagens Docker para o Docker Hub com a tag `latest` e `${{ github.sha }}`
3.  Atualiza o `kustomization.yaml` com a nova imagem
4.  Faz commit e push da alteração

### Acessar a aplicação implantada

Execute os seguintes comandos para acessar a aplicação:

```bash
kubectl port-forward svc/fullstack-frontend-service 8080:80
kubectl port-forward svc/fullstack-backend-service 5000:5000
```

## Tecnologias Utilizadas

Backend

Flask 2.3.2
Flask-CORS 3.0.10

Frontend

Vue.js 3.3.4
Axios 1.4.0
Vite 4.4.5
