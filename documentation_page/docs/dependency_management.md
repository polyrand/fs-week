# Python packages and dependencies

We can use [pip-tools](https://pypi.org/project/pip-tools/) to take
a file with requirements and get a new one with the versions pinned.

*Pinned = with a very specific version number associated*

```bash
pip-compile -v --output-file requirements/main.txt requirements/main.in
pip-compile -v --output-file requirements/dev.txt requirements/dev.in
```

To upgrade:

```bash
pip-compile -v --upgrade --output-file requirements/main.txt requirements/main.in
pip-compile -v --upgrade --output-file requirements/dev.txt requirements/dev.in
```

To replicate an environment:

```bash
pip-sync requirements/*.txt
```
