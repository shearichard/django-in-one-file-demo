'''
A example of using ninjadjango to provide a 'one-file' Django project
which exposes an API.

The API allows for items on 'to-do' list to be maintained and reviewed
by the consumer of the API
'''
import os

from django.db import models
from nanodjango import Django
from typing import Optional
from ninja import Schema

API_VERSION = "v1"
API_TODOS_URL_BASE = "todos"

app = Django(
    SECRET_KEY=os.environ["DJANGO_SECRET_KEY"],
    SQLITE_DATABASE="todos_db.sqlite3"
)


# #############################################################################
# Models
# #############################################################################
class ToDo(models.Model):
    '''
    A task to be done
    '''
    task = models.CharField(max_length=100)
    is_completed = models.BooleanField()
    should_be_completed_by_date = models.DateTimeField(null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = "To Do"
        verbose_name_plural = "To Do"

    def __str__(self):
        return str(self.name)


# #############################################################################
# Views
# #############################################################################
@app.route("/")
def todos(request):
    todos = ToDo.objects.order_by("-should_be_completed_by_date")
    output = ""
    if todos:
        output = "There are some todos"
    else:
        output = "There are no todos"
    #
    return output


# #############################################################################
# API End Points
# #############################################################################
@app.api.get(f"{API_TODOS_URL_BASE}/{API_VERSION}/")
def api_todos(request):
    output = []
    todos = ToDo.objects.order_by("-should_be_completed_by_date")
    for t in todos:
        output.append({"task": t.taskr})
    #
    return {"data": output}


# #############################################################################
# Using app.run avoids having to invoke the script with 'nanojango'
# #############################################################################
if __name__ == "__main__":
    app.run()


'''
from django.http import HttpResponse

from .models import Question


def index(request):
        latest_question_list = Question.objects.order_by("-pub_date")[:5]
            output = ", ".join([q.question_text for q in latest_question_list])
                return HttpResponse(output)


            # Leave the rest of the views (detail, results, vote) unchanged
'''
