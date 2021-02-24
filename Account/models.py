from django.db import models
from django.contrib.auth.models import User

class Follow(models.Model):
    user = models.ForeignKey(User, related_name = "user", on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name = "following", on_delete=models.CASCADE)
    