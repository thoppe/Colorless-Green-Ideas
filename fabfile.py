from fabric.api import local, env, task, prefix, cd

@task
def demo():
    local("python app.py")

@task
def heroku_create():
    local("heroku create flask-colorless")
    heroku_deploy()
    heroku_startup()

@task
def heroku_startup():
    local("heroku ps:scale web=1")

@task
def heroku_view():
    local("heroku open")

@task
def heroku_deploy():
    local("git push heroku flask:master")

@task
def heroku_DESTROY():
    local("heroku apps:destroy flask-colorless --confirm flask-colorless")

# Aliases
@task
def deploy(): heroku_deploy()
