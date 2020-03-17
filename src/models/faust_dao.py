from abc import ABC
from enum import Enum

import faust
from typing import Any, Optional

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


class ModelTask(faust.Record):
    _id: Optional[str]
    model_name: str
    data: dict
    result: Optional[dict]
    # state: State = State.QUEUED
    state: str = ChoiceField(choices=['QUEUED', 'IN_PROGRESS', 'FINISHED',
                                      'ERROR'],
                             default='QUEUED', required=False)
