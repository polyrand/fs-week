This is a full-stack machine learning project. It includes the following:

* Multiple Flask apps
* Model training script
* Tests
* GitHub workflow for automatic testing
* A good project organization!
* Documentation
* Good dependency management. We are using `pip-tools` but other managers also work.
* Automatic deployments to AWS SageMaker and saving the models to S3

## Exercises of each day

### Day 1

Start a **new** and **empty** GitHub repository.

1. Think about how you're going to organize your project. What folders will it have? What files will go into this folders?
2. Start writing [documentation](/documentation) about your project. You will need to keep it updated throughout the week. The instructions provided are for MkDocs, but you can use other documentation methods if you want.

3. Write a script to train an ML model.

Turn the 2.train.ipynb notebook into a python script

The script can have the following options:

```
--download-data
--train --epochs INT (it should have a default)
--optimizer STRING
--load-weights STRING
    
# extra work:
# load the data URL from an environment variable (using a .env file and the python-dotenv package)
```

Then you can run the script like:

```
python3 train.py --download-data --train --epochs 3 --optimizer sgd --load-weights my_weigths.pth
```

**Don't worry if you can't implement all the options**

#### Day 1.2

Try creating a Python class that abstracts all the operations you want to make that interact with the database.

```python
class DB:

	def __init__(self, dbname):
		self.conn =  sqlite3.connect(dbname)
		
	def do_something(self):
		with self.conn as cursor:
    		cursor.execute(".......", (a, b))
```


### Day 2

1. Understand [this](https://github.com/polyrand/fs-week) github repository. 
why it's organized like that, how is the documentation written (using the `mkdocs` library we sa), and more importantly, understanding the `service.py` file. That file is a Flask application, last week you used flask to show some HTML, this week we are using it to receive an image and doing a prediction with it.

2. Create an HTML form using flask. An HTML form is the same thing you fill in when signing up in a new website. The task is creating an HTML form that lets the user upload an image. [Here's some info](https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/) on how to do it, but feel free to look for other resources.

You can try doing everything inside `service.py` if that's easier at first. So both the file upload and model prediction is donde in the same place. Feel free to adapt the exercise.

3. After that's done, try to integrate this HTML form with `service.py`, now when you receive an image, instead of doing nothing with it, use the requests library to send it to the other service.

As always, having everything done is not the objective. The objective is that you understand how to design a solution to a problem and how to communicate and organize the "solution" (our project).

If you have time you can work on the documentation and improve it. Explain to other people how to run your `service.py` and/or `app.py`.

**Video**

[Logging inside a Flask app](https://www.youtube.com/watch?v=4ZiZCqC6rRQ)

### Day 3

* Create an HTML form to register a new user (email + password)
* Save the password hashed to the DB
* Finish writing the test in the `tests/test_app.py` file
* Add some more tests, even if they are simple ones

Extra:

* If you have problems with `passlib`. There's also an alternative secure hashing function using `hashlib`, which comes fomr the Python standard library.

Also, always take into account that hashing functions receive and return bytes, not strings. Passlib already handles that for you, but if you look at my implementation you'll see that I'm doing a few password.encode() to convert a string to bytes and hash(...).hex() to convert the hashed bytes to an hexadecimal string

If you are already receiving bytes you don't need to encode it, but when you get the data from the flask request i'm pretty sure it's as a string, not bytes. ANyway, if you don't get the hashing working 100% don't worry, you can "create" your own hashing by just appending a random string to the end. As long as you make it work and write a couple of tests.

Something extra to try in the exercises:

* Creating a test for the ML model (taking the functions from service.py). For example, testing that the function returns one of the 2 classes. Or that if you have an image that it's been correctly predicted, write a test for it.

### Day 4

Create a github workflow that does anything. It can be just a `print()` or running all the tests. You can do it in a new empty repository or in an old one.
Some resources that may be helpful:

* [Official introduction to GitHub Actions](https://docs.github.com/en/actions/learn-github-actions/introduction-to-github-actions)

* [GitHub Actios Syntax (this is a long one, you don't really need it for now)](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)

* [A basic template for a github action. It does a print("hello") with Python](https://github.com/polyrand/fs-week/blob/main/.github/workflows/echo.yaml)

Remember, the workflows/actions have to be inside a folder called `.github/workflows` inside your repo.


### Final

So far we have learned how to deal with Flask apps [running](/running) ML models, Python scripts to [train](/training) models, how to organize a project or how to write [documentation](/documentation).

Now imagine your ML product has do more things. Your users may be sending you some unwanted data and you need to filter it. Well, the best way to do it is with another model. The task for the last day is:

1. Getting a new dataset with items that are **not** part of your main dataset.
2. Train a yes/no model. The model should be able to filter data that does not belong to your dataset.
3. Deploy this model as a new Flask app.

When a new item arrives, it first goes through the first Flask app / service. If it determines it belongs to your data, then send the item to the main Flask service.

Some things you may modify:

* Instead of running the image through the 2 flask apps, you can implement an HTML dropdown / form field to let the user choose which model they want to run the image through.

* Instead of running the 2 ML models in different Flask apps, you can try putting the 2 models insider service.py. This is a double-edged sword. It's easier because you don't need to run an extra Flask app. However, now you need to load 2 models inside a single Flask app, which may also become a challenge.
