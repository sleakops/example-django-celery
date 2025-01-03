# Generated by Django 4.2 on 2024-01-13 20:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('client', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('source', models.CharField(choices=[('reddit', 'Reddit'), ('twitter', 'Twitter'), ('facebook', 'Facebook'), ('instagram', 'Instagram'), ('tumblr', 'Tumblr'), ('pinterest', 'Pinterest'), ('youtube', 'YouTube'), ('vimeo', 'Vimeo'), ('flickr', 'Flickr'), ('soundcloud', 'SoundCloud'), ('spotify', 'Spotify'), ('twitch', 'Twitch'), ('tiktok', 'TikTok')], max_length=50)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.client')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField()),
                ('username', models.CharField(max_length=50)),
                ('publication_date', models.DateTimeField(null=True)),
                ('likes', models.IntegerField(null=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='post.post')),
            ],
        ),
    ]
