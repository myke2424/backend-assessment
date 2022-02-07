import logging

from flask import Flask

from api.routes import posts_api
from config import Config

logging.basicConfig(
    level=Config.LOG_LEVEL,
    format=Config.LOG_FORMAT,
    handlers=[logging.FileHandler(Config.LOG_FILE_PATH), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)
logger.setLevel(Config.LOG_LEVEL)


def run_app() -> None:
    app = Flask(__name__)
    app.config.from_object(Config)
    app.register_blueprint(posts_api, url_prefix="/api")
    app.run(host=Config.HOST, port=Config.PORT)


if __name__ == "__main__":
    run_app()
