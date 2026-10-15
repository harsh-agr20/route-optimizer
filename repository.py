from network.models import Node, Edge, RouteHistory

def create_node(name):
    return Node.objects.create(name=name)

def get_node(name):
    return Node.objects.filter(name=name).first()

def get_nodes():
    return list(Node.objects.values("id", "name"))

def delete_node(node_id):
    deleted, _ = Node.objects.filter(id=node_id).delete()
    return deleted > 0

def create_edge(source, destination, latency):
    return Edge.objects.create(source=source, destination=destination, latency=latency)

def get_edges():
    return list(Edge.objects.values("id", "source__name", "destination__name", "latency"))

def get_all_edges():
    return Edge.objects.values_list("source_id", "destination_id", "latency")

def delete_edge(edge_id):
    deleted, _ = Edge.objects.filter(id=edge_id).delete()
    return deleted > 0

def get_node_names(node_ids):
    return dict(Node.objects.filter(id__in=node_ids).values_list("id", "name"))

def save_route(source, destination, path, latency):
    RouteHistory.objects.create(source=source, destination=destination, path=path, total_latency=latency)

def get_history():
    return list(RouteHistory.objects.order_by("-created_at").values(
        "source", "destination", "path", "total_latency", "created_at"
    )[:100])
