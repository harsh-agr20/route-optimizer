import json
from django.urls import path
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
import service
import repository as repo

def response(data, status=200):
    return JsonResponse(data, status=status, safe=False)

def read_body(request):
    try:
        data = json.loads(request.body)
        if not isinstance(data, dict):
            raise ValueError("JSON object required")
        return data
    except (json.JSONDecodeError, UnicodeDecodeError):
        raise ValueError("Invalid JSON")

@csrf_exempt
def nodes(request):
    try:
        if request.method == "GET":
            return response(repo.get_nodes())
        if request.method == "POST":
            data = read_body(request)
            node = service.add_node(data["name"])
            return response({"id": node.id, "name": node.name}, 201)
        return response({"error": "Method not allowed"}, 405)
    except (ValueError, KeyError, TypeError, AttributeError, IntegrityError) as e:
        return response({"error": str(e)}, 400)

@csrf_exempt
def node_detail(request, node_id):
    if request.method != "DELETE":
        return response({"error": "Method not allowed"}, 405)
    if repo.delete_node(node_id):
        return response({"message": "Node deleted"})
    return response({"error": "Node not found"}, 404)

@csrf_exempt
def edges(request):
    try:
        if request.method == "GET":
            return response(repo.get_edges())
        if request.method == "POST":
            data = read_body(request)
            edge = service.add_edge(data["source"], data["destination"], data["latency"])
            return response({"id": edge.id, "message": "Edge created"}, 201)
        return response({"error": "Method not allowed"}, 405)
    except (ValueError, KeyError, TypeError, IntegrityError) as e:
        return response({"error": str(e)}, 400)

@csrf_exempt
def edge_detail(request, edge_id):
    if request.method != "DELETE":
        return response({"error": "Method not allowed"}, 405)
    if repo.delete_edge(edge_id):
        return response({"message": "Edge deleted"})
    return response({"error": "Edge not found"}, 404)

@csrf_exempt
def shortest_route(request):
    if request.method != "POST":
        return response({"error": "Method not allowed"}, 405)
    try:
        data = read_body(request)
        return response(service.find_shortest_path(data["source"], data["destination"]))
    except (ValueError, KeyError) as e:
        return response({"error": str(e)}, 400)

def route_history(request):
    if request.method != "GET":
        return response({"error": "Method not allowed"}, 405)
    return response(repo.get_history())

urlpatterns = [
    path("nodes", nodes),
    path("nodes/<int:node_id>", node_detail),
    path("edges", edges),
    path("edges/<int:edge_id>", edge_detail),
    path("routes/shortest", shortest_route),
    path("routes/history", route_history),
]
