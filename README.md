# Django in one file Demo
![Screenshot of application banner.](doco_assets/README.md-assets/splash-screen.png)

## Overview
This project explores the ideas of having an entire [Django](https://www.djangoproject.com/) project in a single file, internally the result will be a Django project but externally it will be more like a [Flask](https://flask.palletsprojects.com/en/3.0.x/) project. 



## What?

When looking at Python web frameworks it's natural to think first of [Flask](https://flask.palletsprojects.com/en/3.0.x/Flask) and [Django](https://www.djangoproject.com/), there are others but Flask and Django are the leaders.

One of the more obvious differences between Flask and Django is that Flask projects don't have an expected file structure, in fact it's not unusual for a Flask project to consist of single file. By contrast, in Django, there's a well established convention on which files do what and where they are located.

This project is all about trying out the possibilities of turning that Django convention on its head, and putting everything into a single file.

### Why?

I'm interested in this alternative approach for two reasons.

*   I'm interested in the benefits that might accrue for teaching and demonstration. I think it's likely that when teaching, or demonstrating, Django having all the processing in a single file allows the learner to get a quick start to understanding which bits do what, and why.
*   Secondarily I am interested in discovering whether 'real' Django apps might be built this way. In the past I've turned to Flask when the task at hand seems 'too simple' for Django and I think it's worth investigating whether for some use cases 'Single File Django' might be a way of achieving the simplicity of having only a single file while enjoying the 'batteries included' benefits of Django.

### How?

This project is based on the excellent and interesting [nanadjango project](https://github.com/radiac/nanodjango). Nanodjango is being developed by Richard Terry who is responsible for a number of other interesting projects which may be seen on his [Github page](https://github.com/radiac)

## Use of Environmental Variables
Secrets are kept in environmental variables. 

The use of the [direnv utility](https://direnv.net), in conjunction with a .envrc file, results in the environmental variables being autoloaded when the current directory is the project root (or child directories of that). 

The .envrc file is not committed to the repos but the .envrc_TEMPLATE file, which is committed, provides guidance on what should appear in the .envrc.

## Regenerating Django Secret Key
```
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

# Static Analysis
Static code analysis is done using [flake8](https://flake8.pycqa.org/en/latest/#).

## Executing the analysis

A `.flake8` configuration file controls how flake8 behaves, amongst other thing this configuration file allows some warnings to be suppressed and this is sometimes an appropriate action.

Execute the following from the project root directory.

```default
$ flake8 ./
```

