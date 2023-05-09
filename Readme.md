# Projeto base para demais microsserviços
- Este projeto deve ser usado somente para base de desenvolvimento do microsserviço nele já contém:
    -  routes(Rotas do serviço):
        - TestRoute:
            - Rota de teste para verificar se está de pé e rodando o serviço
        - Example:
            - Rota que não é possivel chamar de forra pois ela executa quando é estartado a aplicação.
    - domains:
        - interfaces
            - Database:
                - Interface de comunicação com a camada de adapters.
            - Example:
                - Interface de comunicação entre o routes e o use case.
            - Queue:
                - Interface de comunicação com a camada de adapters.
            - Cache:
                - Interface de comunicação com a camada de adapters.
            - Cloud_Provider:
                - Interface de comunicação com a camada de adapters.
        - entities(Entidade para o banco de dados):
            - User:
                - Entidade de usuário criada somente para se comunicar com o banco de dados.
        - usecases(Caso de uso):
            - Example:
                - Caso de uso que deve ser utilizado como exemplo, ele já conecta no rabbit na fila "messages" e no processamento das mensagens, ele concta no Banco de Dados e pega todos os usuarios da tabela user, também conecta com o GCP pegando o conteudo de um bucket e também conecta ao Redis setando e pegando mensagens.
        - actions(Ações da aplicação que irão chamar as interfaces):
            - Database
                - Action com os métodos de comunicação da interface para realizar o bind com a camada de adapters.
            - Example
                - Action com os métodos de comunicação entre o routes e o use case.
            - Queue
                - Action com os métodos de comunicação da interface para realizar o bind com a camada de adapters.
            - Cache:
                - Action com os métodos de comunicação da interface para realizar o bind com a camada de adapters.
            - Cloud_Provider:
                - Action com os métodos de comunicação da interface para realizar o bind com a camada de adapters.
    - adapters(Camada de adaptadores):
        - Database:
            - Adaptador para se conectar com o banco de dados que neste caso é um banco de dados(SQLite) fake presente na raiz do projeto(sample.db).
        - queue:
            - Adaptador para se conectar com o provider de fila neste caso é o Rabbit.
        - Cache:
            - Adaptador para se conectar com o provider de cache neste caso é o Redis.
        - Cloud_Provider:
            - Adaptador para se conectar com o provider de nuvem neste caso é o GCP com o método de Bucket.

# Requerimentos:
- Para poder iniciar é preciso ter instalado as dependências abaixo:
    - [Python](https://www.python.org/)
    - [Pip](https://pip.pypa.io/)
    - [Poetry](https://poetry.eustace.io/)
    - [Git](https://git-scm.com/)
    - [poethepoet](https://github.com/nat-n/poethepoet)

# Instruções de clonagem e execução do projeto:
- Clonar o repositório:
####
    git clone .....
- Para executar o projeto é preciso estar dentro da pasta do projeto e rodar o comando abaixo para definir que queremos criar o ambiente virtual dentro da pasta do projeto:
######
    poetry config virtualenvs.in-project true
- Após isso pode ser executado a criação e ativação do ambiente virtual:
######
    poetry shell
- Após pode ser executado o comando abaixo para instalar as dependências do projeto(O poetry fará todo o trabalho para nós):
######
    poetry install
- Precisa ser definido também uma variavel global para que o Flask consiga encontrar quem inicia o projeto:
    - Windows: ```set FLASK_APP=src\main.py```
    - Mac/Linux: ```export FLASK_APP=main.py```
- Após isso pode ser executado o comando abaixo para executar o projeto:
######
    poe start
ou
#####
    flask run --port 8080

# Instruções para conteinizar o projeto:
## Buildar o container
### Buildar para produção:
    docker build --build-arg YOUR_ENV=production -t poetry:v2 . 
### Buildar para DEV:
    docker build --build-arg YOUR_ENV=dev -t poetry:v2 .
## Rodar em produção o container
    docker run -e YOUR_ENV=production -p 8080:8080 poetry:v2
## Rodar em desenvolvimento o container
    docker run -e YOUR_ENV=dev -p 8080:8080 poetry:v2
## Renomear e subir imagem:
### Renomear a imagem:
    docker tag poetry:v2 gcr.io/ped/example:v1
### Subir a imagem:
    docker push gcr.io/ped/example:v1


