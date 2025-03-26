from django.db import models

from accounts.models import CustomUser

class ChatMessage(models.Model):
    """ Chat Message Model """
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sent_message')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='received_message')
    message = models.TextField()
    timestap = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
