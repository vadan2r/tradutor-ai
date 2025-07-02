from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

endpoint = "<SEU_ENDPOINT_LANGUAGE>"
key = "<SUA_CHAVE_LANGUAGE>"

text_analytics_client = TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

documento = [texto_extraido] # ou o texto do seu artigo

response = text_analytics_client.detect_language(documento)

for document in response:
    print(f"Idioma detectado: {document.primary_language.name} ({document.primary_language.iso6391_name})")
    linguagem_origem = document.primary_language.iso6391_name