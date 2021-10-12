from invoke import Collection

from .docker_tasks import docker_hot_reload, docker_hot_reload_disabled, docker_frontend_build_disabled
from .testing_tasks import lint_js, lint_py, test_python
from .dev_tasks import (
    prettier_js,
    prettier_py,
    set_node_path,
    install_requirements,
    build_local,
    webpack_dev_server,
    python_server
)

task_col = Collection()

task_col.add_task(prettier_js)
task_col.add_task(prettier_py)
task_col.add_task(lint_js)
task_col.add_task(lint_py)
task_col.add_task(test_python)
task_col.add_task(set_node_path)
task_col.add_task(install_requirements)
task_col.add_task(build_local)
task_col.add_task(webpack_dev_server)
task_col.add_task(python_server)
task_col.add_task(docker_hot_reload)
task_col.add_task(docker_hot_reload_disabled)
task_col.add_task(docker_frontend_build_disabled)
