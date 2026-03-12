# Real-Time Event Processing System

This project is a backend system designed to ingest, process, and serve real-time sensor events in a scalable and reliable way. It uses an event-driven architecture with Apache Kafka for asynchronous processing, Redis for caching, and MySQL for persistent storage.

The system is built to handle high-throughput event ingestion while keeping read APIs fast and consistent.

---

## System Architecture

The system follows an event-driven architecture designed for scalable real-time event processing.

Components:

- **FastAPI API Service**  
  Handles incoming sensor events and publishes them to Kafka.

- **Apache Kafka**  
  Acts as the event streaming platform and message broker.

- **Consumer Service**  
  Consumes events from Kafka, processes them, and stores them in MySQL.

- **MySQL Database**  
  Stores processed sensor events persistently.

- **Redis Cache**  
  Provides fast access for read APIs using a cache-aside strategy.

- **Docker Compose**  
  Orchestrates all services and infrastructure components.

## Overview

The system consists of two main services:

- **API Service**
  - Accepts sensor events via REST APIs
  - Publishes events to Kafka
  - Serves processed data through cached read endpoints

- **Consumer Service**
  - Consumes events from Kafka
  - Processes and stores events in MySQL
  - Invalidates Redis cache when new data arrives

Supporting infrastructure includes Kafka, ZooKeeper, Redis, and MySQL, all orchestrated using Docker Compose.

---
## Event Processing Flow

1. A client sends a sensor event to the API service.
2. The API validates the payload and publishes the event to the Kafka topic `sensor_readings`.
3. Kafka stores the event and makes it available to consumers.
4. The consumer service reads the event from Kafka.
5. The consumer processes the event and stores it in the MySQL `processed_events` table.
6. Redis cache entries related to that sensor are invalidated.
7. Future API requests fetch fresh data from the database and update the cache.

## Technology Stack

- Python 3.11
- FastAPI
- Apache Kafka
- Redis
- MySQL
- SQLAlchemy
- Pytest
- Docker and Docker Compose

---

## Project Structure

```text
my-event-processing-system/
├── app/
│   ├── api/        # API routes
│   ├── kafka/      # Kafka producer and consumer
│   ├── cache/      # Redis cache logic
│   ├── models/     # Database models
│   ├── schemas/    # Request/response schemas
│   └── main.py     # FastAPI application entry point
├── tests/          # Unit and integration tests
├── Dockerfile.api
├── Dockerfile.consumer
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup Instructions

### Prerequisites

- Docker
- Docker Compose

### Environment Variables

Create a `.env` file using the template below:


```env
MYSQL_ROOT_PASSWORD=root
MYSQL_DATABASE=events_db
MYSQL_USER=app
MYSQL_PASSWORD=app
```

All application configuration (database, Kafka, Redis) is managed using environment variables.

### Start the System
```bash
docker compose up -d --build
```


This command starts all required services:

ZooKeeper

Kafka

Redis

MySQL

API service

Consumer service

### API Endpoints
POST /api/events

Ingests a new sensor event and publishes it to Kafka.

# Request body

{
  "sensorId": "sensor-1",
  "timestamp": "2026-01-23T10:00:00Z",
  "value": 25,
  "type": "temperature"
}


# Response

201 Created on success

400 / 422 for invalid payloads

Example:

curl -X POST http://localhost:8080/api/events \
  -H "Content-Type: application/json" \
  -d "{\"sensorId\":\"sensor-1\",\"timestamp\":\"2026-01-23T10:00:00Z\",\"value\":25,\"type\":\"temperature\"}"

# GET /api/events/{sensorId}

Returns all processed events for a given sensor, ordered by timestamp.

Data is cached in Redis to improve performance

Returns 404 Not Found if no events exist

Example:
curl http://localhost:8080/api/events/sensor-1



# GET /api/events/summary/{sensorId}

Returns summary statistics (average, minimum, maximum) for events received in the last 24 hours.

Response is cached in Redis for a short duration

Returns 404 Not Found if no data exists

Example:

curl http://localhost:8080/api/events/summary/sensor-1


# Caching Strategy

Event lists are cached for approximately 10 minutes

Summary responses are cached for approximately 2 minutes

Cache entries are invalidated by the Kafka consumer whenever new events for a sensor are processed

This ensures fast reads while preventing stale data.

# Kafka Processing and Idempotency

Events are produced to the sensor_readings Kafka topic

The consumer processes messages asynchronously

Each processed event uses a UUID as a primary key

Duplicate Kafka messages are safely ignored using database constraints

This makes the system resilient to Kafka re-delivery and consumer restarts.

# Error Handling and Resilience

API service retries database connections during startup

Kafka and database failures are logged without crashing services

Consumer handles duplicate and invalid messages gracefully



# Testing

The project includes both unit and integration tests.

Run tests inside the API container:

docker compose exec api-service pytest

Expected output:

8 passed

# Tests cover:

Payload validation

API behavior

Database persistence

Redis caching logic



# Event Simulation

The project includes a simulation script that generates multiple sensor events automatically.

Run the script from the project root:

python scripts/simulate_events.py

The script sends random sensor events to the API endpoint:

POST /api/events

This allows testing the full pipeline:

Client → API → Kafka → Consumer → MySQL → Redis Cache

# Notes

All secrets and configuration values are environment-based

Services are loosely coupled using Kafka

Designed with scalability, fault tolerance, and performance in mind

# Author

Developed as part of a backend system design and distributed processing challenge.



