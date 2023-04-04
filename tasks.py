from invoke import task

@task
def start(ctx):
    ctx.run('python ./chumachechy/manage.py runserver')
