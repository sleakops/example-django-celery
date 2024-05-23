from django.db import models


class Client(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(max_length=50)
    full_name = models.CharField(max_length=150)
    text = models.TextField(blank=True, null=True, default="")
    
    def __str__(self) -> str:
        return f"{self.id} - {self.username}"