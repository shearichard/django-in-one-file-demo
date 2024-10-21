'''
A example of using ninjadjango to provide a 'one-file' Django project
which exposes an API.

The API allows for items on 'to-do' list to be maintained and reviewed
by the consumer of the API
'''
import os

from django.db import models
from nanodjango import Django

app = Django(
    SECRET_KEY=os.environ["DJANGO_SECRET_KEY"],
)


class ToDo(models.Model):
    '''
    A task to be done
    '''
    task = models.CharField(max_length=100)
    is_completed = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = "To Do"
        verbose_name_plural = "To Do"

    def __str__(self):
        return str(self.name)
