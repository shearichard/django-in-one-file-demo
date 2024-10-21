# Django in one file Demo
This project explores the ideas of having an entire [Django](https://www.djangoproject.com/) project in a single file, internally the result will be a Django project but externally it will be more like a [Flask](https://flask.palletsprojects.com/en/3.0.x/) project. 

It's initially based around [this repos](https://github.com/radiac/nanodjango).

## Use of Environmental Variables
Secrets are kept in environmental variables. 

The use of the [direnv utility](https://direnv.net), in conjunction with a .envrc file, results in the environmental variables being autoloaded when the current directory is the project root (or child directories of that). 

The .envrc file is not committed to the repos but the .envrc_TEMPLATE file, which is committed, provides guidance on what should appear in the .envrc.

## Regenerating Django Secret Key
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

