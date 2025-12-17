from django.db import models

# Create your models here.
class Player(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    number = models.IntegerField()
    team = models.CharField(max_length=100)
    age = models.IntegerField()
    height = models.DecimalField(max_digits=4, decimal_places=3, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_starting = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} - {self.position}"
