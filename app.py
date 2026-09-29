import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
chave_api = os.getenv("GEMINI_API_KEY")
cliente = genai.Client(api_key=chave_api)
tipo_negocio =input ("Digite o tipo de negócio:")
nome_produto = input ("digite o nome do produto ou serviço:")
preco = float (input("digite o preço:"))
objetivo = input("Digite o objetivo da publicação:")
formato = input ("digite o formato da publicação:")
Prompt = f" Crie um {formato} sobre {nome_produto} para {tipo_negocio}."
Prompt += f" O preço é R$ {preco:.2f}."
Prompt += f" O objetivo da publicação é {objetivo}."

resposta = cliente.models.generate_content(model="gemini-3.1-flash-lite", contents=Prompt)
print ("\n---RESUMO---")
print ("Tipo de negócio:",tipo_negocio)
print ("Produto ou Serviço:",nome_produto)
print (f"Preço: R$ {preco:.2f}")
print ("Objetivo:", objetivo)
print ("formato:", formato)
print ("Prompt:", Prompt )
print ("\n---CONTEÚDO GERADO PELA IA---")
print (resposta .text)