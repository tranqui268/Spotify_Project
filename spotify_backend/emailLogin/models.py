# models.py
from django.db import models
from django.utils import timezone
import uuid

class EmailLoginCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(default=timezone.now)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} - {self.code}"

