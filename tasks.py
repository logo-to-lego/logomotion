# pylint: skip-file
from invoke import task


@task
def lint(ctx):
    ctx.run("pylint src", pty=True)


@task
def test(ctx):
    ctx.run("pytest src", pty=True)

@task
def e2e(ctx):
    ctx.run("robot src", pty=True)

@task
def black(ctx):
    ctx.run("black src", pty=True)


@task(optional=["debug"])
def start(ctx, logo_file, debug=False):
    command = f"python3 src/main.py {logo_file} "
    if debug:
        command += "-d"
    ctx.run(command)


# From https://github.com/ohjelmistotekniikka-hy/python-todo-app/blob/master/tasks.py
@task
def coverage(ctx):
    ctx.run("coverage run --branch -m pytest src", pty=True)


@task(coverage)
def coverage_report(ctx):
    ctx.run("coverage html", pty=True)
