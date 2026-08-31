import win32com.client

outlook = win32com.client.Dispatch("Outlook.Application")

namespace = outlook.GetNamespace("MAPI")

caixa_entrada = namespace.GetDefaultFolder(6)

mensagens = caixa_entrada.Items

print("Caixa de entrada encontrada!")

print("Quantidade de mensagens:", mensagens.Count)

print()
print("===== ÚLTIMOS 5 E-MAILS =====")

for mensagem in list(mensagens)[-5:]:
    # print("ID:", mensagem.EntryID)
    print("Assunto:", mensagem.Subject)
    print("Remetente:", mensagem.SenderName)
    print("Data:", mensagem.ReceivedTime)
    print("Quantidade de objetos de anexo:", mensagem.Attachments.Count)

    print("====CORPO DO E-MAIL ====")
    print(mensagem.Body)
    print()

    for anexo in mensagem.Attachments:
        print("   -", anexo.FileName)
        
    print()

    