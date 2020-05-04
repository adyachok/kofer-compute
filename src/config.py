import os

from src.models.faust_dao import ModelTask, ModelTaskDoEvent
from src.utils.logger import get_logger

logger = get_logger('config')


class Config:
    KAFKA_BROKER_URL = None
    WEB_PORT = None

    def __init__(self):
        """
        Initiates microservice configuration
        :return: configuration object
        """
        self.KAFKA_BROKER_URL = self._set_kafka_url()
        self.WEB_PORT = self._set_web_port()
        self.topics = {
            'model-tasks-do': None,
            'model-tasksdone': None,
            'model-metadata-updates': None
        }
        self.debug_models = {
            'mod-dummy':
                'https://mod-dummy-501-zz-test.22ad.bi-x.openshiftapps.com'
                '/v1/models/mod-dummy:predict',
            'mod-text-class':
                'https://mod-text-class-501-zz-test.22ad.bi-x.'
                'openshiftapps.com/v1/models/mod-text-class:predict'
        }

    def _set_kafka_url(self):
        kafka_broker_url = os.getenv('KAFKA_BROKER_URL')
        if not kafka_broker_url:
            kafka_broker_url = 'kafka://localhost'
        return kafka_broker_url

    def init_app(self, app):
        self._init_topics(app)

    def _init_topics(self, app):
        self.topics['model-tasks-do'] = app.topic('model-tasks-do',
                                                  value_type=ModelTaskDoEvent)
        self.topics['model-tasks-done'] = app.topic('model-tasks-done',
                                                    value_type=ModelTask)

    def _set_web_port(self):
        web_port = os.getenv('WEB_PORT')
        if not web_port:
            web_port = 8090
        return web_port
