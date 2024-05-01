from django.db import models

# Create your models here.

class bill(models.Model):
    billname = models.TextField()
    text = models.TextField()
    def __str__(self) -> str:
        return self.billname