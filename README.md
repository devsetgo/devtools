# PIP Requirements Checker
I got tired of trying to figure out which libraries are updated, so I created a simple way to check if your requirements.txt file is up-to-date. Add your requirements.txt to the data folder and then run it to check if the version has changed at PyPI.


### Notes
Python 3.6 or higher

## How to User
- git clone https://github.com/devsetgo/pip-checker.git
- create virtual environment
  - Linux: python3 -m venv env
  - Windows: virtualenv env
- start virtual environment
  - Linux: source env/bin/activate
  - Windows: env\scripts\activate
- Install App requirements
  - Linux: pip3 install -r requirments.txt
  - Windows: pip install -r requirements.txt
- Place **your* requirements.txt in the data folder
- Run application
  - Linux: python3 app.py
  - Windows: python app.py
- Results will be placed in the data folder in the file new_requirments.txt
  
# Example output in file
```
aiosqlite==0.10.0
alembic==1.0.9 # Change from 1.0.8
```

