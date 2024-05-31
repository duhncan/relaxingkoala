# Relaxing Koala Restaraunt Management System

This software aims to implement the requirements and quality attributes of the new Restaurant Management System.




# Start Application
## Linux
export FLASK_APP=run.py
export FLASK_ENV=development


## Windows Powershell
$env:FLASK_APP = "run.py"
$env:FLASK_ENV = "development"




# Update DB Models
To update db models, run the following commands:
```
flask db init
flask db migrate -m "Any Message of the updates"
flask db upgrade
```