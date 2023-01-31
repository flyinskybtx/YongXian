import numpy as np

from agents.alarm_radar import AlarmRadar
from agents.command_unit import CommandUnit
from agents.firing_unit import FiringUnit
from agents.tracking_radar import TrackingRadar
from networkx_prj.config import *

from agents import *

if __name__ == '__main__':
    poses = {
        "火力": np.random.uniform(-1, 1, (NUM_NODES["火力"], 2)) * DEFEND_AREA_RADIUS / 2,
        "指挥控制": np.random.uniform(-1, 1, (NUM_NODES["指挥控制"], 2)) * DEFEND_AREA_RADIUS,
        "预警探测": np.random.uniform(-1, 1, (NUM_NODES["预警探测"], 2)) * DEFEND_AREA_RADIUS,
        "跟踪识别": np.random.uniform(-1, 1, (NUM_NODES["跟踪识别"], 2)) * DEFEND_AREA_RADIUS,
    }
    node_class_mapping = {
        "火力": FiringUnit,
        "指挥控制": CommandUnit,
        "预警探测": AlarmRadar,
        "跟踪识别": TrackingRadar,
    }
    
    all_nodes = {}
    all_edges = {}
    
    for _type, _poses in poses.items():
        NodeClass = node_class_mapping[_type]
        all_nodes[_type] = []
        for i, pos in enumerate(_poses):
            name = '-'.join([_type, f'{i:03d}'])
            _node = NodeClass(name=name, pos=pos, t=0)
            all_nodes[_type].append(_node)
