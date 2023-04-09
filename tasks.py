# pylint: skip-file
from invoke import task

# python -m venv .venv
# pip install invoke
# inv *task*
# to system: pip install pylint pre-commit

import os
current_file_path = os.path.abspath(__file__)
current_dir_path = os.path.dirname(current_file_path)
os.chdir(current_dir_path)


@task
def dev(ctx):
    ctx.run("pip install -r requirements.txt")
    ctx.run("pre-commit install")


@task
def freeze(ctx):
    ctx.run("pip freeze > requirements.txt")


@task
def start(ctx):
    ctx.run('python ./chumachechy/manage.py runserver')


@task
def pep8(ctx):
    ctx.run("pip install autopep8")
    ctx.run("python -m autopep8 --in-place --recursive ./chumachechy")


@task(pep8)
def doc(ctx):
    ctx.run("sphinx-apidoc -o ./docs/ ./chumachechy/")
    ctx.run("sphinx-build -b html docs docs/_build/html")
    ctx.run("powershell ./docs/_build/html/index.html")


@task(pep8)
def pre(ctx):
    ctx.run("pre-commit run --all-files")
