# tradutor-ai
Projeto DIO - Criar tradutor de artigo tecnico com azureai.

## Passo a Passo para Criar um Tradutor de Artigos Técnicos com Azure AI

- Este guia oferece um passo a passo para construir um tradutor de artigos técnicos utilizando os serviços de IA da Azure. 

- Assumimos que você tenha uma conta Azure ativa e conhecimentos básicos de programação (Python será utilizado como exemplo).

1. Planejamento e Preparação:

# Definir o escopo:
- Domínio técnico: Qual área técnica seus artigos cobrem? (e.g., engenharia de software, medicina, finanças) Isso influenciará o vocabulário especializado que o tradutor precisará aprender.
- Línguas: Quais línguas serão suportadas para tradução? Defina a língua de origem e as línguas alvo.
- Volume: Quantos artigos você planeja traduzir? Isso ajudará a determinar o nível de personalização necessário e o custo dos serviços Azure.

# Escolher os serviços Azure:
- Azure AI Translator: O principal serviço para tradução automática.
- Azure AI Document Intelligence (Opcional): Para extrair texto formatado de documentos complexos (PDFs, imagens, etc.) antes da tradução. Útil se os artigos não estiverem em texto simples.
- Azure AI Language: Para tarefas de processamento de linguagem natural (PNL) como detecção de idioma, reconhecimento de entidades nomeadas (NER) e análise de sentimento. (Opcional, mas útil para melhorar a qualidade da tradução).
- Azure Custom Translator (Opcional): Permite personalizar o modelo de tradução com terminologia e estilo específicos do seu domínio técnico. Essencial para obter traduções de alta qualidade em áreas especializadas.

# Configurar o ambiente Azure:
Crie um grupo de recursos no Azure para organizar seus recursos.
Crie instâncias dos serviços Azure escolhidos (Translator, Document Intelligence, Language, Custom Translator) dentro do grupo de recursos.
Obtenha as chaves de API e endpoints de cada serviço. Guarde-as com segurança.

2. Extração do Texto (se necessário):

- Se seus artigos estiverem em formato não textual (PDFs, imagens), utilize o Azure AI Document Intelligence para extrair o texto.

# Exemplo em Python (Document Intelligence):

from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

endpoint = "<SEU_ENDPOINT_DOCUMENT_INTELLIGENCE>"
key = "<SUA_CHAVE_DOCUMENT_INTELLIGENCE>"

document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# Caminho para o documento
document_path = "meu_artigo_tecnico.pdf"

# Opções de leitura do documento (padrão para documentos gerais)
with open(document_path, "rb") as f:
    poller = document_analysis_client.begin_analyze_document("prebuilt-document", document=f)
result = poller.result()

# Extrair o texto
texto_extraido = ""
for page in result.pages:
    for line in page.lines:
        texto_extraido += line.content + " "


3. Detecção do Idioma (Opcional):

- Se você não souber o idioma de origem do artigo, utilize o Azure AI Language para detectá-lo.

# Exemplo em Python (Azure AI Language):

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


4. Tradução com Azure AI Translator:

- Utilize o serviço Azure AI Translator para traduzir o texto.

# Exemplo em Python (Azure AI Translator):

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


5. Personalização da Tradução (Opcional, mas Recomendado):

- Para obter traduções de alta qualidade em domínios técnicos, utilize o Azure Custom Translator para personalizar o modelo de tradução.

- Criar um workspace: Crie um workspace no Azure Custom Translator.

- Criar um projeto: Crie um projeto específico para o seu domínio técnico e línguas alvo.

- Carregar dados de treinamento:
    - Dados paralelos: Carregue pares de frases ou documentos com o texto original e a tradução correspondente (de alta qualidade). Quanto mais dados, melhor será a personalização.
    - Dados monolíngues: Carregue dados monolíngues (apenas na língua alvo) para ajudar o modelo a entender o estilo e o vocabulário do domínio técnico.
    - Glossários: Carregue glossários de termos técnicos e suas traduções preferidas. Isso garante a consistência da terminologia.

- Treinar o modelo: Treine um novo modelo personalizado com os dados carregados. O processo de treinamento pode levar algum tempo.

- Implantar o modelo: Implante o modelo treinado para torná-lo acessível para uso.

- Utilizar o modelo personalizado na tradução: Ao fazer a chamada para o Azure AI Translator, especifique o ID do modelo personalizado. A documentação do Azure Translator explica como fazer isso.

6. Pós-processamento (Opcional):

- Após a tradução, você pode realizar um pós-processamento para melhorar a qualidade do texto:
    - Revisão manual: A revisão por um especialista no domínio técnico e nas línguas envolvidas é fundamental para garantir a precisão e a fluidez da tradução.
    - Correção gramatical e ortográfica: Utilize ferramentas de correção gramatical e ortográfica na língua alvo.
    - Formatação: Restaure a formatação original do artigo (títulos, listas, tabelas, etc.).

7. Testes e Iteração:

- Traduza vários artigos de teste e avalie a qualidade da tradução.
- Se a qualidade não for satisfatória, refine os dados de treinamento no Azure Custom Translator, ajuste os parâmetros de tradução ou invista em revisão manual mais aprofundada.


# Código de Exemplo Completo (com tratamento de erros e melhorias):

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


# Observações Importantes:

- Custo: Os serviços Azure têm custos associados. Monitore o uso e otimize para reduzir os custos. O Custom Translator pode ter custos de treinamento e hospedagem de modelos.

- Segurança: Proteja suas chaves de API e dados confidenciais.

- Escalabilidade: Planeje a escalabilidade da sua solução se você espera traduzir um grande volume de artigos.

- Qualidade da Tradução: A qualidade da tradução automática depende muito da qualidade dos dados de treinamento e da complexidade do texto. A revisão manual é sempre recomendada para traduções críticas.

- Documentação Azure: Consulte a documentação oficial da Azure para obter informações detalhadas sobre os serviços e suas APIs:

    - Azure AI Translator: https://learn.microsoft.com/pt-br/azure/cognitive-services/translator/translator-api

    - Azure AI Document Intelligence: https://learn.microsoft.com/pt-br/azure/ai-services/document-intelligence/

    - Azure AI Language: https://learn.microsoft.com/pt-br/azure/cognitive-services/language-service/

    - Azure Custom Translator: https://learn.microsoft.com/pt-br/azure/cognitive-services/translator/custom-translator/overview

- Este guia oferece um ponto de partida. A implementação real dependerá dos seus requisitos específicos. Boa sorte!
