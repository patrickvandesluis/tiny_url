from django.db import models


class Link(models.Model):
    link = models.CharField(max_length=5000)
    short = models.CharField(max_length=200, unique=True)
    ip = models.CharField(max_length=40, blank=True)
    times_used = models.IntegerField(blank=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return f"Short Url for: {self.link} is {self.short}"
