Projeto Content - README

Este é o README do projeto Content, uma aplicação Django que gerencia clientes, empresas, mídias, boletins informativos, notificações e outras funcionalidades relacionadas. O projeto também inclui um componente de rastreador da web e utiliza o Celery para tarefas em segundo plano.

## Configurando o projeto localmente

### Pré-requisitos
- Docker
- Python (preferencialmente 3.8 ou superior)
- Pip
- Virtualenv (opcional, mas recomendado)

### Configuração Inicial do PostgreSQL
1. Execute o contêiner do PostgreSQL com o seguinte comando:

docker run --name nxt-web -e POSTGRES_DB=nxt -e POSTGRES_USER=nxt -e POSTGRES_PASSWORD=nxt -v ./nxt.backup:/app/nxt.backup -p 5432:5432 -d postgres:14

2. Acesse o CLI dentro do contêiner:

docker exec -it nxt-web /bin/sh

3. Restaure o backup:

pg_restore --host=localhost --dbname=nxt ./nxt.backup --no-owner --verbose

4. Saia do contêiner.

### Executando o servidor Django
1. Ative seu ambiente virtual:

source venv/bin/activate

2. Instale as dependências necessárias:

pip install -r requirements.txt

3. Execute o servidor Django:

python manage.py runserver

**Nota:** Se não for a primeira vez que você executa o projeto, simplesmente inicie o contêiner nxt-web no Docker normalmente.

### Executando o Rastreador
1. Carregue o diário oficial para uma data específica:

python manage.py load_gazette ../nxtcrawler/data --date=AAAA-MM-DD

*Nota: Substitua AAAA-MM-DD pela data desejada que você deseja inserir.*

2. Execute o rastreador:

python manage.py runner.py

3. Carregue os dados do diário oficial para uma data específica:

python manage.py load_gazette data --date=AAAA-MM-DD

*Nota: Substitua AAAA-MM-DD pela data desejada que você deseja inserir.*

Agora você deve ter o projeto Content rodando localmente e pode interagir com ele usando seu navegador da web ou cliente de API.
