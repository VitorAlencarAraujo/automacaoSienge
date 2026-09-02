from google import genai
from pydantic import BaseModel

cliente = genai.Client()

class DocumentoAnexo(BaseModel):
    nome_arquivo: str
    relevante: bool
    tipo_documento: str | None
    motivo: str


class AnaliseEmail(BaseModel):
    eh_lancamento: bool
    motivo: str

    instrucoes_lancamento: list[str]

    documentos_relevantes: list[DocumentoAnexo]
    documentos_ignorados: list[DocumentoAnexo]


def analisar_email(corpo_email, anexos):

    conteudo = []

    conteudo.append(
        "CORPO DO E-MAIL:\n"
        + corpo_email
    )

    conteudo.append(
        "\n\nARQUIVOS ANEXADOS:"
    )

    arquivos_enviados = []

    for caminho in anexos:

        arquivo = cliente.files.upload(
            file=caminho
        )

        arquivos_enviados.append(arquivo)

        conteudo.append(
            f"\nArquivo: {caminho}"
        )

    instrucao = """
Analise cuidadosamente o e-mail e todos os arquivos anexados.

Seu objetivo é identificar se este e-mail corresponde a uma
solicitação de lançamento de uma conta a pagar.

Analise o conteúdo visual e textual dos arquivos.

IMPORTANTE:
- Não considere um arquivo irrelevante apenas porque ele é uma imagem.
- Uma imagem pode ser um documento importante.
- Identifique quais arquivos realmente possuem informações
  relacionadas ao lançamento.
- Imagens decorativas, logotipos, assinaturas e elementos
  sem informações relevantes devem ser classificados como
  irrelevantes.
- Não invente informações.
- Se não houver informações suficientes, indique isso no motivo.

Também identifique no corpo do e-mail quaisquer instruções
importantes para o lançamento.

Retorne:
- se o e-mail é ou não uma solicitação de lançamento;
- o motivo dessa decisão;
- as instruções de lançamento encontradas;
- quais anexos são relevantes;
- quais anexos são irrelevantes;
- o tipo de cada documento relevante ou ignorado;
- o motivo da classificação de cada arquivo.
"""

    resposta = cliente.models.generate_content(
        model="gemini-3.5-flash-lite",

        contents=[
            *arquivos_enviados,
            "\n".join(conteudo),
            instrucao
        ],

        config={
            "response_mime_type": "application/json",
            "response_schema": AnaliseEmail,
        }
    )

    return resposta.parsed