# How to run the model as a service


This app is designed to be run inside Flask. The app is in `service.py`


```bash
FLASK_ENV=development FLASK_APP=service.py flask run --port 5001
```

