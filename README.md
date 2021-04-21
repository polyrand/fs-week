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

## Testing the app

Testing is done using pytest. After you install it, from the root of the repo run:

```bash
python3 -m pytest -vv
```

## Running the Flask app

TO DO

## Training a new model

TO DO

## Contributing to the docs

We are using [mkdocs](https://www.mkdocs.org/)

Documentation is deployed using the command `mkdocs gh-deploy` do not
update the files in GitHub directly. Update the markdown in your laptop and use the command.
Also, remember to keep the `mkdocs.yaml` synchronized with your markdown files.
