from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel
from typing import List, Optional
from collections import defaultdict, deque
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


origins = [
    "https://node-editor-lyart.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request body schema
class Position(BaseModel):
    x: float
    y: float

class Node(BaseModel):
    id: str
    type: str
    position: Position
    data: dict

class Edge(BaseModel):
    id: str
    source: str
    target: str
    sourceHandle: Optional[str] = None
    targetHandle: Optional[str] = None

class PipelineData(BaseModel):
    nodes: List[Node]
    edges: List[Edge]

@app.get("/")
def read_root():
    return {"Ping": "Pong"}

@app.post("/pipelines/parse")
def parse_pipeline(pipeline: PipelineData):
    nodes = pipeline.nodes
    edges = pipeline.edges

    num_nodes = len(nodes)
    num_edges = len(edges)

    # Build graph and in-degree
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    for node in nodes:
        in_degree[node.id] = 0

    for edge in edges:
        graph[edge.source].append(edge.target)
        in_degree[edge.target] += 1

    # Kahn's algorithm to check for DAG
    queue = deque([node_id for node_id in in_degree if in_degree[node_id] == 0])
    processed_count = 0

    while queue:
        current = queue.popleft()
        processed_count += 1
        for neighbor in graph[current]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    is_dag = processed_count == num_nodes
    message = "Pipeline is valid and ready for execution." if is_dag else "Pipeline contains cycles."

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "is_dag": is_dag,
        "message": message
    }
