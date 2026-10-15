from django.db import models

class Node(models.Model):
    name = models.CharField(max_length=100, unique=True)

class Edge(models.Model):
    source = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="outgoing")
    destination = models.ForeignKey(Node, on_delete=models.CASCADE, related_name="incoming")
    latency = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["source", "destination"], name="unique_edge")
        ]

class RouteHistory(models.Model):
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    path = models.JSONField()
    total_latency = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
