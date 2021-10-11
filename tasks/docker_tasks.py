from invoke import run, task


@task(name='docker-hot-enabled', aliases=['dc', 'dc-front'])
def docker_hot_reload(context):
    """Runs docker-compose in detached mode with hot reload enabled"""
    context.run('docker-compose up -d', echo=True)


@task(name='docker-hot-disabled', aliases=['dc-hd', 'dc-bend'])
def docker_hot_reload_disabled(context):
    """Runs docker-compose in detached mode with hot reload disabled"""
    context.run('docker-compose -f docker-compose.yml -f .docker/docker-compose-no-watch.yml up -d', echo=True)


@task(name='docker-front-disabled', aliases=['dc-fd', 'dc-no-front'])
def docker_frontend_build_disabled(context):
    """Runs docker-compose in detached mode with frontend build disabled"""
    context.run('docker-compose -f docker-compose.yml -f .docker/docker-compose-no-front.yml up -d', echo=True)
