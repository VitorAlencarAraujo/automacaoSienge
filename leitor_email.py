import win32com.client
import os
import json

from controle_emails import email_ja_processado
from analisador_email import analisar_email
from leitor_ia import analisar_documento

# Conecta ao Outlook
outlook = win32com.client.Dispatch("Outlook.Application")

# Acessa o MAPI do Outlook
namespace = outlook.GetNamespace("MAPI")

# Acessa a Caixa de Entrada
caixa_entrada = namespace.GetDefaultFolder(6)

# Obtém os e-mails
mensagens = caixa_entrada.Items

# Pasta onde os anexos serão salvos
pasta_projeto = os.path.dirname(os.path.abspath(__file__))

pasta_anexos = os.path.join(
    pasta_projeto,
    "anexos"
)
os.makedirs(pasta_anexos, exist_ok=True)


print("===== LEITOR DE E-MAIL =====")
print()


for mensagem in mensagens:

    # Obtém o endereço do remetente
    remetente = mensagem.SenderEmailAddress

    # Verifica se o e-mail é da Babi
    if mensagem.Subject != "ENC: FATURA CLARO PARA PAGTO EM 05/09/26":
        continue

    # Obtém o identificador único do e-mail
    entry_id = mensagem.EntryID

    # Verifica se já processamos esse e-mail
    if email_ja_processado(entry_id):
        continue

    pasta_anexos_email = os.path.join(
    pasta_anexos,
    entry_id
)
    os.makedirs(pasta_anexos_email, exist_ok=True)

    print("===== NOVO E-MAIL ENCONTRADO =====")

    print("Assunto:", mensagem.Subject)
    print("Remetente:", remetente)
    print("Data:", mensagem.ReceivedTime)
    print("EntryID:", entry_id)

    print()

    print("===== CORPO DO E-MAIL =====")
    print(mensagem.Body)
    print()

    print("===== ANEXOS =====")

    print("Quantidade de objetos de anexo:", mensagem.Attachments.Count)

    anexos_salvos = []

    for anexo in mensagem.Attachments:

        nome_arquivo = anexo.FileName

        caminho_anexo = os.path.join(
            pasta_anexos_email,
            nome_arquivo
        )
       

        anexo.SaveAsFile(caminho_anexo)

        anexos_salvos.append(caminho_anexo)

        print("     Salvo em:", caminho_anexo)

        print()
        print("=" * 50)
        print()

    print("===== ENVIANDO E-MAIL PARA A IA =====")

    resultado = analisar_email(
        mensagem.Body,
        anexos_salvos
    )

    print()
    print("===== REMOVENDO ARQUIVOS IRRELEVANTES =====")

    for documento in resultado.documentos_ignorados:

        for caminho_arquivo in anexos_salvos:

            nome_arquivo = os.path.basename(caminho_arquivo)

            if nome_arquivo == documento.nome_arquivo:

                if os.path.exists(caminho_arquivo):

                    os.remove(caminho_arquivo)

                    print("Removido:", nome_arquivo)

                break

    print()
    print("===== ANÁLISE DA IA =====")

    print("É lançamento:", resultado.eh_lancamento)
    print("Motivo:", resultado.motivo)

    print()
    print("Instruções:")

    for instrucao in resultado.instrucoes_lancamento:
        print("-", instrucao)

    print()
    print("Documentos relevantes:")

    for documento in resultado.documentos_relevantes:
        print("-", documento.nome_arquivo)
        print("  Tipo:", documento.tipo_documento)
        print("  Motivo:", documento.motivo)

    print()

    print("===== ANALISANDO DOCUMENTOS RELEVANTES =====")

    documentos = []

    for documento in resultado.documentos_relevantes:

        for caminho_arquivo in anexos_salvos:

            nome_arquivo = os.path.basename(caminho_arquivo)

            if nome_arquivo == documento.nome_arquivo:

                print()
                print("Analisando:", nome_arquivo)

                dados, erros = analisar_documento(caminho_arquivo)

                print("Fornecedor:", dados.fornecedor)
                print("CNPJ fornecedor:", dados.cnpj_fornecedor)
                print("Empresa pagadora:", dados.empresa_pagadora)
                print("CNPJ empresa pagadora:", dados.cnpj_empresa_pagadora)
                print("Número do documento:", dados.numero_documento)
                print("Data de emissão:", dados.data_emissao)
                print("Data de vencimento:", dados.data_vencimento)
                print("Valor bruto:", dados.valor_bruto)

                print()

                if len(erros) == 0:
                    print("✅ Documento aprovado nas validações.")
                else:
                    print("⚠️ Documento precisa de conferência.")

                    for erro in erros:
                        print("❌", erro)
                    

                documentos.append({
                    "nome_arquivo": documento.nome_arquivo,
                    "caminho_arquivo": os.path.relpath(caminho_arquivo, pasta_projeto),
                    "relevante": True,
                    "tipo_documento": documento.tipo_documento,
                    "motivo": documento.motivo,
                    "dados": dados.model_dump(),
                    "erros": erros
                })

                break    

    for documento in resultado.documentos_ignorados:

        documentos.append({
        "nome_arquivo": documento.nome_arquivo,
        "relevante": False,
        "tipo_documento": documento.tipo_documento,
        "motivo": documento.motivo
    })

    pasta_analises = os.path.join(
    pasta_projeto,
    "analises"
    )

    os.makedirs(pasta_analises, exist_ok=True)

    caminho_json = os.path.join(
        pasta_analises,
        f"{entry_id}.json"
    )

    analise_completa = {
    "email": {
        "assunto": mensagem.Subject,
        "remetente": remetente,
        "data": str(mensagem.ReceivedTime),
        "entry_id": entry_id
    },

    "analise": {
        "eh_lancamento": resultado.eh_lancamento,
        "motivo": resultado.motivo,
        "instrucoes_lancamento": resultado.instrucoes_lancamento
    },

    "documentos": documentos
    }

    with open(caminho_json, "w", encoding="utf-8") as arquivo:

        json.dump(
            analise_completa,
            arquivo,
            ensure_ascii=False,
            indent=4
    )               

    print()
    print("Documentos ignorados:")

    for documento in resultado.documentos_ignorados:
        print("-", documento.nome_arquivo)
        print("  Tipo:", documento.tipo_documento)
        print("  Motivo:", documento.motivo)