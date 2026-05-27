# Neo4j API

A simple FastAPI-based REST API for managing products, categories, suppliers, customers, and orders using a Neo4j graph database.

## Features

- CRUD operations for products, categories, suppliers, customers, and orders
- Neo4j database integration via `neomodel`
- FastAPI routers for clean API design
- Built-in health check endpoint

## Requirements

- Python 3.11+ (or compatible)
- Neo4j database
- `docker-compose` (recommended for local Neo4j setup)

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

- a `.env` file for application database configuration
- Docker Compose native secrets for Neo4j authentication

The Docker Compose service is configured to read Neo4j credentials from the secret source file `./neo4j_auth.txt`.

## Run the API

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## Endpoints

The application includes routers for:

- `/products`
- `/categories`
- `/suppliers`
- `/customers`
- `/orders`

Use the generated OpenAPI docs at `http://127.0.0.1:8000/docs` for detailed operation information.

## Testing

Run tests with:

```bash
pytest
```

## Project Structure

- `app/`
  - `main.py` - FastAPI application entrypoint
  - `database.py` - Neo4j database connection management
  - `routers/` - API route definitions
  - `schemas/` - Pydantic request/response schemas
  - `services/` - business logic and CRUD operations
  - `models/` - domain model definitions
- `tests/` - test suite
- `docker-compose.yaml` - local Neo4j service definition
- `requirements.txt` - Python dependencies

## Notes

This repository is designed as a starter API blueprint for Neo4j-backed FastAPI services. Adjust database settings, authentication, and models to fit your use case.
