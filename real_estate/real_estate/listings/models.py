from django.contrib.auth.models import User
from django.db import models

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='listings/')
    square_meters = models.PositiveIntegerField()

    def __str__(self):
        return self.title
