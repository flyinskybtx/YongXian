import os
from dataclasses import dataclass, field

import numpy as np
import yaml

from config import COLORS, SYMBOLS, LAYERS


@dataclass
class BaseUnit:
    name: str
    pos: np.ndarray
    t: int = 0
    info: dict = field(default_factory=dict)
    
    def __post_init__(self):
        unit_type = self.name.split('-')[0]
        self.color = COLORS[unit_type]
        self.symbol = SYMBOLS[unit_type]
        self.layer = LAYERS[unit_type]
    
    def update(self):
        self.t += 1


def check_kill_chain():
    pass


def establish_connections():
    pass


def write_decorator(func):
    def wrapper(sender, receiver, *args):
        filename = os.path.join('.channels', sender.name + '->' + receiver.name)
        t = sender.t
        with open(filename, 'a') as stream:
            msg = func(sender, receiver, *args)
            yaml.dump({t: msg}, stream)
    
    return wrapper


def read_decorator(func):
    def wrapper(receiver, sender, *args):
        t = receiver.t
        filename = os.path.join('.channels', sender.name + '->' + receiver.name)
        with open(filename, 'a') as stream:
            msgs = yaml.safe_load(stream)
            msg = msgs[t]
            msg = func(receiver, sender, msg, *args)
            return msg
    
    return wrapper


def request_decorator(func):
    def wrapper(client, server, *args):
        # todo: log起来
        return func(client, server, *args)
    
    return wrapper
