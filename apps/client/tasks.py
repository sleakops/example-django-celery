from celery import shared_task

from .models import Client
from apps.post.models import Post


@shared_task
def collect_post_by_client(client_id):
    client = Client.objects.get(id=client_id)
    print(f'Request: {client.username}')

    for i in range(1, 200):
        Post.objects.create(
            client=client,
            source="twitter",
            description=f"Lorem {i}"
        )