import azure.functions as func
import logging
import json
import os
from azure.cosmos import CosmosClient

# Initialize Cosmos client
COSMOSDB_CONNECTION_STRING = COSMOSDB_CONNECTION_STRING = os.getenv("COSMOSDB_CONNECTION_STRING")
client = CosmosClient.from_connection_string(COSMOSDB_CONNECTION_STRING)
database_name = 'VisitorData'
container_name = 'VisitorCount'
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="VisitorCougit punterFunction")
def VisitorCounterFunction(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        # Retrieve the current count from Cosmos DB
        item = container.read_item(item='1', partition_key='1')
        count = item.get('count', 0)

        # Increment the count
        count += 1
        item['count'] = count

        # Update the item in Cosmos DB
        container.replace_item(item='1', body=item)

        # Return the updated count
        return func.HttpResponse(
            json.dumps({'count': count}),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            "Error processing request.",
            status_code=500
        )
