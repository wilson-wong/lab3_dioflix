import json
import logging

from azure.functions import HttpRequest, HttpResponse
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient


def main(req: HttpRequest) -> HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    filetype = req.headers.get('file-type')
    if not filetype:
        return HttpResponse(
            "O cabeçalho 'file-type' é obrigatório.",
            status_code=400
        )

    file = req.files['file']
    if not file or file.filename == '':
        return HttpResponse(
            "O arquivo não pode ser nulo ou vazio.",
            status_code=400
        )

    connection_string = os.getenv('AzureWebJobsStorage')
    if not connection_string:
        return HttpResponse(
            "A variável de ambiente 'AzureWebJobsStorage' é obrigatória.",
            status_code=500
        )

    try:
        blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        container_client = blob_service_client.get_container_client(filetype)
        blob_client = container_client.get_blob_client(file.filename)
        blob_client.upload_blob(file.stream, overwrite=True, max_concurrency=4)
    except Exception as e:
        logging.error(f"Erro ao fazer upload do arquivo '{file.filename}' do tipo '{filetype}': {e}")
        return HttpResponse(
            "Erro ao fazer upload do arquivo.",
            status_code=500
        )

    blob_url = blob_client.url
    response_body = {
        "message": "Arquivo armazenado com sucesso.",
        "blobURI": blob_url
    }
    return HttpResponse(
        json.dumps(response_body),
        status_code=200,
        mimetype="application/json"
    )