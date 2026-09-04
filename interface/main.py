import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QPushButton,
)


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

lista_emails.addItem("ENC: FATURA CLARO PARA PAGTO EM 05/09/26")
lista_emails.addItem("DIGITALIZAÇÃO")
lista_emails.addItem("Tarefa")

# Função para interagir com os emails da lista
def selecionar_email(item):

    informacao.setText(
        f"E-mail selecionado:\n\n{item.text()}"
    )

    botao_analise.show()


lista_emails.itemClicked.connect(selecionar_email)

layout_conteudo.addWidget(lista_emails, 1)


# Área do e-mail selecionado
layout_email = QVBoxLayout()

layout_conteudo.addLayout(layout_email, 3)


informacao = QLabel("Selecione um e-mail")
informacao.setAlignment(Qt.AlignmentFlag.AlignCenter)

fonte = QFont()
fonte.setPointSize(14)
informacao.setFont(fonte)

layout_email.addWidget(informacao)


botao_analise = QPushButton("Análise IA")
botao_analise.hide()

layout_email.addWidget(botao_analise)


janela.show()

sys.exit(app.exec())