# Cookiecutter ML flask serving

_Project structure for serving a ML model using flask_


#### [Project homepage](https://github.com/ShilpaGopal/cookiecutter-ml-flask-serving/)


### Requirements to use the cookiecutter template:
-----------
 - Python 2.7 or 3.5
 - [Cookiecutter Python package](http://cookiecutter.readthedocs.org/en/latest/installation.html) >= 1.4.0: This can be installed with pip by or conda depending on how you manage your Python packages:

``` bash
$ pip install cookiecutter
```

### To start a new project, run:
------------

    cookiecutter https://github.com/ShilpaGopal/cookiecutter-ml-flask-serving

### The resulting directory structure
------------

The directory structure of your new project looks like this: 

```
├── LICENSE
├── Makefile           <- Makefile with commands like `make serve` or `make request`
├── README.md          <- The top-level README for developers using this project.
├── app 
│   ├── api            <- Manages service response format for success and failure cases with custom exceptions
│   ├── config         <- Service configs in three category MODEL_CONFIG, LOGGER_CONFIG, SERVICE_CONFIG
│   ├── constants      <- Global service constants declaration
│   ├── handlers       <- Handles api requests layer with custom responses
│   ├── logger         <- Custom service log implementation
│   ├── provider       <- Manages service core logic core loading the model, pre/post processing and prediction
│   ├── app.py         <- Service routes declaration
│   ├── gunicorn.conf.py <- Configurations for gunicorn webserver gateway
│   └── wsgi.py        <- Entry point for the service
│
├── data
│   └── model          <- A folder to keep model weights file
│
├── build              
│   └── docker
│       ├── Dockerfile <- Docker build file to containerize the service
│       └── env_dev.env<- Service configs for the container
│
├── requirements       <- Manages project dependencies
│   ├── common.txt     <- Common dependencies across all the env
│   ├── dev.txt        <- Dev dependencies + Common dependencies
│   └── prod.txt       <- Prod dependencies + Common dependencies
│
├── log                <- Service log
│
├── tests              <- Service tests
│   └── data           <- Tests data
│
│── bootstrap.sh       <- Gunicorn wsgi entry point
└── requirements.txt   <- Mirrors prod
```