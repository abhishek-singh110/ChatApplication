from django.db import models
from django.contrib.auth.models import User


# Model to save the interestMessage 
class InterestMessage(models.Model):
    sender = models.ForeignKey(User, related_name='interest_sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='interest_received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False)
    rejected = models.BooleanField(default=False)

# Model to save the ChatMessage
class ChatMessage(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
