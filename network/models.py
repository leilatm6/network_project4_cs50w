from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class NetPost(models.Model):
    text = models.TextField(blank=False)
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="posts")
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "user": self.user.username,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }
