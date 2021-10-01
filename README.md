# python-saleae-resampler

Convert
[Saleae](https://support.saleae.com/user-guide/using-logic/exporting-data#exporting-raw-data)
export files to binary

## Local Development

Change to a branch:

```console
git checkout -b my_branch
```

Install Poetry: https://python-poetry.org/docs/#installation.

Install project deps and pre-commit hooks:

```console
poetry install
pre-commit install
pre-commit run --all-files
```

Ready to go, try the following::

```console
saleae_resampler --channel 0 --rate 25000 < sample.csv > sample.bin
```

Remember to activate your virtualenv whenever working on the repo, this is needed
because pylint and mypy pre-commit hooks use the "system" python for now (because reasons).

Running "pre-commit run --all-files" and "py.test -v" regularly during development and
especially before committing will save you some headache.
