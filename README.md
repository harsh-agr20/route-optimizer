# Simple Django + MySQL Route Optimizer

Four main layers: `main.py` (entry point), `handler.py` (API routes), `service.py` (validation and Dijkstra), and `repository.py` (database operations). Django models live in `network/models.py`.

## Setup

1. Create MySQL database: `CREATE DATABASE route_optimizer;`
2. Install dependencies: `pip install -r requirements.txt`
3. Set `MYSQL_DATABASE`, `MYSQL_USER`, `MYSQL_PASSWORD`, `MYSQL_HOST`, `MYSQL_PORT` environment variables, or edit `settings.py` for local development.
4. Run `python main.py makemigrations network`
5. Run `python main.py migrate`
6. Run `python main.py`

## Endpoints

- `POST /nodes` JSON `{"name":"A"}`
- `GET /nodes`
- `DELETE /nodes/1`
- `POST /edges` JSON `{"source":"A","destination":"B","latency":10}`
- `GET /edges`
- `DELETE /edges/1`
- `POST /routes/shortest` JSON `{"source":"A","destination":"B"}`
- `GET /routes/history`

Edges are directed. The shortest route is computed with Dijkstra's algorithm and a min-heap. This is a learning/assignment example, not a production-hardened service. CSRF is disabled for the demo endpoints; add authentication and security controls before deployment.
