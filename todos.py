'''
A example of using ninjadjango to provide a 'one-file' Django project
which exposes an API.

The API allows for items on 'to-do' list to be maintained and reviewed
by the consumer of the API
'''
import os
from datetime import date
from datetime import datetime
import json

from django.db import models
from django.http import HttpResponse
from django.template import loader
from django.contrib.staticfiles.views import serve
from django.forms.models import model_to_dict
from django.http import JsonResponse, Http404
from django.views.decorators.http import require_http_methods
from django.utils.dateparse import parse_datetime
from django.utils import timezone

#
# from pydantic import (BaseModel, EmailStr, Field, field_validator, model_validator,)   # noqa: E401
from pydantic import (Field)

#
from nanodjango import Django
#
API_VERSION = "v1"
API_TODOS_URL_BASE = "todos"
#
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
# Views - todos
# #############################################################################
@app.route("/")
def todos(request):
    todos_list = ToDo.objects.order_by("should_be_completed_by_date")
    template = loader.get_template("todos/index.html")
    context = {
        "todos_list": todos_list,
    }
    return HttpResponse(template.render(context, request))

@app.route("/about")
def about(request):
    template = loader.get_template("todos/about.html")
    context={}
    return HttpResponse(template.render(context, request))

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
        output.append({ "id": t.id,
                        "task": t.task,
                        "is_completed": t.is_completed,
                        "should_be_completed_by_date": t.should_be_completed_by_date,
                        "created": t.created})
    #
    return {"data": output}


@app.api.post(f"{API_VERSION}/{API_TODOS_URL_BASE}/")
def api_create_todos(request, data: ToDoIn):
    '''
    For ease of reference here's a curl command to exercise this end point.

    curl -X POST http://localhost:8000/api/v1/todos/ -H "Content-Type: application/json" -d "{\"task\": \"clean-a $(date +%s)\", \"should_be_completed_by_date\": \"2024-12-01\"}"

    '''
    todo = ToDo(task=data.task,
                should_be_completed_by_date=data.should_be_completed_by_date
                )
    #
    todo.save()
    #Now get ready to return a representation of the newly created object
    todo.refresh_from_db()
    #The created/last_updated attributes are not included by model_to_dict
    todo_dict = model_to_dict(todo)
    #The 'DateTimeEncoder' ensures that datetimes are encoded properly in the JSON
    todo_json = json.dumps(todo_dict, cls=DateTimeEncoder)
    #
    return {"data": todo_json}

@app.api.patch(f"{API_VERSION}/{API_TODOS_URL_BASE}/")
def api_update_todo(request, data: ToDoIn):
    try:
        # Parse the incoming JSON data
        data = json.loads(request.body)
        todo_id = data.get("id")
        
        if not todo_id:
            return JsonResponse({"error": "ID is required"}, status=400)
        
        # Fetch the existing ToDo object
        try:
            todo = ToDo.objects.get(id=todo_id)
        except ToDo.DoesNotExist:
            raise Http404("ToDo item not found")
        
        # Update the fields based on the provided JSON data
        if "task" in data:
            todo.task = data["task"]
        if "is_completed" in data:
            todo.is_completed = data["is_completed"]
        if "should_be_completed_by_date" in data:
            # Parse the incoming datetime string
            should_be_completed_by_date = parse_datetime(data["should_be_completed_by_date"])
            
            if should_be_completed_by_date is None:
                return JsonResponse({"error": "Invalid datetime format for 'should_be_completed_by_date'"}, status=400)
            
            # Check if the datetime is naive
            if timezone.is_naive(should_be_completed_by_date):
                return JsonResponse({"error": "Naive datetime provided; time zone information is required."}, status=400)
            
            # If aware, assign the value
            todo.should_be_completed_by_date = should_be_completed_by_date
        
        # Save the changes to the database
        todo.save()
        
        # Return a success response
        updated_data = {
            "id": todo.id,
            "task": todo.task,
            "is_completed": todo.is_completed,
            "should_be_completed_by_date": todo.should_be_completed_by_date,
            "created": todo.created,
            "last_updated": todo.last_updated,
        }
        return JsonResponse({"data": updated_data})
    
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


# #############################################################################
# Utilities
# #############################################################################
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # Converts to ISO 8601 format
        return super().default(obj)

# Assuming `instance` is an instance of the Foo model

# #############################################################################
# Using app.run avoids having to invoke the script with 'nanojango'
# #############################################################################
if __name__ == "__main__":
    app.run()
