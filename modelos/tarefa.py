# Importa os pacotes necessários para criar a tabela "tarefa"

from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  modelos import Base


class Tarefa(Base):
    __tablename__ = 'tarefas'

    id = Column("pk_tarefas", Integer, primary_key=True)
    nome = Column(String(300), unique=True)
    prazo = Column(String(100))
    adicao = Column(DateTime, default=datetime.now())

    def __init__(self, nome:str, prazo:str, adicao:Union[DateTime, 
                                                    None] = None):
        """
        Cria uma nova tarefa na lista

        Arguments:
            nome: descrição da tarefa.
            prazo: prazo de conclusão da tarefa
            adicao: data de quando a tarefa foi inserida à base
        """
        self.nome = nome
        self.prazo = prazo
        self.adicao = adicao

        # Se não for informada, será o data exata da inserção no banco
        if adicao:
            self.adicao = adicao
