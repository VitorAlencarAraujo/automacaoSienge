import win32com.client
import os

from controle_emails import email_ja_processado


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


for mensagem in list(mensagens)[-1:]:

    # Obtém o endereço do remetente
    remetente = mensagem.SenderEmailAddress

    # Verifica se o e-mail é da Babi
    

    # Obtém o identificador único do e-mail
    entry_id = mensagem.EntryID

    # Verifica se já processamos esse e-mail
    if email_ja_processado(entry_id):
        continue

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

    for anexo in mensagem.Attachments:

        print("   -", anexo.FileName)

        # Caminho onde o anexo será salvo
        caminho_anexo = os.path.join(
            pasta_anexos,
            anexo.FileName
        )

        # Salva o anexo
        anexo.SaveAsFile(caminho_anexo)

        print("     Salvo em:", caminho_anexo)

    print()
    print("=" * 50)
    print()