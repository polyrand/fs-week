# How to run the model as a separate service

This app is designed to be run inside Flask. The machine learning model is running in `service.py`. The main app is inside `app.py`. If you run any of the apps in a different port, check the python files and modify them accordingly.

To run the apps use:

```bash
FLASK_ENV=development FLASK_APP=service.py flask run --port 5005
```

```bash
FLASK_ENV=development FLASK_APP=app.py flask run --port 5002
```

Now you can navigate to [127.0.0.1:5002](127.0.0.1:5002) and use your app. The main `app.py` calls `service.py` to do the predictions.

At the top fo the Flask apps there are a few configuration variables. They are mostly about the paths to find the files we need and the name of the files (for example the weights of the best performing model). Modify those if you change the project structure.