from invoke import run, task


@task(name='prettier-js')
def prettier_js(context):
    """Runs prettier, a JS code formatter"""
    run('bin/prettier_fix.sh', echo=True)


@task(name='prettier-py')
def prettier_py(context):
    run('black --verbose ./backend/**/*', echo=True)


@task(name='set-node-path')
def set_node_path(context):
    """set node path"""
    run('bin/functions/set_node_path.sh', echo=True)


@task(name='install-requirements')
def install_requirements(context):
    """Install python and node requirements"""
    run('pipenv install --skip-lock', echo=True)
    run('npm install', echo=True)


@task(name='build-local')
def build_local(context):
    """run webpack build"""
    run('npm run build', echo=True)


@task(name='webpack-server')
def webpack_dev_server(context):
    """run webpack-dev server"""
    run('npm run watch', echo=True)


@task(name='run-server')
def python_server(context):
    """run python server"""
    run('python manage.py runserver', echo=True)
