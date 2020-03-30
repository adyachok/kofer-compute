from abc import ABC
from enum import Enum

import faust
from typing import Any, Optional, List

from src.utils.fields import ChoiceField


class ModelMetadata(faust.Record, ABC):
    _id: Optional[str]
    name: str
    latest_version: int
    server_metadata: Any
    business_metadata: Any


class State(Enum):
    QUEUED = 'QUEUED'
    IN_PROGRESS = 'IN_PROGRESS'
    FINISHED = 'FINISHED'
    ERROR = 'ERROR'


class CalculationItem(faust.Record):
    name: str
    unit_step: str
    type: str = ChoiceField(choices=['float', 'int', 'str', 'array', 'byte'],
                            default='str')
    value: Any


class ModelTask(faust.Record):
    _id: Optional[str]
    model_name: str
    data: List[CalculationItem]
    result: Optional[List[Any]]
    # state: State = State.QUEUED
    state: str = ChoiceField(choices=['QUEUED', 'IN_PROGRESS', 'FINISHED',
                                      'ERROR'],
                             default='QUEUED', required=False)
    runner_id: Optional[str] = ''
    execution_state: Optional[int] = 0


class ModelTaskDoEvent(faust.Record):
    task: ModelTask
    runner_code: Optional[str] = ''
