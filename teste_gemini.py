from google import genai

cliente = genai.Client()

resposta = cliente.models.generate_content(
    model="gemini-3.7-flash",
    contents="Responda apenas: conexão funcionando!"
)

print(resposta.text)