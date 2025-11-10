# 🔐 VOA — Vaulity Ops API  
### Secure Secrets Management Platform with RBAC, TTL, Encryption Rotation, and Observability

![GitHub last commit](https://img.shields.io/github/last-commit/senani-derradji/VOA)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-success)
![Docker](https://img.shields.io/badge/Docker-Compose-important)
![License](https://img.shields.io/github/license/senani-derradji/VOA)

---

## 🧩 Overview

**VOA (Vaulity Ops API)** is a **secure secrets manager** built with **FastAPI** that provides encryption, rotation, access control, and observability features for managing application secrets and credentials.

It supports **RBAC (Role-Based Access Control)**, **JWT authentication**, **TTL expiration for secrets**, **audit logging with integrity checks**, and **automatic key rotation (KEK/DEK)**.

VOA can run in two modes:
- 🟢 **Mini**: Lightweight version with SQLite and minimal services.
- 🧱 **Full**: Production-ready stack with PostgreSQL, Redis, Prometheus, and Grafana.

---

## 🧠 Core Concepts

| Component | Description |
|------------|-------------|
| **KEK (Key Encryption Key)** | Managed by a dedicated `kek_server` container. It encrypts the DEK for the backend. |
| **DEK (Data Encryption Key)** | Used to encrypt/decrypt secrets in the database. Automatically rotated every 12 hours. |
| **RBAC System** | Supports roles: `Admin`, `Developer`, and `CEO`, each with specific permissions. |
| **JWT Authentication** | Login/Refresh tokens for user authentication. |
| **Secrets CRUD + Versioning** | Create, read, update, delete secrets with version history and TTL expiration. |
| **TTL System** | Background task checks for expired users/secrets and removes them automatically. |
| **Audit Log + Integrity Chain** | Every action is hashed and linked to ensure tamper-proof audit trails. |
| **Monitoring Stack** | Prometheus exporters and Grafana dashboards (in full mode). |
| **Nginx Reverse Proxy** | Manages frontend/backend routing and SSL termination. |

---

## 🚀 Features

### 🛡️ Security
- AES/Fernet-based encryption
- Dual-layer KEK/DEK encryption system
- Automatic DEK rotation every **12 hours**
- Secure webhook for KEK update
- JWT + refresh tokens
- Rate limiting (via `slowapi`)

### 👥 Access Control
- Role-based permissions (`Admin`, `Developer`, `CEO`)
- Centralized user and secret management

### ⏰ Lifecycle Management
- Background **TTL checks** for users/secrets
- Versioning of secrets
- Automated cleanup

### 🧾 Audit & Integrity
- Logging of all critical actions
- Tamper-proof chain using hash linking (mini blockchain)
- Exportable audit trails

### 📊 Observability (Full Mode)
- Prometheus metrics via `prometheus_fastapi_instrumentator`
- Redis caching layer
- Grafana dashboards with preconfigured exporters

---

## 🐳 Deployment

### 🟢 Mini Mode (Local or Development)

Includes:
> KEK Server, Backend (FastAPI), SQLite, NGINX (n) / FullMode (y)

```bash
# Clone the repo
git clone https://github.com/senani-derradji/VOA.git
cd VOA && py install.py
