# VOA Secrets Manager

A full-stack secrets management project including API backend, CLI tool, and monitoring infrastructure. Built with **FastAPI**, **Docker**, **PostgreSQL**, **Redis**, **Prometheus**, **Grafana**, and **Nginx**.

---

## Table of Contents
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Docker Deployment](#docker-deployment)
- [Backend API](#backend-api)
- [CLI Tool](#cli-tool)
- [Infrastructure](#infrastructure)
- [Environment Variables](#environment-variables)
- [Hosts File](#hosts-file)
- [License](#license)

---
[![VOA Demo](https://img.youtube.com/vi/XALXbmzHZMM/hqdefault.jpg)](https://youtu.be/XALXbmzHZMM?si=302Gt9Zp2pOI4pcl)
---

## Project Structure

```
secrets-manager-api/
├─ backend/         # FastAPI backend (click here to see [README](backend/README.md))
├─ cli/             # VOA CLI tool (click here to see [README](cli/README.md))
├─ infrastructure/  # Monitoring & services configuration
│  ├─ grafana/
│  ├─ nginx/
│  ├─ prometheus/
│  └─ redis/
├─ docker-compose.yml
├─ install.py       # Script to generate .env files and check the Dependencies
└─ LICENSE
```

> Clicking on `backend` or `cli` folders in most GitHub interfaces will redirect to their respective `README.md` files.

---

## Installation

1. Clone the repository:
```bash
git clone https://github.com/senani-derradji/VOA && cd VOA
```

2. Run the installer to create `.env` files:
```bash
python install.py
```

3. Check and update `.env` files in `backend/` and `cli/` if needed.

---

## Hosts File

Make sure to update your system's hosts file to map the local domain:

```
127.0.0.1 voa.local
```

This ensures Nginx reverse proxy and local services work correctly.

---

## Docker Deployment

1. Build and start all services using Docker Compose:
```bash
docker-compose up -d --build
```

2. Services included:
- **PostgreSQL**: `voa-db`
- **Redis**: `voa-redis`
- **Backend API**: `voa-backend`
- **Nginx**: `voa-nginx`
- **Prometheus**: `voa-prometheus`
- **Grafana**: `voa-grafana`
- **Exporters**: `postgres-exporter`, `redis-exporter`, `nginx-exporter`

3. Access points:
- FastAPI backend: `http://localhost:8000`
- Nginx: `http://localhost`
- Prometheus: `http://localhost:9090`
- Grafana: `http://localhost:3030`

---

## Backend API

The backend is located in the `backend/` folder. See [backend README](backend/README.md) for details on:
- API endpoints
- Running locally
- Docker setup
- Database initialization
- Testing

---

## CLI Tool
```bash
pip install dvoa-cli
```

The CLI tool is located in the `cli/` folder. See [CLI README](cli/README.md) for details on:
- Commands
- Authentication
- Usage examples

---

## Infrastructure

Configured services for monitoring, caching, and reverse proxy:

- **PostgreSQL** for database
- **Redis** for caching and rate limiting
- **Nginx** as reverse proxy
- **Prometheus** for metrics
- **Grafana** for dashboards
- **Exporters** for PostgreSQL, Redis, Nginx

Configuration files are located in `infrastructure/` subfolders.

---

## Environment Variables

The `install.py` script generates `.env` files with default values:

```
**** UPDATE IS COMING SOON ****
```

Update these values before deploying to production.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
