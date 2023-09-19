# Importa as libs para rodar o Flask e o OpenAI
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

# Importa as libs do SQLAlchemy para o IntegrityError
from sqlalchemy.exc import IntegrityError

# Importa as demais libs para a execução da API 
from modelos import Session, Tarefa
from logger import logger
from schemas import *
from flask_cors import CORS

# Define o nome da API
info = Info(title="Tasker", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Define as tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
tarefa_tag = Tag(name="Tarefa", description="Gerenciamento das tarefas na base")

# Redireciona a home para o OpenAPI
@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

# Retorna a lista de tarefas
@app.get('/tarefas', tags=[tarefa_tag],
        responses={"200": ListagemTarefasSchema, "409": ErrorSchema, "400": ErrorSchema})
def get_tarefas():
    """ Define como uma listagem de tarefas será retornada
    """
    logger.debug(f"Estruturando a lista de tarefas")
    # Conectando com a base
    session = Session()
    # Preparando a lista
    tarefas = session.query(Tarefa).all()

    if not tarefas:
        # Se não há tarefas no banco de dados
        return {"tarefas": []}, 200
    else:
        logger.debug(f"%d tarefas encontradas" % len(tarefas))
        # Representação das tarefas
        print(tarefas)
        return apresenta_tarefas(tarefas), 200

# Adiciona tarefas
@app.post('/adicionar-tarefas', tags=[tarefa_tag],
            responses={"200": TarefaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_tarefa(form: TarefaSchema):
    """Adiciona uma nova tarefa
    """

    tarefa = Tarefa(
        nome=form.nome,
        prazo=form.prazo)
    logger.debug(f"Incluindo a tarefa '{tarefa.nome}'")
    try:
        # Conectando com a base
        session = Session()
        # Adicionando uma nova trefa
        session.add(tarefa)
        # Efetivando o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Incluindo a tarefa '{tarefa.nome}'")
        return apresenta_tarefa(tarefa), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Tarefa duplicada"
        logger.warning(f"Erro ao adicionar a tarea '{tarefa.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # Erros foras do previsto
        error_msg = "Não foi possível incluir a nova tarefa na lista"
        logger.warning(f"Erro ao adicionar a tarefa '{tarefa.nome}', {error_msg}")
        return {"message": error_msg}, 400

# Remove tarefas
@app.delete('/remover-tarefas', tags=[tarefa_tag],
            responses={"200": TarefaDelSchema, "404": ErrorSchema})
def del_tarefa(query: TarefaBuscaSchema): 
    """Remove uma tarefa a partir do nome informado 
    """
    tarefa_nome = unquote(unquote(query.nome))
    print(tarefa_nome)
    logger.debug(f"Removendo a tarefa {tarefa_nome}")
    # Conectando com a base
    session = Session()
    # Removendo
    count = session.query(Tarefa).filter(Tarefa.nome == tarefa_nome).delete()
    session.commit()

    if count:
        # Confirmação da exclusão
        logger.debug(f"'{tarefa_nome} removida com sucesso")
        return {"message": "Tarefa removida", "id": tarefa_nome}
    else:
        # Caso a tarefa não tenha sido encontrada
        error_msg = "Tarefa não encontrada"
        logger.warning(f"Erro ao remover a tarefa {tarefa_nome}, {error_msg}")
        return {"message": error_msg}, 404