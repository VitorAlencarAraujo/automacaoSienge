import json
import os


ARQUIVO_CONTROLE = "processados.json"


def carregar_processados():

    if not os.path.exists(ARQUIVO_CONTROLE):
        return {"emails": {}}

    with open(ARQUIVO_CONTROLE, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)


def email_ja_processado(entry_id):

    dados = carregar_processados()

    return entry_id in dados["emails"]


def marcar_como_processado(entry_id):

    dados = carregar_processados()

    dados["emails"][entry_id] = {
        "status": "processado"
    }

    with open(ARQUIVO_CONTROLE, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
        