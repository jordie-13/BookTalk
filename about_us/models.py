from django.db import models

class About_Us(models.Model):
    title = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=1000)

    def __str__(self):
        return self.title