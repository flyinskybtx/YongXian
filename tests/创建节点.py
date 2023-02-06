import functools
import itertools

import numpy as np

from agents import *
from networkx_prj.config import *

from agents import *

if __name__ == '__main__':
    poses = {
        "火力": np.random.uniform(-1, 1, (NUM_NODES["火力"], 2)) * DEFEND_AREA_RADIUS / 2,
        "指挥控制": np.random.uniform(-1, 1, (NUM_NODES["指挥控制"], 2)) * DEFEND_AREA_RADIUS,
        "预警探测": np.random.uniform(-1, 1, (NUM_NODES["预警探测"], 2)) * DEFEND_AREA_RADIUS,
        "跟踪识别": np.random.uniform(-1, 1, (NUM_NODES["跟踪识别"], 2)) * DEFEND_AREA_RADIUS,
    }
    
    
    def get_node_class(_type: str, ) -> BaseUnit:
        return {
            "火力": FiringUnit,
            "指挥控制": CommandUnit,
            "预警探测": AlarmRadar,
            "跟踪识别": TrackingRadar,
        }[_type]
    
    
    all_nodes = {}
    all_edges = {}
    
    for _type, _poses in poses.items():
        NodeClass = get_node_class(_type)
        all_nodes[_type] = []
        for i, pos in enumerate(_poses):
            name = '-'.join([_type, f'{i:03d}'])
            # noinspection PyCallingNonCallable
            _node = NodeClass(name=name, pos=pos, t=0)
            all_nodes[_type].append(_node)
    
    filename = '创建节点.yml'
    stream = to_yaml(all_nodes, filename)
    all_nodes = from_yaml(stream=filename, )
    print(all_nodes)
