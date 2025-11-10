# VOA Secrets Manager API

A secure and robust API for managing secrets, users, and audits.  
Built with **FastAPI**, **SQLAlchemy**, **Alembic**, and Docker-ready for deployment.

---

![VOA Architecture](https://i.pinimg.com/736x/39/79/14/39791480b4e863e3ffdf6f1c642c590d.jpg)

## Features

- User management (Admin, Developer, CEO roles with RBAC)
- Secrets management with versioning and TTL
- JWT authentication and refresh tokens
- Background DEK rotation every 12 hours
- Background TTL check every 30 seconds
- Audit logging with hash-based integrity chain
- Secure password hashing
- Dockerized for easy deployment
- Alembic migrations for database version control
- Prometheus metrics & Grafana dashboards (in full mode)

---

## 🧠 Encryption Workflow

VOA uses a **dual-key encryption model** (KEK/DEK) to ensure secrets remain secure, even if one layer is compromised.

### 1. **Key Encryption Key (KEK)**
- Managed by a standalone service (`kek_server`).
- Stored securely and rotated periodically.
- Encrypts and decrypts the **DEK** file.

### 2. **Data Encryption Key (DEK)**
- Encrypted with the KEK before being saved on disk (`app/core/keys/dek.key.enc`).
- Used to encrypt all sensitive data (secrets, tokens) stored in the database.
- Rotated automatically every **12 hours** by a background task.
