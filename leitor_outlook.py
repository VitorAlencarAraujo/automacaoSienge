import win32com.client


def obter_emails():

    outlook = win32com.client.Dispatch("Outlook.Application")

    namespace = outlook.GetNamespace("MAPI")

    caixa_entrada = namespace.GetDefaultFolder(6)

    mensagens = caixa_entrada.Items

    mensagens.Sort("[ReceivedTime]", True)

    return mensagens


