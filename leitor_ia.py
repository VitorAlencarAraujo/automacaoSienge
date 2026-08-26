from google import genai
from pydantic import BaseModel


class DadosFatura(BaseModel):
    fornecedor: str | None
    cnpj_fornecedor: str | None
    empresa_pagadora: str | None
    cnpj_empresa_pagadora: str | None
    numero_documento: str | None
    data_emissao: str | None
    data_vencimento: str | None
    valor_bruto: float | None

def validar_cnpj(cnpj):

    if not cnpj:
        return False

    numeros = ''.join(filter(str.isdigit, cnpj))

    if len(numeros) != 14:
        return False

    return True

def validar_fatura(dados):

    erros = []

    if not dados.fornecedor:
        erros.append("Fornecedor não identificado.")

    if not dados.cnpj_fornecedor:
        erros.append("CNPJ do fornecedor não identificado.")
    elif not validar_cnpj(dados.cnpj_fornecedor):
        erros.append("CNPJ do fornecedor possui formato inválido.")

    if not dados.empresa_pagadora:
        erros.append("Empresa pagadora não identificada.")

    if not dados.cnpj_empresa_pagadora:
        erros.append("CNPJ da empresa pagadora não identificado.")
    elif not validar_cnpj(dados.cnpj_empresa_pagadora):
        erros.append("CNPJ da empresa pagadora possui formato inválido.")

    if not dados.numero_documento:
        erros.append("Número do documento não identificado.")

    if not dados.data_emissao:
        erros.append("Data de emissão não identificada.")

    if not dados.data_vencimento:
        erros.append("Data de vencimento não identificada.")

    if dados.valor_bruto is None:
        erros.append("Valor bruto não identificado.")
    elif dados.valor_bruto <= 0:
        erros.append("Valor bruto deve ser maior que zero.")

    return erros

cliente = genai.Client()


arquivo = cliente.files.upload(
    file="titulo_4045989_demonstrativo.pdf"
)


instrucao = """
Analise cuidadosamente este documento.

Identifique as seguintes informações:

- fornecedor
- CNPJ do fornecedor
- empresa pagadora
- CNPJ da empresa pagadora
- número do documento
- data de emissão
- data de vencimento
- valor bruto

Não invente informações.

Se uma informação não estiver claramente presente
no documento, retorne null para esse campo.

Preste atenção à relação entre os rótulos e seus respectivos valores.
Considere a estrutura visual do documento para identificar
corretamente cada informação.
"""


resposta = cliente.models.generate_content(
    model="gemini-3.6-flash",
    contents=[
        arquivo,
        instrucao
    ],
    config={
        "response_mime_type": "application/json",
        "response_schema": DadosFatura,
    }
)


dados = resposta.parsed

print("===== DADOS DA FATURA =====")

print("Fornecedor:", dados.fornecedor)
print("CNPJ fornecedor:", dados.cnpj_fornecedor)
print("Empresa pagadora:", dados.empresa_pagadora)
print("CNPJ empresa pagadora:", dados.cnpj_empresa_pagadora)
print("Número do documento:", dados.numero_documento)
print("Data de emissão:", dados.data_emissao)
print("Data de vencimento:", dados.data_vencimento)
print("Valor bruto:", dados.valor_bruto)

erros = validar_fatura(dados)


if len(erros) == 0:

    print()
    print("===== VALIDAÇÃO =====")
    print("✅ Documento aprovado nas validações básicas.")

else:

    print()
    print("===== VALIDAÇÃO =====")
    print("⚠️ Documento precisa de conferência.")
    print()

    for erro in erros:
        print("❌", erro)