from src.app import app, config
from src.models.faust_dao import State

from src.utils.logger import get_logger


logger = get_logger('zz-compute-agents')


@app.agent(config.topics['model-tasks-do'])
async def compute_agent(tasks):
    """Example agent."""
    async for task in tasks:
        print(f'MYAGENT RECEIVED -- {task!r}')
        task.state = State.IN_PROGRESS.value
        await config.topics['model-tasks-done'].send(value=task)
        yield task
