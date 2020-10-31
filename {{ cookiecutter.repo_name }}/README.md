OCR
---------------
### Dev Setup

Prerequisites:

> Python 3.8

> Miniconda/Anaconda

* Create a virtual environment for Python version 3.8

```
conda create -n <SERVICE-NAME> python=3.8.5
conda activate <SERVICE-NAME>
conda install pip
```

### The resulting directory structure
------------

Template also contains sample Service request validation for below contract
```
Request:
--------
curl --location --request POST 'http://127.0.0.1:8000/<SERVICE-PREFIX>/v1/predict' \
--header 'X-Request-ID: 1a8a3ca3-8a45-4cae-b165-43c962241e1a' \
--header 'Content-Type: application/json' \
--data-raw '{
    "roi": "base64encoded(bytearray(image))"}'

Response:
--------
{
    "predictions": ""
}
```

The directory structure of your new project looks like this: 

```
├── LICENSE
├── Makefile           <- Makefile with commands like `make serve` or `make request`
├── README.md          <- The top-level README for developers using this project.
├── app 
│   ├── api            <- Manages service response format for success and failure cases with custom exceptions
│   ├── config         <- Service configs in three categories MODEL_CONFIG, LOGGER_CONFIG, SERVICE_CONFIG
│   ├── constants      <- Global service constants declaration
│   ├── handlers       <- Handles api requests layer with custom responses
│   ├── logger         <- Custom service log implementation
│   ├── provider       <- Manages service core logic core loading the model, pre/post-processing, and prediction
│   ├── app.py         <- Service routes declaration
│   ├── gunicorn.conf.py <- Configurations for gunicorn web server gateway
│   └── wsgi.py        <- An entry point for the service
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

Replace listed variables across the project
```
<MODEL-NAME> # in app/constants/constants.py
<SERVICE-NAME> # Project wide search and replace
<SERVICE-SHORT-NAME> # in app/constants/constants.py
<SERVICE-PREFIX> # in app.py and Makefile
```
### Logging format
----------------

INFO log
```
{"timestamp": "2020-09-09T15:24:41.125863Z", 
"level": "INFO", 
"message": "prediction successful", 
"event": "<SERVICE-SHORT-NAME>PredictSuccessEvent", 
"status_code": 200, 
"req_id": "a121b432-ed27-11ea-adc1-0242ac120002", 
"res": ""}
```
ERROR log
```
{"timestamp": "2020-09-09T13:53:20.724995Z", 
"level": "ERROR", 
"message": "error occurred while processing the prediction", 
"event": "<SERVICE-SHORT-NAME>PreprocessErrorEvent", 
"status_code": 500, 
"req_id": "a121b432-ed27-11ea-adc1-0242ac120002", 
"error": "Internal server error", 
"nested_error": "<Stack Trace>"}
```