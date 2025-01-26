# Azure Function Project - DIOFlix

This project contains Azure Functions to handle movie data using Cosmos DB. The functions include creating, retrieving, and listing movies.

## Prerequisites

- Python 3.8+
- Azure Functions Core Tools
- Azure CLI
- An Azure Cosmos DB account

## Setup

1. Clone the repository:

    ```bash
    git clone https://github.com/your-repo/dioflix.git
    cd dioflix/fnPostDatabase
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3. Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Update the `local.settings.json` file with your Azure Cosmos DB connection details:

    ```json
    {
      "IsEncrypted": false,
      "Values": {
        "AzureWebJobsStorage": "DefaultEndpointsProtocol=...",
        "FUNCTIONS_WORKER_RUNTIME": "python",
        "COSMOS_DB_CONNECTION": "your_cosmos_db_connection_string",
        "COSMOS_DB_NAME": "your_cosmos_db_name",
        "COSMOS_DB_CONTAINER": "your_cosmos_db_container"
      }
    }
    ```

## Running the Functions Locally

1. Start the Azure Functions runtime:

    ```bash
    func start
    ```

2. The functions will be available at `http://localhost:7071`.

## Functions

### POST /movie

Creates a new movie entry in Cosmos DB.

- **Request Body:**

    ```json
    {
      "title": "Inception",
      "year": 2010,
      "video": "https://example.com/inception.mp4",
      "thumbnail": "https://example.com/inception.jpg"
    }
    ```

- **Response:**

    ```json
    {
      "message": "Movie request has been posted successfully."
    }
    ```

### GET /details?id={movie_id}

Retrieves a movie entry by its ID.

- **Response:**

    ```json
    {
      "id": "movie_id",
      "title": "Inception",
      "year": 2010,
      "video": "https://example.com/inception.mp4",
      "thumbnail": "https://example.com/inception.jpg"
    }
    ```

### GET /getAllMovies

Retrieves all movie entries.

- **Response:**

    ```json
    [
      {
        "id": "movie_id",
        "title": "Inception",
        "year": 2010,
        "video": "https://example.com/inception.mp4",
        "thumbnail": "https://example.com/inception.jpg"
      },
      ...
    ]
    ```

## Deployment

1. Login to Azure:

    ```bash
    az login
    ```

2. Create a resource group:

    ```bash
    az group create --name dioflix-rg --location eastus
    ```

3. Create a storage account:

    ```bash
    az storage account create --name dioflixstorage --location eastus --resource-group dioflix-rg --sku Standard_LRS
    ```

4. Deploy the function app:

    ```bash
    func azure functionapp publish dioflix-func-app
    ```
