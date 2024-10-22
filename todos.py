'''
A example of using ninjadjango to provide a 'one-file' Django project
which exposes an API.

The API allows for items on 'to-do' list to be maintained and reviewed
by the consumer of the API
'''
import os
import pprint
from datetime import datetime
from datetime import date

from django.db import models
from django.http import HttpResponse
from django.template import loader
#
from pydantic import (
  BaseModel,
  EmailStr,
  Field,
  field_validator,
  model_validator,
)
from nanodjango import Django

API_VERSION = "v1"
API_TODOS_URL_BASE = "todos"

app = Django(
    ADMIN_URL="admin/",
    SECRET_KEY=os.environ["DJANGO_SECRET_KEY"],
    SQLITE_DATABASE="todos_db.sqlite3"
)


# #############################################################################
# Models
# #############################################################################
@app.admin
class ToDo(models.Model):
    '''
    A task to be done
    '''
    task = models.CharField(max_length=100)
    is_completed = models.BooleanField(default=False)
    should_be_completed_by_date = models.DateTimeField(null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    last_updated = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        verbose_name = "To Do"
        verbose_name_plural = "To Do"

    def __str__(self):
        return str(self.task)


# #############################################################################
# Views
# #############################################################################
@app.route("/")
def todos(request):
    todos_list = ToDo.objects.order_by("-should_be_completed_by_date")
    template = loader.get_template("todos/index.html")
    context = {
        "todos_list": todos_list,
    }
    return HttpResponse(template.render(context, request))
    '''
    output = [] 
    if todos:
        for t in todos:
          output.append(t.task)
    else:
        output = "There are no todos"
    #
    return output
    '''


# #############################################################################
# Schema
# #############################################################################
class ToDoIn(app.ninja.Schema):
    task: str
    should_be_completed_by_date: date = Field(alias="should_be_completed_by_date", repr=False, frozen=True) 


# #############################################################################
# API End Points
# #############################################################################
@app.api.get(f"{API_VERSION}/{API_TODOS_URL_BASE}/")
def api_todos(request):
    '''
    For ease of reference here's a curl command to exercise this end point.

    curl GET http://localhost:8000/api/v1/todos/ 

    '''
    output = []
    todos = ToDo.objects.order_by("-should_be_completed_by_date")
    for t in todos:
        output.append({
                        "task": t.task, 
                        "is_completed": t.is_completed,
                        "should_be_completed_by_date": t.should_be_completed_by_date,
                        "created": t.created
                        })
    #
    return {"data": output}


@app.api.post(f"{API_VERSION}/{API_TODOS_URL_BASE}/")
def api_create_todos(request, data: ToDoIn):
    '''
    For ease of reference here's a curl command to exercise this end point.

    curl -X POST http://localhost:8000/api/v1/todos/ -H "Content-Type: application/json" -d "{\"task\": \"clean-a $(date +%s)\", \"should_be_completed_by_date\": \"2024-12-01\"}"

    '''
    todo = ToDo(  task=data.task, 
          should_be_completed_by_date=data.should_be_completed_by_date)
    todo.save() 
    return {"data": ""}

# #############################################################################
# Using app.run avoids having to invoke the script with 'nanojango'
# #############################################################################
if __name__ == "__main__":
    app.run()


'''

# #############################################################################
# Models
# #############################################################################
@api.post("/users/")
def create_user(request, data: UserIn):
    user = User(username=data.username) # User is django auth.User
    user.set_password(data.password)
    user.save()
    # ... return ?














from django.http import HttpResponse

from .models import Question


def index(request):
        latest_question_list = Question.objects.order_by("-pub_date")[:5]
            output = ", ".join([q.question_text for q in latest_question_list])
                return HttpResponse(output)


            # Leave the rest of the views (detail, results, vote) unchanged
'''

'''
def parse_datetime(date_string):
    if not date_string:  # Check if the string is empty
        return None
    
    try:
        # Parse the string to a datetime object
        return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
    except ValueError as e:
        # Raise an exception if the date_string is not a valid date/time
        raise ValueError(f"Invalid date/time format: {date_string}") from e

'''
'''
# Examples of usage
parsed_datetime = parse_datetime("2024-11-23T02:46:19")
print(parsed_datetime)

parsed_datetime_none = parse_datetime("")  # Should return None
print(parsed_datetime_none)

# This will raise a ValueError with a message about the invalid format
parse_datetime("invalid-date")

'''
'''
from django.http import HttpResponse
from django.template import loader

from .models import Question


def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    template = loader.get_template("polls/index.html")
    context = {
        "latest_question_list": latest_question_list,
    }
    return HttpResponse(template.render(context, request))
'''
