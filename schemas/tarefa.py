from pydantic import BaseModel
from typing import Optional, List
from modelos.tarefa import Tarefa

# Define a inserção de tarefas
class TarefaSchema(BaseModel):
    """ Define como uma nova tarefa a ser inserida deve ser representada
    """
    nome: str = "Finalizar o MVP"
    prazo: str = "2023-09-20"

# Define a estrutura da busca de tarefas
class TarefaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do produto.
    """
    nome: str = "Finalizar o MVP"

# Define o retorno da lista de tarefas
class ListagemTarefasSchema(BaseModel):
    """ Define como uma listagem de tarefas será retornada
    """
    tarefas:List[TarefaSchema]

# Define os elementos de retorno de uma tarefa
def apresenta_tarefas(tarefas: List[Tarefa]):
    """ Retorna uma representação da tarefa seguindo o schema 
    definido em TarefaViewSchema
    """
    result = []
    for tarefa in tarefas:
        result.append({
            "nome": tarefa.nome,
            "prazo": tarefa.prazo
        })
    
    return {"tarefas": result}

# Define o retorno de uma tarefa
class TarefaViewSchema(BaseModel):
    """ Define como uma tarefa será retornada
    """
    id: int = 1
    nome: str = "Finalizar o MVP"
    prazo: str = "2023-09-20"  

# Define a remoção de uma tarefa
class TarefaDelSchema(BaseModel):
    """Define como deve ser a estrutura da tarefa após a requisição 
    de remoção
    """
    message: str
    nome: str

# Define a apresentação da tarefa
def apresenta_tarefa(tarefa: Tarefa):
    """ Retorna uma representação da tarefa seguindo o schema definido em
        TarefaViewSchema
    """ 
    return {
        "id": tarefa.id,
        "nome": tarefa.nome,
        "prazo": tarefa.prazo
    }