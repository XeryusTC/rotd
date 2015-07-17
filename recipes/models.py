from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=64, blank=False, default='')

    def __str__(self):
        return self.name
