from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=64, blank=False, default='',
            unique=True)
    description = models.TextField(default='')
    add_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
