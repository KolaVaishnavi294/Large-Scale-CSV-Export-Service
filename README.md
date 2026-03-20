# Large-Scale CSV Export Service with Async Streaming and Progress Tracking
## Overview

This project implements a high-performance data export service capable of streaming millions of database rows to CSV files efficiently.

The system is designed using asynchronous streaming, chunked database reads, and background job processing to ensure that exporting large datasets does not block the main application.

The application is fully containerized using Docker and Docker Compose, enabling reproducible environments and easy deployment.

This system demonstrates production-grade techniques used in analytics platforms, SaaS applications, and large-scale data processing systems.

---

## Features

- Export 10 million+ database rows to CSV

- Asynchronous background export jobs

- Streaming data processing to prevent high memory usage

- Export custom columns

- Custom CSV formatting

- Gzip compressed downloads

- Cancelable export jobs

- Progress tracking for exports

- Concurrent export jobs

- Fully Dockerized environment

---

## Architecture

The system consists of two main services:

### 1. Application Service

FastAPI based service responsible for:

- Handling API requests

- Managing export jobs

- Streaming database results

- Writing CSV files

- Serving downloads

#### 2. Database Service

PostgreSQL database containing 10 million user records used for export.

---

## Tech Stack
| Technology     | Purpose                |
| -------------- | ---------------------- |
| FastAPI        | API framework          |
| PostgreSQL     | Database               |
| AsyncPG        | Async database driver  |
| Docker         | Containerization       |
| Docker Compose | Service orchestration  |
| Python         | Backend implementation |

---

## Project Structure
```bash
data-export-service
│
├── app
│   ├── main.py
│   ├── routes.py
│   ├── exporter.py
│   ├── database.py
│   ├── job_manager.py
│   ├── config.py
│   └── schemas.py
│
├── seeds
│   └── init.sql
│
├── exports
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```
---

## Running the Application
### Start the system
```bash
docker compose up --build
```
This command will:

- Build the application container

- Start PostgreSQL

- Create database tables

- Seed 10 million records

- Start the API server

The API will be available at:
```bash
http://localhost:8080
```
Check :
```bash
docker exec -it data-export-service-db-1 psql -U exporter -d exports_db
```
Then run this :
```bash
SELECT COUNT(*) FROM users;
```
## API Endpoints
Swagger UI:
```bash
http://localhost:8080/docs
```
### Health Check
```bash
GET /health
```
Response:
```bash
{
  "status": "ok"
}
```
### Start Export
```bash
POST /exports/csv
```
Optional query parameters:

| Parameter | Description             |
| --------- | ----------------------- |
| columns   | Select specific columns |
| delimiter | Custom CSV delimiter    |
| quoteChar | Custom quote character  |

Example:
```bash
POST /exports/csv?columns=id,email
```
Response:
```bash
{
  "exportId": "uuid",
  "status": "pending"
}
```
### Check Export Status
```bash
GET /exports/{exportId}/status
```
Response:
```bash
{
  "exportId": "uuid",
  "status": "processing",
  "progress": {
      "totalRows": 10000000,
      "processedRows": 2000000,
      "percentage": 20
  },
  "createdAt": "...",
  "completedAt": "..."
}
```
### Download Export
```bash
GET /exports/{exportId}/download
```
Headers:
```bash
Content-Type: text/csv
Content-Disposition: attachment
Accept-Ranges: bytes
```
Supports resumable downloads.
### ⚠️ Note: Swagger UI may show "Error: OK" for this endpoint because it returns a file stream instead of JSON. Use a browser to download the file.

## Download With Gzip Compression
```bash
curl -H "Accept-Encoding: gzip" \
http://localhost:8080/exports/{exportId}/download
```
Response header:
```bash
Content-Encoding: gzip
```
## Cancel Export
```bash
DELETE /exports/{exportId}
```
Response:
```bash
204 No Content
```
This stops the export and deletes the partial file.

## Performance Design

The system uses several techniques to handle large datasets efficiently:

### Streaming Export

Rows are processed in small chunks instead of loading all records into memory.

### Asynchronous Jobs

Exports run in background tasks, keeping the API responsive.

### Chunked Database Reads

Database results are fetched in batches of 1000 rows to reduce memory usage.

### Backpressure Handling

Streaming ensures the writer does not overwhelm the system.

### Memory Control

The Docker container is limited to 150MB memory usage.

## Testing the System

Start an export:
```bash
Invoke-RestMethod -Method POST http://localhost:8080/exports/csv
```
Check progress:
```bash
Invoke-RestMethod http://localhost:8080/exports/{exportId}/status
```
Download file:
```bash
curl http://localhost:8080/exports/{exportId}/download -o export.csv
```
## Concurrency

The system supports multiple export jobs simultaneously.

Each job runs independently and maintains its own progress state.

## Dataset

The database contains:

```bash
10,000,000 user records
```
Schema:

| Column            | Type      |
| ----------------- | --------- |
| id                | SERIAL    |
| name              | VARCHAR   |
| email             | VARCHAR   |
| signup_date       | TIMESTAMP |
| country_code      | CHAR(2)   |
| subscription_tier | VARCHAR   |
| lifetime_value    | NUMERIC   |

## Scalability Considerations

The system is designed to scale by:

- Using async streaming

- Offloading work to background tasks

- Avoiding large in-memory datasets

- Supporting concurrent exports