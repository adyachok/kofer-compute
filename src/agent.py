import json
import os

import aiohttp

from src.app import app, config
from src.models.faust_dao import State

from src.utils.logger import get_logger


logger = get_logger('zz-compute-agents')


@app.agent(config.topics['model-tasks-do'])
async def compute_agent(tasks):
    async for task in tasks:
        print(f'MYAGENT RECEIVED -- {task!r}')
        task.state = State.IN_PROGRESS.value
        await config.topics['model-tasks-done'].send(value=task)
        try:
            async with aiohttp.ClientSession() as session:
                response = await compute(session, task)
                logger.info(f'Got next response {response}')
                task.result = response.get('outputs', [])
                task.state = State.FINISHED
                await config.topics['model-tasks-done'].send(value=task)
        except aiohttp.client_exceptions.ClientConnectorError as e:
            task.state = State.ERROR
            tasks.result = [str(e)]
            await config.topics['model-tasks-done'].send(value=task)
        yield task


async def compute(session, task):
    inputs = [[item.value] for item in task.data]
    data = json.dumps(
        {"signature_name": "serving_default",
         "inputs": inputs})

    url = f'http://{task.model_name}/v1/models/{task.model_name}:predict'
    if os.getenv('DEBUG_URLS'):
        url = f'https://mod-dummy-501-zz-test.22ad.bi-x.openshiftapps.com' \
              f'/v1/models/{task.model_name}:predict'
    # headers = {"content-type": "application/json"}
    async with session.post(url, data=data) as response:
        return await response.json()
