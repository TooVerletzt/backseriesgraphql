from django.conf import settings
from django.db import models

class Post(models.Model):
    title      = models.CharField(max_length=200)
    content    = models.TextField()
    game       = models.CharField(max_length=100)
    image      = models.ImageField(upload_to='post_images/', blank=True, null=True)
    posted_by  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.posted_by}"

class Vote(models.Model):
    post       = models.ForeignKey(Post, related_name='votes', on_delete=models.CASCADE)
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

class Comment(models.Model):
    post       = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content    = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Reaction(models.Model):
    REACTION_CHOICES = [
        ('LIKE',  '👍'),
        ('LOVE',  '❤️'),
        ('HAHA',  '😂'),
        ('WOW',   '😮'),
        ('SAD',   '😢'),
        ('ANGRY', '😡'),
    ]
    post          = models.ForeignKey(Post, related_name='reactions', on_delete=models.CASCADE)
    user          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reaction_type = models.CharField(max_length=10, choices=REACTION_CHOICES)
    created_at    = models.DateTimeField(auto_now_add=True)
