print("Automação Sienge Iniciada!")

#imports
import pymupdf
import re #import para expressões regulares

caminho_pdf = "Nf_n_807_Agosto_2026.pdf"

documento = pymupdf.open(caminho_pdf)  

datas = re.findall(r"\d{2}/\d{2}/\d{4}", texto)

print(f"Quantidade de páginas: {len(documento)}") 
"""
f -> permite colocar valores de     variaveis dentro do texto
len -> Retorna o tamanho de alguma coisa (Nesse caso: numero de paginas do PDF) 
"""

print("\n" + "=" * 60)

#for que se repete para cada número de página
for numero, pagina in enumerate(documento, start=1):

    texto = pagina.get_text() # -> pagina.get_text() le o texto da página 

    print(f"\n--- PÁGINA {numero} ---\n")
    print(texto)



documento.close()