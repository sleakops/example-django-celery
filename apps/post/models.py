from django.db import models


SOURCES = (
    ('reddit', 'Reddit'),
    ('twitter', 'Twitter'),
    ('facebook', 'Facebook'),
    ('instagram', 'Instagram'),
    ('tumblr', 'Tumblr'),
    ('pinterest', 'Pinterest'),
    ('youtube', 'YouTube'),
    ('vimeo', 'Vimeo'),
    ('flickr', 'Flickr'),
    ('soundcloud', 'SoundCloud'),
    ('spotify', 'Spotify'),
    ('twitch', 'Twitch'),
    ('tiktok', 'TikTok'),
)


class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    client = models.ForeignKey('client.Client', on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True, default="", max_length=600)
    
    source = models.CharField(max_length=50, choices=SOURCES)


class Comment(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    username = models.CharField(max_length=50)
    publication_date = models.DateTimeField(null=True)
    likes = models.IntegerField(null=True)
