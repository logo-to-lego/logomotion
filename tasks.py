# pylint: skip-file
from invoke import task


@task
def hello(ctx):
    ctx.run("python3 src/hello.py", pty=True)


@task
def lint(ctx):
    ctx.run("pylint src", pty=True)


@task
def test(ctx):
    ctx.run("pytest src", pty=True)


@task
def black(ctx):
    ctx.run("black src", pty=True)


# From https://github.com/ohjelmistotekniikka-hy/python-todo-app/blob/master/tasks.py
@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)


@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)
