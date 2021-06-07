## MkDocs

The documentation of this project is built using mkdocs with the
[mkdocs-material](https://squidfunk.github.io/mkdocs-material/) theme.

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

```bash pip install mkdocs mkdocs-material ```

## Basic commands

* `mkdocs new [dir-name]` - Create a new project.  `mkdocs serve` - Start the live-reloading docs
* server.  `mkdocs build` - Build the documentation site.  `mkdocs -h` - Print help message and
* exit.

Now run:

``` mkdocs new documentation_page cd documentation_page ```

Edit the `mkdocs.yaml` file.

```yaml theme: name: material language: en plugins:
  - search
nav:
  - Introduction: 'index.md' Examples: 'examples.md' Models: 'models.md'
```

Development:

```bash mkdocs serve ```

Inside your `documentation_page/docs` folder, you can create an `examples.md` and `models.md` files
and they will show up in your mkdocs site!

Production:

```bash mkdocs build ```

That's it! This will generate a `site/` folder.

## Updating the documentation

Modify any of the markdown files and from the `documentation_page/` folder run:


`mkdocs gh-deploy`

This will automatically build the docs and push them to the `gh-pages` branch. **Do not modify the
files directly in the github branch**. GitHub will detect the branch and build a static
documentation site for the project.

**NOTE**

Make sure to keep the `mkdocs.yaml` configuration file updated if you create new files.
