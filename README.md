# Full Stack Node Editor – Backend

This is the **backend service** for the **Full Stack Node Editor** project.  
It is built with [FastAPI](https://fastapi.tiangolo.com/) and provides APIs for validating and processing node-based pipelines.

## 🚀 Features

- **FastAPI** server with CORS enabled (frontend at `http://localhost:5173`).
- **Pipeline validation** endpoint:
  - Accepts a list of nodes and edges.
  - Runs a DAG (Directed Acyclic Graph) check using **Kahn’s Algorithm**.
  - Detects cycles in the pipeline graph.
- Ready to integrate with the frontend editor.

## 📦 Requirements

- Python **3.9+**
- Dependencies listed in `requirements.txt`

Install them:

```bash
pip install -r requirements.txt
```

## ▶️ Run the Server

Start the backend locally with:

```bash
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

## 📡 API Endpoints

### `GET /`

Simple health check.

**Response**

```json
{ "Ping": "Pong" }
```

### `POST /pipelines/parse`

Validate a pipeline by checking if it is a **valid DAG**.

**Request Body**

```json
{
  "nodes": [
    { "id": "1", "type": "Start", "position": { "x": 0, "y": 0 }, "data": {} },
    {
      "id": "2",
      "type": "Task",
      "position": { "x": 100, "y": 100 },
      "data": {}
    }
  ],
  "edges": [{ "id": "e1-2", "source": "1", "target": "2" }]
}
```

**Response**

```json
{
  "num_nodes": 2,
  "num_edges": 1,
  "is_dag": true,
  "message": "Pipeline is valid and ready for execution."
}
```

---

## 🛠 Development Notes

- CORS allows requests from the frontend (`http://localhost:5173`).
- Modify `origins` in `main.py` to allow other clients.
- Future extension: Add execution engine for pipelines.
