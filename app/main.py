from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from app.filter import filtrar_dados
from app.ai import gerar_roteiro_ia


app = FastAPI()

class Gosto(BaseModel):
    id: str
    name: str

class RequisicaoRoteiro(BaseModel):
    dias: int
    gostos: List[Gosto]
    dataHoje: str
    periodoChegada: str

@app.post("/api/gerar-roteiro")
def gerar_roteiro(requisicao: RequisicaoRoteiro):
    dados_filtrados = filtrar_dados(requisicao)
    roteiro_final = gerar_roteiro_ia(dados_filtrados, requisicao)
    return {"roteiro": roteiro_final}


