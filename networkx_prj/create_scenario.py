import itertools
from dataclasses import dataclass
from config import *

import numpy as np

poses = {
    # "火力": np.random.uniform([-1, -1], [0, 1], (NUM_NODES["火力"], 2)) * DEFEND_RADIUS,
    # "网络攻防": np.random.uniform([0, -1], [1, 1], (NUM_NODES["网络攻防"], 2)) * DEFEND_RADIUS,
    "火力": np.random.uniform(-1, 1, (NUM_NODES["火力"], 2)) * DEFEND_RADIUS,
    "网络攻防": np.random.uniform(-1, 1, (NUM_NODES["网络攻防"], 2)) * DEFEND_RADIUS,
    "指挥控制": np.random.uniform(-1, 1, (NUM_NODES["指挥控制"], 2)) * DEFEND_RADIUS,
    "预警探测": np.random.uniform(-1, 1, (NUM_NODES["预警探测"], 2)) * DEFEND_RADIUS,
    # "跟踪识别": np.random.uniform([-1, -1], [0, 1], (NUM_NODES["跟踪识别"], 2)) * DEFEND_RADIUS,
    # "电子对抗": np.random.uniform([0, -1], [1, 1], (NUM_NODES["电子对抗"], 2)) * DEFEND_RADIUS,
    "跟踪识别": np.random.uniform(-1, 1, (NUM_NODES["跟踪识别"], 2)) * DEFEND_RADIUS,
    "电子对抗": np.random.uniform(-1, 1, (NUM_NODES["电子对抗"], 2)) * DEFEND_RADIUS,
}


@dataclass
class MyNode:
    id: str
    pos: np.ndarray
    layer: int
    color: str
    type: str
    symbol: str
    # _activated: bool = field(init=False)


@dataclass
class MyEdge:
    start: str
    end: str
    color: str
    # _activated: bool = field(init=False)


def build_grouped_nodes():
    group_nodes = {}
    for name in NAMES:
        nodes = []
        color = COLORS[name]
        symbol = SYMBOLS[name]
        layer = LAYERS[name]
        for i, pos in enumerate(poses[name]):
            nodes.append(MyNode(
                id=f'{name}-{i}',
                type=name,
                pos=pos,
                color=color,
                symbol=symbol,
                layer=layer,
            ))
        group_nodes[name] = nodes
    return group_nodes


def build_group_edges(group_nodes):
    pairs = list(itertools.combinations(list(group_nodes.keys()), 2))
    pairs += [(k, k) for k in group_nodes.keys()]
    
    group_edges = {}
    for key1, key2 in pairs:
        key1, key2 = sorted([key1, key2])
        if key1 + '-' + key2 in RULES:  # 符合连接规则
            limits = RULES[key1 + '-' + key2]
            nodes1 = group_nodes[key1]
            nodes2 = group_nodes[key2]
            
            edges = []
            for n1 in nodes1:
                color = COLORS_EDGE[key1 + '-' + key2]
                connectable_n2 = [n2 for n2 in nodes2
                                  if np.linalg.norm(n1.pos - n2.pos) <= CONNECTION_RADIUS and
                                  np.random.random() <= CONNECTION_RATE and n1.id != n2.id]
                if len(connectable_n2) > limits:
                    connectable_n2 = np.random.choice(connectable_n2, limits, replace=False)
                
                for n2 in connectable_n2:
                    edges.append(MyEdge(
                        start=n1.id,
                        end=n2.id,
                        color=color,
                    ))
            group_edges[key1 + '-' + key2] = edges
    return group_edges


group_nodes = build_grouped_nodes()
group_edges = build_group_edges(group_nodes)
