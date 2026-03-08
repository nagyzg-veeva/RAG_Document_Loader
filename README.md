# RAG Document Loader

A Python application for loading documents into Google Cloud Vertex AI RAG corpora with plugin architecture and version tracking.

## Docker Setup

### Prerequisites
- Docker and Docker Compose installed
- Google Cloud credentials (JSON file)
- Environment variables configured

### Building the Docker Image

```bash
# Build the image
docker build -t rag-document-loader .

# Run the container
docker run --rm \
  -e DB_HOST=your_db_host \
  -e DB_USER=your_db_user \
  -e DB_PASS=your_db_pass \
  -e DB_NAME=your_db_name \
  -e GCP_PROJECT_ID=your_project_id \
  -e GCP_LOCATION=your_location \
  -e GCP_CORPUS_NAME=projects/your-project/locations/your-location/ragCorpora/your-corpus \
  -v $(pwd)/credentials:/app/credentials:ro \
  -v $(pwd)/config:/app/config:ro \
  -v $(pwd)/plugins:/app/plugins:ro \
  rag-document-loader
```

### Using Docker Compose

1. Create a `.env` file with your environment variables:
```bash
DB_HOST=postgres
DB_USER=rag_user
DB_PASS=rag_password
DB_NAME=rag_database
DB_TABLE_NAME=file_tracker
GCP_PROJECT_ID=your-project-id
GCP_LOCATION=us-central1
GCP_CORPUS_NAME=projects/your-project/locations/us-central1/ragCorpora/your-corpus
```

2. Place your Google Cloud credentials in `credentials/credentials.json`

3. Start the services:
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Run a single execution
docker-compose run --rm rag-document-loader python main.py

# Stop services
docker-compose down
```

### Development with Docker

```bash
# Build and run in development mode
docker-compose up --build

# Run tests
docker-compose run --rm rag-document-loader python -m unittest discover

# Access PostgreSQL database
docker-compose exec postgres psql -U rag_user -d rag_database
```

### Dockerfile Features
- Uses Python 3.13 slim image for smaller size
- Installs system dependencies for PostgreSQL support
- Uses `uv` for fast dependency management
- Creates non-root user for security
- Sets proper Python environment variables
- Includes volume mounts for configuration and credentials

### Security Notes
- Google Cloud credentials should be mounted as read-only volumes
- Never commit credentials to version control
- Use environment variables for sensitive data
- The container runs as a non-root user

## Todo

### Dockling
Generic dockling method for text document conversion

### Version Service
A way to provide the plugins with the last know version of the stored documents

- Last modified date
- Version number
- etc.

The versions should store in a database.
- document name
- document source
- last version

### PostgreSQL: libpq-dev necessary to install the psycopg2 module