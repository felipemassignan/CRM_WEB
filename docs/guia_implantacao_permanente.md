# Guia de Implantação Permanente do CRM Python

Este guia fornece instruções detalhadas para implantar permanentemente o CRM Python em diferentes plataformas de hospedagem sem a necessidade de Docker.

## Opções de Implantação

Existem várias plataformas que oferecem hospedagem gratuita ou de baixo custo para aplicações Flask:

1. **Railway** - Plataforma com plano gratuito generoso
2. **Render** - Oferece tier gratuito para aplicações web
3. **PythonAnywhere** - Especializada em hospedagem Python
4. **Heroku** - Plataforma estabelecida (planos pagos)

## Preparação do Código

Antes de implantar, certifique-se de que o código está preparado para produção:

1. O arquivo `requirements.txt` já está atualizado com todas as dependências
2. A aplicação está configurada para usar variáveis de ambiente
3. O banco de dados está configurado corretamente para produção

## Opção 1: Implantação no Railway

Railway oferece um plano gratuito que inclui 500 horas de execução por mês, ideal para projetos pessoais ou de pequeno porte.

### Passo a Passo:

1. **Crie uma conta no Railway**:
   - Acesse [Railway.app](https://railway.app/)
   - Registre-se usando GitHub ou email

2. **Prepare seu projeto para o Railway**:
   - Certifique-se de que o arquivo `Procfile` está na raiz do projeto com o conteúdo:
     ```
     web: gunicorn src.main:app
     ```

3. **Implante via GitHub**:
   - Faça upload do código para um repositório GitHub
   - No Railway, clique em "New Project" > "Deploy from GitHub repo"
   - Selecione o repositório
   - Railway detectará automaticamente a aplicação Flask

4. **Configure variáveis de ambiente**:
   - No painel do Railway, vá para "Variables"
   - Adicione:
     ```
     FLASK_APP=src.main
     FLASK_ENV=production
     SECRET_KEY=sua_chave_secreta
     ```

5. **Configure o banco de dados**:
   - Para persistência, você pode adicionar um banco PostgreSQL:
     - Clique em "New" > "Database" > "PostgreSQL"
     - Railway fornecerá automaticamente a variável `DATABASE_URL`
   - Atualize o código para usar essa variável:
     ```python
     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///crm.db')
     ```

6. **Acesse sua aplicação**:
   - Railway fornecerá uma URL pública (exemplo: https://seu-projeto.up.railway.app)
   - Essa URL é permanente enquanto o projeto estiver ativo

## Opção 2: Implantação no Render

Render oferece um plano gratuito para aplicações web com algumas limitações, mas suficiente para muitos casos de uso.

### Passo a Passo:

1. **Crie uma conta no Render**:
   - Acesse [Render.com](https://render.com/)
   - Registre-se usando GitHub ou email

2. **Prepare seu projeto para o Render**:
   - Certifique-se de que o arquivo `requirements.txt` está atualizado
   - Crie um arquivo `render.yaml` na raiz do projeto:
     ```yaml
     services:
       - type: web
         name: crm-python
         env: python
         buildCommand: pip install -r requirements.txt
         startCommand: gunicorn src.main:app
         envVars:
           - key: FLASK_APP
             value: src.main
           - key: FLASK_ENV
             value: production
           - key: SECRET_KEY
             value: sua_chave_secreta
     ```

3. **Implante via Dashboard**:
   - No Render, clique em "New" > "Web Service"
   - Conecte ao repositório GitHub ou faça upload direto
   - Configure o nome, ambiente (Python), comando de build e comando de início
   - Clique em "Create Web Service"

4. **Configure o banco de dados**:
   - Para persistência, você pode adicionar um banco PostgreSQL:
     - No Render, vá para "New" > "PostgreSQL"
     - Conecte ao seu serviço web
   - Atualize o código para usar a variável de ambiente:
     ```python
     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///crm.db')
     ```

5. **Acesse sua aplicação**:
   - Render fornecerá uma URL pública (exemplo: https://crm-python.onrender.com)
   - Essa URL é permanente enquanto o serviço estiver ativo

## Opção 3: Implantação no PythonAnywhere

PythonAnywhere é especializado em hospedagem Python e oferece um plano gratuito adequado para projetos pessoais.

### Passo a Passo:

1. **Crie uma conta no PythonAnywhere**:
   - Acesse [PythonAnywhere.com](https://www.pythonanywhere.com/)
   - Registre-se para uma conta gratuita

2. **Faça upload do código**:
   - No dashboard, vá para a seção "Files"
   - Faça upload do arquivo zip do projeto ou clone via Git
   - Extraia os arquivos se necessário

3. **Configure o ambiente virtual**:
   - Abra um console Bash
   - Execute:
     ```bash
     mkvirtualenv --python=python3.11 crm-venv
     cd ~/seu-projeto
     pip install -r requirements.txt
     ```

4. **Configure a aplicação web**:
   - Vá para a seção "Web"
   - Clique em "Add a new web app"
   - Selecione "Manual configuration" e Python 3.11
   - Configure o caminho para o virtualenv: `/home/seuusuario/.virtualenvs/crm-venv`
   - Edite o arquivo WSGI:
     ```python
     import sys
     import os
     
     path = '/home/seuusuario/seu-projeto'
     if path not in sys.path:
         sys.path.append(path)
     
     os.environ['FLASK_APP'] = 'src.main'
     os.environ['FLASK_ENV'] = 'production'
     os.environ['SECRET_KEY'] = 'sua_chave_secreta'
     
     from src.main import app as application
     ```

5. **Configure o banco de dados**:
   - PythonAnywhere permite usar SQLite para planos gratuitos
   - Certifique-se de que o caminho do banco de dados é absoluto:
     ```python
     app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'crm.db')
     ```

6. **Acesse sua aplicação**:
   - PythonAnywhere fornecerá uma URL pública (exemplo: http://seuusuario.pythonanywhere.com)
   - Essa URL é permanente enquanto a conta estiver ativa

## Opção 4: Implantação no Heroku

Heroku é uma plataforma estabelecida que oferece planos pagos, mas com boa relação custo-benefício para aplicações em produção.

### Passo a Passo:

1. **Crie uma conta no Heroku**:
   - Acesse [Heroku.com](https://www.heroku.com/)
   - Registre-se para uma conta

2. **Instale o Heroku CLI**:
   - Baixe e instale o [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
   - Faça login: `heroku login`

3. **Prepare seu projeto para o Heroku**:
   - Certifique-se de que o arquivo `Procfile` está na raiz do projeto:
     ```
     web: gunicorn src.main:app
     ```
   - Certifique-se de que o `requirements.txt` está atualizado

4. **Crie e implante a aplicação**:
   - No diretório do projeto, execute:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     heroku create crm-python-app
     git push heroku main
     ```

5. **Configure variáveis de ambiente**:
   - Execute:
     ```bash
     heroku config:set FLASK_APP=src.main
     heroku config:set FLASK_ENV=production
     heroku config:set SECRET_KEY=sua_chave_secreta
     ```

6. **Configure o banco de dados**:
   - Adicione um banco PostgreSQL:
     ```bash
     heroku addons:create heroku-postgresql:hobby-dev
     ```
   - Heroku configurará automaticamente a variável `DATABASE_URL`
   - Atualize o código para usar essa variável:
     ```python
     app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///crm.db')
     ```

7. **Acesse sua aplicação**:
   - Heroku fornecerá uma URL pública (exemplo: https://crm-python-app.herokuapp.com)
   - Essa URL é permanente enquanto a aplicação estiver ativa

## Considerações Finais

- **Persistência de Dados**: Para aplicações em produção, considere usar um banco de dados PostgreSQL em vez de SQLite
- **Segurança**: Sempre use variáveis de ambiente para senhas e chaves secretas
- **Monitoramento**: Todas as plataformas oferecem algum nível de logs e monitoramento
- **Escalabilidade**: Os planos gratuitos têm limitações de recursos; considere planos pagos para aplicações com mais tráfego

Escolha a plataforma que melhor atende às suas necessidades de custo, facilidade de uso e requisitos técnicos.
