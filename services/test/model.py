from pydantic import conint

from settings import Settings
import random


class Test:
    __slots__ = ['pong']

    settings = Settings()

    def __init__(self) -> None:
        self.pong = 'pong'

    @staticmethod
    def generate_list(n: conint()):
        generator = []
        for k in range(0, n):
            generator.append(random.randint(0, 99))
        return generator
