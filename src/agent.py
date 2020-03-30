import json
import os

import aiohttp
import numpy as np

from src.app import app, config
from src.models.faust_dao import State, CalculationItem

from src.utils.logger import get_logger


logger = get_logger('zz-compute-agents')


@app.agent(config.topics['model-tasks-do'])
async def compute_agent(events):
    async for event in events:
        task = event.task
        print(f'MYAGENT RECEIVED -- {task!r}')
        task.state = State.IN_PROGRESS.value
        await config.topics['model-tasks-done'].send(value=task)
        try:
            async with aiohttp.ClientSession() as session:
                compute_closure = compute(session, task)
                if not event.runner_code:
                    outputs = await compute_closure(task.data)
                else:
                    _locals = {'klass': None}
                    exec(event.runner_code,
                         {'__builtins__': __builtins__, 'np': np},
                         _locals)
                    klass = _locals.get('klass')
                    gen = klass(compute_closure).execute(task.data)
                    async for outputs, execution_state in gen:
                        if execution_state < 100:
                            task.execution_state = execution_state
                            await config.topics['model-tasks-done'].send(
                                value=task)
                logger.info(f'Got next response outputs {outputs}')
                task.result = outputs
                task.execution_state = 100
                task.state = State.FINISHED
                await config.topics['model-tasks-done'].send(value=task)
        except aiohttp.client_exceptions.ClientConnectorError as e:
            task.state = State.ERROR
            task.result = []
            logger.error(f'Error occured while computing task {task._id}.')
            await config.topics['model-tasks-done'].send(value=task)
        yield task


def compute(session, task):
    url = f'http://{task.model_name}:8501/v1/models/{task.model_name}' \
          f':predict'
    if os.getenv('DEBUG_URLS'):
        url = f'https://mod-dummy-501-zz-test.22ad.bi-x.' \
              f'openshiftapps.com/v1/models/{task.model_name}:predict'

    async def inner(data):
        is_of_calc_type = any([isinstance(i, CalculationItem) for i
                               in data])
        if is_of_calc_type:
            inputs = [[item.value] for item in data]
        else:
            inputs = data
        data = json.dumps(
            {"signature_name": "serving_default",
             "inputs": inputs})
        # headers = {"content-type": "application/json"}
        async with session.post(url, data=data) as response:
            response = await response.json()
            return response.get('outputs', [])
    return inner
