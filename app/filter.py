import json
from pathlib import Path

# Caminhos dos arquivos
BASE_DIR = Path(__file__).resolve().parent.parent
CAMINHO_DB_ORIGINAL = BASE_DIR / "data" / "dbmock.json"
CAMINHO_DB_FILTRADO = BASE_DIR / "data" / "dbMockFiltered.json"

def filtrar_dados(requisicao):
    gostos_usuario = [g.name.lower() for g in requisicao.gostos]

    # Carrega o banco de dados original
    with open(CAMINHO_DB_ORIGINAL, "r", encoding="utf-8") as f:
        db = json.load(f)

    atracoes_filtradas = []
    trilhas_filtradas = []
    eventos_filtrados = []

    # Filtra atrações
    for atracao in db.get("atracoes", []):
        categoria = atracao["category"]["name"].lower()
        titulo = atracao["title"].lower()
        if categoria in gostos_usuario or titulo in gostos_usuario:
            atracoes_filtradas.append({
                "type": "atracaoLocal",
                "title": atracao["title"],
                "category": atracao["category"]["name"],
                "neighborhood": atracao.get("neighborhood", {}).get("name", "")
            })

    # Filtra trilhas
    for trilha in db.get("trilhas", []):
        categoria = trilha["category"]["name"].lower()
        titulo = trilha["title"].lower()
        if categoria in gostos_usuario or titulo in gostos_usuario:
            trilhas_filtradas.append({
                "type": "trilha",
                "title": trilha["title"],
                "category": trilha["category"]["name"]
            })

    # Filtra eventos
    for evento in db.get("eventos", []):
        categoria = evento["category"]["name"].lower()
        titulo = evento["title"].lower()
        if categoria in gostos_usuario or titulo in gostos_usuario:
            eventos_filtrados.append({
                "type": "evento",
                "title": evento["title"],
                "category": evento["category"]["name"],
                "neighborhood": evento.get("neighborhood", {}).get("name", ""),
                "dates": evento.get("dates", [])
            })

    # Constrói resultado final
    resultado = {
        "dias": requisicao.dias,
        "gostos": gostos_usuario,
        "dataHoje": requisicao.dataHoje,
        "periodoChegada": requisicao.periodoChegada,
        "dados": {
            "atracoes": atracoes_filtradas + trilhas_filtradas + eventos_filtrados
        }
    }

    # (Opcional) Salva o resultado em dbMockFiltered.json
    with open(CAMINHO_DB_FILTRADO, "w", encoding="utf-8") as f_out:
        json.dump(resultado, f_out, ensure_ascii=False, indent=2)

    return resultado
