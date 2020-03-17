#!/usr/bin/env python
import faust

from src.config import Config
from src.utils.logger import get_logger


logger = get_logger('app')


config = Config()

app = faust.App('compute', broker=config.KAFKA_BROKER_URL,
                debug=True,
                web_port=config.WEB_PORT,
                autodiscover=True,
                origin='src')
config.init_app(app)


if __name__ == '__main__':
    app.main()
