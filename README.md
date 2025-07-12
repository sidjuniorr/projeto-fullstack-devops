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

* GET / - Mensagem de boas-vindas
* GET /tarefas - Lista todas as tarefas
* POST /tarefas - Cria uma nova tarefa
* PUT /tarefas/<id> - Atualiza uma tarefa existente
* DELETE /tarefas/<id> - Exclui uma tarefa

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

## Provisionamento de Infraestrutura com Terraform

Este projeto também conta com o provisionamento automatizado da infraestrutura local usando Terraform.

### O que é provisionado

*   Execução local do cluster Kubernetes via Kind
*   Comando para criação do cluster com base no arquivo `kind-config.yaml`
*   Lógica condicional para evitar recriação do cluster se ele já existir

### Como utilizar

Acesse a pasta `infra/`:

```bash
cd infra
```

Inicialize o Terraform:

```bash
terraform init
```

Aplique o provisionamento:
```bash
terraform apply
```

⚠️ O script de criação do cluster verifica automaticamente se o cluster fullstack-cluster já existe antes de executar. Isso evita erros ou tentativas de recriação.

## Integração com PostgreSQL

Este projeto foi atualizado para utilizar PostgreSQL como banco de dados persistente, substituindo a abordagem anterior de dados em memória. Esta integração garante maior robustez, persistência de dados e escalabilidade para a aplicação.

### Alterações no Backend

O backend Flask (`backend/src/main.py`) foi modificado para interagir com o PostgreSQL utilizando o driver `psycopg2`. As operações CRUD (Criar, Ler, Atualizar, Deletar) agora persistem os dados no banco de dados. A configuração de conexão é gerenciada através de variáveis de ambiente (`DATABASE_URL`).

As dependências do backend foram atualizadas para incluir `psycopg2-binary`.

### Configuração com Docker Compose

O arquivo `docker-compose.yml` foi estendido para incluir um serviço PostgreSQL. Isso permite que você execute a aplicação completa (backend, frontend e banco de dados) localmente com um único comando.

Para iniciar a aplicação com PostgreSQL via Docker Compose:

```bash
docker compose up --build -d
```
O serviço `backend` agora depende do serviço `postgres`, garantindo que o banco de dados esteja pronto antes que o backend tente se conectar.

### Implantação no Kubernetes (Kind)

Os manifestos Kubernetes na pasta `k8s/` foram atualizados para incluir o Deployment e Service do PostgreSQL, além de um Persistent Volume Claim (PVC) para garantir a persistência dos dados do banco. Um `initContainer` foi adicionado ao Deployment do backend para garantir que ele aguarde o PostgreSQL estar disponível antes de iniciar.

Para aplicar os manifests atualizados no seu cluster Kind:

```bash
kubectl apply -f k8s/postgres-simple.yaml
# Certifique-se de que seu kustomization.yaml foi atualizado para incluir postgres-simple.yaml
kubectl apply -k k8s/
```

### Integração com ArgoCD

O ArgoCD reconhecerá automaticamente as novas configurações do PostgreSQL através do `kustomization.yaml` atualizado. Certifique-se de que seu `kustomization.yaml` inclua o `postgres-simple.yaml` na seção `resources`.

O Application do ArgoCD continuará monitorando o repositório Git e aplicará as mudanças no cluster, garantindo que o PostgreSQL seja implantado e gerenciado como parte da sua aplicação fullstack.

### Testes de Backend

Os testes de backend (`backend/tests/test_api.py`) foram atualizados para utilizar mocking das operações de banco de dados. Isso garante que os testes unitários sejam rápidos e isolados, sem a necessidade de um servidor PostgreSQL real durante a execução dos testes. As funções de conexão e inicialização do banco de dados são simuladas para testar a lógica da aplicação de forma eficiente.

Para executar os testes de backend:

```bash
cd backend
source venv/bin/activate
python3 -m pytest tests/
```

## Tecnologias Utilizadas

Backend

* Flask 2.3.2
* Flask-CORS 3.0.10
* Python 3.11
* Docker 24.0.5
* pytest 7.4.2
* PostgreSQL 16
* psycopg2-binary

Frontend

* Vue.js 3.3.4
* Axios 1.4.0
* Vite 4.4.9
* Node.js 20.5.1
* Docker 24.0.5
* Vitest 0.31.2

Infraestrutura

* Docker Compose 2.21.1 (gerencia múltiplos containers)
* Terraform 1.6.7 (infra como código, arquivos .tf)
* Kubernetes 1.29.3 (arquivos YAML para deploy: deployments, services, kustomization)
* Kind 0.21.0 (Kubernetes in Docker, arquivo kind-config.yaml)
