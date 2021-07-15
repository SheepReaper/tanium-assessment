# Assessment Instructions

## Run the Scenario

**Requirements**

The assesment scenario requires `requests` and `returns`.
Install them via `pipenv` or your own package-manager:

```shell
pipenv install
```

**Running It**

Activate your virtual environment, or enter a pipenv shell:

```shell
pipenv shell
```

Run it:

```shell
./run-scenario.py
```

## Run the unit tests

**Requirements**

The tests require `pytest` and `requests-mock`.
Install them (and all other dev dependencies) via `pipenv` or your own package-manager:

```shell
pipenv install --dev
```

**Running the tests**

Run it:

```shell
pytest
```

## Generate a coverage report

**Requirements**

The coverage report requires `coverage`.
Install it (and all other dev dependencies) via `pipenv` or your own package-manager:

```shell
pipenv install --dev
```

**Build Report**

Run this:

```shell
coverage run
coverage html
```

**View Reports**

Report is output in html to the `htmlcov/` directory. Just open `index.html` in a browser.
