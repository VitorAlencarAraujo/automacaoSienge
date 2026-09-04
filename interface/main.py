import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
    QTextBrowser
)

from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from leitor_outlook import obter_emails

app = QApplication(sys.argv)

janela = QWidget()

janela.setWindowTitle("Automação Sienge")
janela.resize(1000, 600)


# Layout principal
layout_principal = QVBoxLayout()

janela.setLayout(layout_principal)


# Título
titulo = QLabel("Automação Sienge")

layout_principal.addWidget(titulo)


# Área principal
layout_conteudo = QHBoxLayout()

layout_principal.addLayout(layout_conteudo)


# Lista de e-mails
lista_emails = QListWidget()

emails = obter_emails()

for email in emails:

    texto = (
        f"{email.Subject}\n"
        f"{email.SenderEmailAddress}\n"
        f"{email.ReceivedTime.strftime('%d/%m/%Y %H:%M')}"
    )

    item = QListWidgetItem(texto)

    item.setData(
        Qt.ItemDataRole.UserRole,
        email
    )

    lista_emails.addItem(item)

# Função para interagir com os emails da lista
def selecionar_email(item):

    email = item.data(
        Qt.ItemDataRole.UserRole
    )

    texto = (
        f"Assunto: {email.Subject}\n\n"
        f"Remetente: {email.SenderEmailAddress}\n\n"
        f"Data: {email.ReceivedTime.strftime('%d/%m/%Y %H:%M')}\n\n"
        f"{email.Body}"
    )

    informacao.setText(texto)

    botao_analise.show()


lista_emails.itemClicked.connect(selecionar_email)

layout_conteudo.addWidget(lista_emails, 1)


# Área do e-mail selecionado
layout_email = QVBoxLayout()

layout_conteudo.addLayout(layout_email, 3)


informacao = QTextBrowser()
informacao.setReadOnly(True)

fonte = QFont()
fonte.setPointSize(14)
informacao.setFont(fonte)

layout_email.addWidget(informacao)


botao_analise = QPushButton("Análise IA")
botao_analise.hide()

layout_email.addWidget(botao_analise)


janela.show()

sys.exit(app.exec())