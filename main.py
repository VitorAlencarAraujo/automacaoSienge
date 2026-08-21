import pymupdf
import re


# Caminho do arquivo PDF
caminho_pdf = "fatura.pdf"


# Abre o PDF
documento = pymupdf.open(caminho_pdf)


# Seleciona a primeira página
pagina = documento[0]


# Extrai o texto da página
texto = pagina.get_text()


# Procura datas no formato DD/MM/AAAA
datas = re.findall(r"\d{2}/\d{2}/\d{4}", texto)


# Procura valores monetários
valores = re.findall(r"R\$\s*[\d.,]+", texto)


# Procura CNPJs
cnpjs = re.findall(r"\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2}", texto)


# Procura sequências de 6 ou mais números
numeros = re.findall(r"\b\d{6,}\b", texto)


# Mostra os resultados
print("\n===== ANÁLISE DO DOCUMENTO =====")

print("\nDatas encontradas:")
for data in datas:
    print("-", data)

print("\nValores encontrados:")
for valor in valores:
    print("-", valor)

print("\nCNPJs encontrados:")
for cnpj in cnpjs:
    print("-", cnpj)

print("\nPossíveis números de documento:")
for numero in numeros:
    print("-", numero)


# Fecha o documento
documento.close()