from django.db import models


class Link(models.Model):
    link = models.CharField(max_length=5000)
    short = models.CharField(max_length=200)
    ip = models.CharField(max_length=40, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
            return f"Short Url for: {self.link} is {self.short}"

