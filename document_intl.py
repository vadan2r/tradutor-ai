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