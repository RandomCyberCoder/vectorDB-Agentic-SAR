# vectorDB-Agentic-SAR
Building Knowledge Base for SAR Agentic AI

# local qdrant setup
docker compose up -d

This command will create a volume called "qdrant_storage" to store database data

Note that qdrant does not enable security be default. The config.yaml is still being worked on so security can
be included. One this is done it will be added to the volumes section in the docker-compose file 
as "$(pwd)/config.yaml:/qdrant/config/config.yaml"
