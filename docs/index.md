Python:

<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

CI/CD Pipeline:

[![codecov](https://codecov.io/gh/devsetgo/pip-checker/branch/master/graph/badge.svg)](https://codecov.io/gh/devsetgo/pip-checker)
[![Actions Status](https://github.com/devsetgo/pip-checker/workflows/PythonPackage/badge.svg)](https://github.com/devsetgo/pip-checker/actions)

SonarCloud:

[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_pip-checker&metric=sqale_rating)](https://sonarcloud.io/dashboard?id=devsetgo_pip-checker)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_pip-checker&metric=reliability_rating)](https://sonarcloud.io/dashboard?id=devsetgo_pip-checker)
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_pip-checker&metric=alert_status)](https://sonarcloud.io/dashboard?id=devsetgo_pip-checker)
[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=devsetgo_pip-checker&metric=bugs)](https://sonarcloud.io/dashboard?id=devsetgo_pip-checker)


# Pypi Requirements Checker
I got tired of trying to check if there is a new version of a library for projects. So I created a way to drop my requirements.txt into a box and then call Pypi to get the lastest version.

### Notes
Python 3.8 or higher

## How to User
- git clone https://github.com/devsetgo/pip-checker.git
- create virtual environment
  - Linux: python3 -m venv env
  - Windows: virtualenv env
- start virtual environment
  - Linux: source env/bin/activate
  - Windows: env\scripts\activate
- Install App requirements
  - cd app/
  - Linux: pip3 install -r requirments.txt or ./scripts/install
  - Windows: pip install -r requirements.txt
- Place **your* requirements.txt in the data folder
- Run application
  - Linux:
  ```console
  $ ./scripts/dev_run.sh
  ```
  - Windows:
  ```console
  uvicorn main:app --port 5000 --reload
  ```
  - Docker:
  ```console
  $ docker run mikeryan56 pypi-checker:latest
    ```
Browser localhost:5000 (or where ever you have it running)


### Try The App

```console

httpx
starlette==0.11.0

```
