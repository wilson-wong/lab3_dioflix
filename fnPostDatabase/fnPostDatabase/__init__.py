import logging
import os
import json
from azure.functions import HttpRequest, HttpResponse
from azure.cosmos import CosmosClient, exceptions, PartitionKey
from ..models.movie_request import MovieRequest
import azure.functions as func

# Retrieve Cosmos DB connection details from environment variables
cosmos_db_connection = os.getenv('COSMODB_CONNECTION')
cosmos_db_name = os.getenv('COSMOS_DB_NAME')
cosmos_db_container = os.getenv('COSMOS_DB_CONTAINER')

# Initialize Cosmos DB client
client = CosmosClient.from_connection_string(cosmos_db_connection)
database = client.create_database_if_not_exists(id=cosmos_db_name)
container = database.create_container_if_not_exists(
    id=cosmos_db_container,
    # partition_key=PartitionKey(path="/partitionKey"),
    partition_key=PartitionKey(path="/id"),
    offer_throughput=400)

def main(req: HttpRequest) -> HttpResponse:
    logging.info('Função de gatilho HTTP Python processou uma solicitação.')

    route = req.route_params.get('route')
    if route == 'movie':
        return handle_movie(req)
    elif route == 'details':
        return handle_details(req)
    elif route == 'getAllMovies':
        return handle_getAllMovies(req)
    else:
        return func.HttpResponse("Rota não encontrada", status_code=404)

    
def handle_movie(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        if not req_body:
            return HttpResponse("Faltando 'movie_request' no corpo da solicitação.", status_code=400)
    except ValueError:
        return HttpResponse("JSON inválido no corpo da solicitação.", status_code=400)

    try:
        movie = MovieRequest(
            title=req_body.get('title'),
            year=req_body.get('year'),
            video=req_body.get('video'),
            thumbnail=req_body.get('thumbnail')
        )
        
        container.create_item(body=movie.to_dict())
        return HttpResponse("Solicitação de filme foi postada com sucesso.", status_code=201)
    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"Erro ao salvar no Cosmos DB: {e}")
        return HttpResponse("Erro ao salvar no Cosmos DB.", status_code=500)
    
def handle_getAllMovies(req: func.HttpRequest) -> func.HttpResponse:
    try:
        query = "SELECT * FROM c"
        items = list(container.query_items(
            query=query,
            enable_cross_partition_query=True
        ))
        return func.HttpResponse(json.dumps(items), status_code=200, mimetype="application/json")
    except exceptions.CosmosHttpResponseError as e:
        logging.error(f"Erro ao buscar filmes no Cosmos DB: {e}")
        return func.HttpResponse("Erro ao buscar filmes no Cosmos DB.", status_code=500)