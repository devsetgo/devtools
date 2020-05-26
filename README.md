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
  - Linux: ./scripts/dev_run.sh
  - Windows: uvicorn main:app --port 5000 --reload
  - Docker: docker run mikeryan56/pypi-checker:latest

Browser localhost:5000 (or where ever you have it running)


### Try The App
'''
httpx
starlette==0.11.0

'''

