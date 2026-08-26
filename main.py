import pymupdf
import re


# Caminho do arquivo PDF
caminho_pdf = "titulo_4045989_demonstrativo.pdf"


# Abre o PDF
documento = pymupdf.open(caminho_pdf)


# Seleciona a primeira página
pagina = documento[0]


# Extrai o texto da página
texto = pagina.get_text()

linhas = texto.splitlines()

for indice, linha in enumerate(linhas):
    print(indice, "->", linha)


# -------------------------------
# IDENTIFICAR DATA DE EMISSÃO
# -------------------------------

padrao_emissao = r"EMISSÃO:\s*(\d{2}/\d{2}/\d{4})"

resultado_emissao = re.search(padrao_emissao, texto)

if resultado_emissao:
    data_emissao = resultado_emissao.group(1)


# -------------------------------
# IDENTIFICAR VENCIMENTO
# -------------------------------

padrao_vencimento = r"VENCIMENTO:\s*(\d{2}/\d{2}/\d{4})"

resultado_vencimento = re.search(padrao_vencimento, texto)

if resultado_vencimento:
    data_vencimento = resultado_vencimento.group(1)


# -------------------------------
# IDENTIFICAR VALOR DA FATURA
# -------------------------------

padrao_valor = r"VALOR DA FATURA:\s*([\d.,]+)"

resultado_valor = re.search(padrao_valor, texto)

if resultado_valor:
    valor_fatura = resultado_valor.group(1)


# -------------------------------
# MOSTRAR RESULTADO
# -------------------------------

print("\n===== DADOS IDENTIFICADOS =====")

if resultado_emissao:
    print("Emissão:", data_emissao)

if resultado_vencimento:
    print("Vencimento:", data_vencimento)

if resultado_valor:
    print("Valor da fatura:", valor_fatura)


# Fecha o documento
documento.close()