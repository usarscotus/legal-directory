# Local Elasticsearch Setup

This project includes a [`docker-compose.yml`](../docker-compose.yml) for running Elasticsearch locally.

## Start Elasticsearch

```bash
docker-compose up -d elasticsearch
```

The service exposes the cluster on <http://localhost:9200>.

Verify that Elasticsearch is running:

```bash
curl http://localhost:9200
```

## Stop Elasticsearch

When finished, shut down the container:

```bash
docker-compose down
```
