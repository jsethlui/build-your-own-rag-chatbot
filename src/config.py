
from .utils import loadConfig
from pydantic.v1 import BaseSettings

class Config(BaseSettings):
    config = loadConfig()

    apiKey = config["chatbot"]["apiKey"]
    llm = config["chatbot"]["llm"]
    temperature = int(config["chatbot"]["temperature"])
    template = config["chatbot"]["template"]