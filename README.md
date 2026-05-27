# Neo4j API

A simple FastAPI-based REST API for managing products, categories, suppliers, customers, and orders using a Neo4j graph database.

## Features

* CRUD operations for products, categories, suppliers, customers, and orders
* Neo4j database integration via `neomodel`
* FastAPI routers for clean API design
* Built-in health check endpoint
* Support for importing Neo4j's prebuilt Northwind dataset

## Requirements

* Python 3.11+ (or compatible)
* Neo4j database
* `docker-compose` (recommended for local Neo4j setup)

## Setup

1. Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create the application `.env` file and the Docker secret file for Neo4j:

```bash
cp .env.example .env
cp neo4j_auth.txt.example neo4j_auth.txt
```

Edit `.env` if you need to change the Neo4j connection string, and replace the placeholder password in `neo4j_auth.txt`.

4. Start Neo4j locally with Docker Compose:

```bash
docker compose up -d
```

5. Confirm Neo4j is running on `http://localhost:7474` and Bolt is available on `bolt://localhost:7687`.

## Configuration

This project uses:

* a `.env` file for application database configuration
* Docker Compose native secrets for Neo4j authentication

The Docker Compose service is configured to read Neo4j credentials from the secret source file `./neo4j_auth.txt`.

## Import Northwind Sample Dataset

This project can be initialized with Neo4j's prebuilt Northwind dataset.

Dataset source:

* [https://github.com/neo4j-graph-examples/northwind/blob/main/scripts/northwind.cypher](https://github.com/neo4j-graph-examples/northwind/blob/main/scripts/northwind.cypher)

### Option 1: Import Directly Using Cypher Shell

1. Download the dataset script:

```bash
curl -o northwind.cypher \
https://raw.githubusercontent.com/neo4j-graph-examples/northwind/main/scripts/northwind.cypher
```

2. Import the dataset into the running Neo4j instance:

```bash
cat northwind.cypher | docker exec -i neo4j cypher-shell \
-u neo4j \
-p $(cat neo4j_auth.txt)
```

If your Neo4j container name is different, replace `neo4j` in the command above with your actual container name.

### Option 2: Import from Neo4j Browser

1. Open Neo4j Browser:

```text
http://localhost:7474
```

2. Login using the credentials configured in your `.env` and `neo4j_auth.txt`.

3. Copy the contents of the `northwind.cypher` file.

4. Paste and execute the script inside Neo4j Browser.

### Verify Dataset Import

Run the following Cypher queries inside Neo4j Browser:

```cypher
MATCH (p:Product)
RETURN count(p) AS total_products;
```

```cypher
MATCH (c:Customer)
RETURN count(c) AS total_customers;
```

```cypher
MATCH (o:Order)
RETURN count(o) AS total_orders;
```

If records are returned successfully, the dataset import is complete.

## Run the API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Endpoints

The application includes routers for:

* `/products`
* `/categories`
* `/suppliers`
* `/customers`
* `/orders`

Use the generated OpenAPI docs at `http://127.0.0.1:8000/docs` for detailed operation information.

## Testing

Run tests with:

```bash
pytest
```

## Project Structure

* `app/`

  * `main.py` - FastAPI application entrypoint
  * `database.py` - Neo4j database connection management
  * `routers/` - API route definitions
  * `schemas/` - Pydantic request/response schemas
  * `services/` - business logic and CRUD operations
  * `models/` - domain model definitions
* `tests/` - test suite
* `docker-compose.yaml` - local Neo4j service definition
* `requirements.txt` - Python dependencies

## Notes

This repository is designed as a starter API blueprint for Neo4j-backed FastAPI services. Adjust database settings, authentication, and models to fit your use case.

The imported Northwind dataset is useful for testing graph relationships, API development, and Neo4j query experimentation.
