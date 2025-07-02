import requests
import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from azure.ai.formrecognizer import DocumentAnalysisClient
import os

# Configurações (Substitua com suas informações)
AZURE_LOCATION = os.environ.get("AZURE_LOCATION", "<SUA_LOCALIZACAO>")
TRANSLATOR_KEY = os.environ.get("TRANSLATOR_KEY", "<SUA_CHAVE_TRANSLATOR>")
LANGUAGE_ENDPOINT = os.environ.get("LANGUAGE_ENDPOINT", "<SEU_ENDPOINT_LANGUAGE>")
LANGUAGE_KEY = os.environ.get("LANGUAGE_KEY", "<SUA_CHAVE_LANGUAGE>")
DOCUMENT_INTELLIGENCE_ENDPOINT = os.environ.get("DOCUMENT_INTELLIGENCE_ENDPOINT", "<SEU_ENDPOINT_DOCUMENT_INTELLIGENCE>")
DOCUMENT_INTELLIGENCE_KEY = os.environ.get("DOCUMENT_INTELLIGENCE_KEY", "<SUA_CHAVE_DOCUMENT_INTELLIGENCE>")
LINGUAGEM_ALVO = "pt"
MODELO_PERSONALIZADO_ID = None # Preencha com o ID do seu modelo Custom Translator se usar.

def extract_text_from_pdf(document_path):
    """Extrai texto de um PDF usando Azure AI Document Intelligence."""
    try:
        document_analysis_client = DocumentAnalysisClient(
            endpoint=DOCUMENT_INTELLIGENCE_ENDPOINT, credential=AzureKeyCredential(DOCUMENT_INTELLIGENCE_KEY)
        )

        with open(document_path, "rb") as f:
            poller = document_analysis_client.begin_analyze_document("prebuilt-document", document=f)
        result = poller.result()

        texto_extraido = ""
        for page in result.pages:
            for line in page.lines:
                texto_extraido += line.content + " "
        return texto_extraido
    except Exception as e:
        print(f"Erro ao extrair texto do PDF: {e}")
        return None

def detect_language(texto):
    """Detecta o idioma do texto usando Azure AI Language."""
    try:
        text_analytics_client = TextAnalyticsClient(endpoint=LANGUAGE_ENDPOINT, credential=AzureKeyCredential(LANGUAGE_KEY))
        documento = [texto]

        response = text_analytics_client.detect_language(documento)

        for document in response:
            if document.primary_language:
                return document.primary_language.iso6391_name
            else:
                print("Não foi possível detectar o idioma.")
                return None
    except Exception as e:
        print(f"Erro ao detectar idioma: {e}")
        return None

def translate_text(texto, linguagem_origem, linguagem_alvo, modelo_personalizado_id=None):
    """Traduz o texto usando Azure AI Translator."""
    endpoint = "https://api.cognitive.microsofttranslator.com"
    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'to': linguagem_alvo,
        'from': linguagem_origem
    }
    if modelo_personalizado_id:
        params['category'] = modelo_personalizado_id  # Usar o modelo personalizado

    headers = {
        'Ocp-Apim-Subscription-Key': TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': AZURE_LOCATION,
        'Content-type': 'application/json'
    }

    body = [{
        'text': texto
    }]

    try:
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        request.raise_for_status()  # Lança uma exceção para códigos de status HTTP ruins
        response = request.json()
        texto_traduzido = response[0]['translations'][0]['text']
        return texto_traduzido
    except requests.exceptions.RequestException as e:
        print(f"Erro na tradução: {e}")
        if request.response is not None:
             print(f"Código de status HTTP: {request.response.status_code}")
             print(f"Resposta do servidor: {request.response.text}")
        return None

# Exemplo de uso
document_path = "meu_artigo_tecnico.pdf"
texto_extraido = extract_text_from_pdf(document_path)

if texto_extraido:
    linguagem_origem = detect_language(texto_extraido)
    if linguagem_origem:
        texto_traduzido = translate_text(texto_extraido, linguagem_origem, LINGUAGEM_ALVO, MODELO_PERSONALIZADO_ID)
        if texto_traduzido:
            print("Texto Traduzido:")
            print(texto_traduzido)
        else:
            print("Falha ao traduzir o texto.")
    else:
        print("Falha ao detectar o idioma.")
else:
    print("Falha ao extrair o texto do PDF.")