import os
import yaml


class Host:
    def __init__(self, graph, t=0):
        self.graph = graph
        self.t = t
    
    def write(self, publisher, listener, message):
        pass
    
    def read(self, publisher, listener, t: int):
        pass
    
    def request(self, listener, task, **kwargs):
        pass
    
    def _create_msg_file(self, publisher, listener):
        pass


def check_connection(f):
    def wrapper(*args):
        return f(*args)
    
    return wrapper


