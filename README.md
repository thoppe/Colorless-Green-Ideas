# flask-vial
A lightweight template of flask implemented as a cookiecutter

When you want to put something complicated up on the web _right now_. This is a barebones template to help get your small flask project up and running. Navigate to a _fresh_ clone git repo that has the project you're working on. Install `cookiecutter`, `fabric` and `virtualenvwrapper` and use it to build a vial (tiny flask):

    pip install cookiecutter
    cookiecutter https://github.com/thoppe/flask-vial.git

These things will happen (perhaps destructively):

1. Sets up a virtual environment and actives it, `{{app_name-vial}}`
2. Installs all dependencies in `requirements.txt` and merges with any existing one.
3. Creates a new branch called `flask` to work in.
4. Copies all the basic flask files to this directory.

To test the install:

    fab demo

and navigate to [http://127.0.0.1:5000/](http://127.0.0.1:5000/).