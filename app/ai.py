from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Carrega o modelo de embeddings
model = SentenceTransformer("paraphrase-MiniLM-L6-v2")

def gerar_roteiro_ia(dados_filtrados, requisicao):
    gostos = dados_filtrados["gostos"]
    atracoes = dados_filtrados["dados"]["atracoes"]
    dias = requisicao.dias

    # 1. Gerar vetores dos gostos
    gostos_texto = [g.lower() for g in gostos]
    vetor_gostos = model.encode(gostos_texto, convert_to_tensor=True).mean(dim=0)

    # 2. Gerar vetores das atrações
    atracoes_texto = [
        f"{a['title']} - {a['category']}" for a in atracoes
    ]
    vetores_atracoes = model.encode(atracoes_texto, convert_to_tensor=True)

    # 3. Calcular similaridade entre os gostos e cada atração
    similares = cosine_similarity(
        vetor_gostos.reshape(1, -1), vetores_atracoes.cpu().numpy()
    ).flatten()

    # 4. Combinar com dados das atrações
    atracoes_com_score = [
        {**a, "score": float(similares[i])} for i, a in enumerate(atracoes)
    ]

    # 5. Ordenar por similaridade (maior primeiro)
    atracoes_ordenadas = sorted(atracoes_com_score, key=lambda x: x["score"], reverse=True)

    # 6. Distribuir atrações por dias e períodos
    roteiro = {}
    periodos = ["manha", "tarde", "noite"]
    total_periodos = dias * len(periodos)

    for i in range(total_periodos):
        dia = (i // 3) + 1
        periodo = periodos[i % 3]
        if dia not in roteiro:
            roteiro[dia] = {}
        if i < len(atracoes_ordenadas):
            roteiro[dia][periodo] = atracoes_ordenadas[i]
        else:
            roteiro[dia][periodo] = None

    # 7. Formatar roteiro em formato legível
    resumo_roteiro = []
    for dia in sorted(roteiro.keys()):
        dia_data = {"dia": dia}
        for periodo in periodos:
            atracao = roteiro[dia].get(periodo)
            if atracao:
                descricao = f"Visite {atracao['title']} (categoria: {atracao['category']})"
                dia_data[periodo] = descricao
            else:
                dia_data[periodo] = "Sem sugestão para este período."
        resumo_roteiro.append(dia_data)

    return {
        "dias": dias,
        "resumo": resumo_roteiro
    }
