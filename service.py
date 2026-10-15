import heapq
import math
from collections import defaultdict
import repository as repo

def add_node(name):
    name = name.strip()
    if not name:
        raise ValueError("Node name cannot be empty")
    if repo.get_node(name):
        raise ValueError("Node already exists")
    return repo.create_node(name)

def add_edge(source, destination, latency):
    src = repo.get_node(source)
    dst = repo.get_node(destination)
    if not src or not dst:
        raise ValueError("Source or destination not found")
    if src.id == dst.id:
        raise ValueError("Self connection not allowed")
    latency = float(latency)
    if not math.isfinite(latency) or latency <= 0:
        raise ValueError("Latency must be positive and finite")
    return repo.create_edge(src, dst, latency)

def find_shortest_path(source, destination):
    src = repo.get_node(source)
    dst = repo.get_node(destination)
    if not src or not dst:
        raise ValueError("Source or destination not found")
    graph = defaultdict(list)
    for u, v, latency in repo.get_all_edges():
        graph[u].append((v, latency))
    heap = [(0, src.id)]
    distance = {src.id: 0}
    parent = {}
    while heap:
        cost, node = heapq.heappop(heap)
        if cost > distance[node]:
            continue
        if node == dst.id:
            break
        for neighbor, weight in graph[node]:
            new_cost = cost + weight
            if new_cost < distance.get(neighbor, float("inf")):
                distance[neighbor] = new_cost
                parent[neighbor] = node
                heapq.heappush(heap, (new_cost, neighbor))
    if dst.id not in distance:
        raise ValueError("No route found")
    path_ids = []
    current = dst.id
    while current != src.id:
        path_ids.append(current)
        current = parent[current]
    path_ids.append(src.id)
    path_ids.reverse()
    names = repo.get_node_names(path_ids)
    path = [names[node_id] for node_id in path_ids]
    total = distance[dst.id]
    repo.save_route(source, destination, path, total)
    return {"path": path, "total_latency": total}
