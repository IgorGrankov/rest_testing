import logging
import inspect
from tests.planet_model import Planet, Planets
from requests import Session, Response


def format_logs(level=logging.DEBUG):
    name = inspect.stack()[1][3]
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler("logs.log", mode="a")
    handler.setLevel(level)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s: %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logging = format_logs()


def response_logging_hook(r: Response, *args, **kwargs):
    logging.info(f"{r.request.method} request to {r.request.url}")
    logging.info(f"request body is {r.request.body}")
    logging.info(f"response text is {r.text}")
    logging.info(f"response status code is {r.status_code}")
    r.raise_for_status()


class ApiClient:
    def __init__(self, host_endpoint="https://swapi.dev/api/"):
        self.host_endpoint = host_endpoint
        self.session = Session()
        self.session.hooks["response"] = response_logging_hook

    def get_planets_id(self, num=""):
        return Planet(**
                      self.session.get(self.host_endpoint + f'planets/{num}').json())

    def get_planets(self, query=None, pagination=None):
        return Planets(**
                       self.session.get(self.host_endpoint + f'planets/?{pagination}',
                                        params=dict(search=query)).json())
