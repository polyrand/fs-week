# Short product title

> Short explanation about it

## Managing dependencies and installation

We are using [pip-tools](https://github.com/jazzband/pip-tools)

To build the `.txt` files use:

```bash
pip-compile -v --output-file requirements/production.txt requirements/production.in
pip-compile -v --output-file requirements/dev.txt requirements/dev.in
```

To sync the dependencies use:

```bash
pip-sync requirements/*.txt
```

## Running the Flask app

TO DO

## Training a new model

TO DO
