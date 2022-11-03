import os
import logging as log
from os import environ
from logging.handlers import *


# if not os.path.exists("log"):
#     os.mkdir("log")


class Environment:
    SECRET_KEY: str = str(environ.get(
        "SECRET_KEY", default="django-insecure-g=k76mt-5o@kl$t018n96u^y=xs(n=@cx!82003%76(j&h#^w7"
    ))

    DEBUG: str = str(environ.get(
        "DEBUG", default=True
    ))


# log.basicConfig(
#     level=log.DEBUG,
#     format='[%(asctime)s.%(msecs)03d] [%(levelname)-6s] [%(filename)-24s] : %(message)s',
#     handlers=[
#         log.StreamHandler(),
#         TimedRotatingFileHandler(filename="log/application.log", when="D", backupCount=14)
#     ]
# )


ENV = Environment()
