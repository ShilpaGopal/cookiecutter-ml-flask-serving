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
* Install required packages

Packages are managed as per below structure.

    
    |--requirements
    |   |-- common.txt -> Contains requirements common to all environments
    |   |-- dev.txt -> Contains dev-specific requirements along with coomon packages
    |   |-- prod.txt -> Contains requirements for prod
    |--requirements.txt --> Mirrors prod
```
pip install -r requirements/dev.txt
```