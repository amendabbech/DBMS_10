# Blutspende-Verwaltungssystem

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688.svg) ![Python](https://img.shields.io/badge/Python-3.12+-yellow.svg) ![Debian Package](https://img.shields.io/badge/Package-Debian%20.deb-D70A53.svg) ![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)

A database-backed blood donation management system built for the Term Project of Introduction to Database Management Systems (THGA Bochum).

It manages donors (Spender), donation centers (Spendezentren) and donations (Spenden), and enforces the mandatory 56-day waiting period between two donations directly at the database level via a PostgreSQL trigger.

## Documentation

| Document | Format | Description |
|---|---|---|
| Documentation | Separate repository: https://github.com/amendabbech/DBMS_10-documentation | ER model, relational schema, API design, deployment |
| Proposal | out/proposal.pdf (run make locally to build) | Original project proposal |

## System architecture

    db-frontend (tkinter GUI)
        HTTP/JSON, header: X-API-Key
        v
    FastAPI backend (Uvicorn)
        psycopg2
        v
    PostgreSQL 16 (Docker)
        tables: spender, spende, spendezentrum
        trigger: 56-day minimum interval between donations

## Core features

- 56-day donation rule enforced in the database, via a PostgreSQL trigger (trg_spendeabstand), so the constraint holds regardless of which client writes data.
- Relational schema in 3NF: spender, spendezentrum, spende (N:M between donors and centers, resolved through donations).
- REST API (FastAPI) with public GET endpoints and X-API-Key protected POST endpoints.
- Desktop GUI (tkinter) with a connection dialog and tabs for Spender, Spendezentrum and Spende, packaged as a native .deb.
- Containerized backend via Docker Compose.

## Repository layout

    system/
      db/schema.sql            PostgreSQL schema and trigger
      backend/                 FastAPI application
      frontend/db-frontend/    tkinter GUI, uv-managed, packaged as .deb
    docker-compose.yml

## Running the system

1. Start the database

       docker-compose up -d

2. Start the backend

       cd system/backend
       source venv/bin/activate
       uvicorn main:app --host 0.0.0.0 --port 8000

3. Install and launch the frontend

       cd system/frontend/db-frontend
       sudo dpkg -i db-frontend_0.1.0_amd64.deb
       db-frontend

In the connection dialog, enter the API URL (http://localhost:8000) and the X-API-Key (default: geheimschluessel123, see system/backend/main.py).

Note: this key is hardcoded for demo/grading purposes. In a real deployment, it should be set via an environment variable instead of being committed to source control.

## Links

- Documentation repository: https://github.com/amendabbech/DBMS_10-documentation
- Author: Amen Allah Dabbech
