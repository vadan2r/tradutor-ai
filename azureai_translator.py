import requests
import json

endpoint = "https://api.cognitive.microsofttranslator.com"
location = "<SUA_LOCALIZACAO>" # e.g., "eastus"
key = "<SUA_CHAVE_TRANSLATOR>"
linguagem_alvo = "pt" # Português
path = '/translate'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'to': linguagem_alvo,
    'from': linguagem_origem # Se você detectar o idioma, use o resultado aqui
}

headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json'
}

body = [{
    'text': texto_extraido
}]

request = requests.post(constructed_url, params=params, headers=headers, json=body)
response = request.json()

texto_traduzido = response[0]['translations'][0]['text']

print(texto_traduzido)