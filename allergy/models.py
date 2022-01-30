from django.db import models
from users.models import User

# Create your models here.
class Allergy(models.Model):
    milk = models.BooleanField(default=False)
    egg = models.BooleanField(default=False)
    peach = models.BooleanField(default=False)
    bean = models.BooleanField(default=False)
    pork = models.BooleanField(default=False)
    beef = models.BooleanField(default=False)

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="allergy")