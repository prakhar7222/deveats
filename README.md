# DevEats — Developer Application Package

Developer-provided source package for Project 5.

Components:
- frontend: static HTML/CSS/JavaScript
- backend: Flask REST API
- database: PostgreSQL schema and seed data

The backend listens on port 5000 and reads DB_HOST, DB_PORT, DB_NAME, DB_USER and DB_PASSWORD.

API:
GET /api/health
GET /api/restaurants
GET /api/restaurants/<id>
GET /api/restaurants/<id>/menu
GET /api/orders/<id>
POST /api/orders

Dockerfiles, Docker Compose, Jenkinsfile and production Nginx configuration are intentionally excluded. Those are the DevOps tasks.
