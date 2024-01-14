from django.db import models

# Create your models here.

class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    deadline = models.DateTimeField()
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.title
