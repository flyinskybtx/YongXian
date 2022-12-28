import itertools
from copy import deepcopy
from dataclasses import dataclass, field

import numpy as np
from matplotlib import pyplot as plt
from scipy.spatial.distance import cdist
import plotly.graph_objects as go
from tqdm import trange

from agents import Radar, Commander, Missile, Enemy
from yongxian import create_pheudo_random_pos, create_plotly_nodes, create_random_pos

NUM_RADAR = 32
NUM_COMMANDER = 32
NUM_MISSILE = 64
NUM_ENEMY = 10

RADAR_Z = 1
COMMANDER_Z = 0
MISSILE_Z = -1

BATTLE_GROUD_SIZE = int(1e4)
DEFEND_RADIUS = int(1e3)
R2C_DIST = 4e2
C2C_DIST = 5e2
C2M_DIST = 4e2

CONNECTION_RADIUS = 4e2
CONNECTION_RATE = 0.4

NUMBERS = {
    "预警探测": 300,
    "跟踪识别": 200,
    "指挥控制": 200,
    "火力": 500,
    "电子对抗": 200,
    "网络攻防": 200,
}

LAYERS = {
    "火力": 4,
    "网络攻防": 4,
    "指挥控制": 3,
    "预警探测": 2,
    "跟踪识别": 1,
    "电子对抗": 1,
}

POSES = {
    "火力": np.random.uniform([-1, -1], [0, 1], (NUMBERS["火力"], 2)) * DEFEND_RADIUS,
    "网络攻防": np.random.uniform([0, -1], [1, 1], (NUMBERS["网络攻防"], 2)) * DEFEND_RADIUS,
    "指挥控制": np.random.uniform(-1, 1, (NUMBERS["指挥控制"], 2)) * DEFEND_RADIUS,
    "预警探测": np.random.uniform(-1, 1, (NUMBERS["预警探测"], 2)) * DEFEND_RADIUS,
    "跟踪识别": np.random.uniform([-1, -1], [0, 1], (NUMBERS["跟踪识别"], 2)) * DEFEND_RADIUS,
    "电子对抗": np.random.uniform([0, -1], [1, 1], (NUMBERS["电子对抗"], 2)) * DEFEND_RADIUS,
}

SYMBOLS = {
    "火力": "circle",
    "网络攻防": "circle",
    "指挥控制": "circle",
    "预警探测": "circle",
    "跟踪识别": "circle",
    "电子对抗": "circle",
}

COLORS = {
    "火力": "orange",
    "网络攻防": "purple",
    "指挥控制": "blue",
    "预警探测": "pink",
    "跟踪识别": "cyan",
    "电子对抗": "olive",
}


@dataclass
class Node:
    id: str
    pos: np.ndarray
    layer: int
    color: str
    type: str
    # _activated: bool = field(init=False)


def make_layout():
    return go.Layout(
        xaxis=dict(range=[-DEFEND_RADIUS, DEFEND_RADIUS], autorange=False),
        yaxis=dict(range=[-DEFEND_RADIUS, DEFEND_RADIUS], autorange=False),
        title="涌现",
        # hovermode="closest",
        legend=dict(title="图例"),
        # {'#00cc96':'missile','#ffa15a':'commander','#636efa':'radar',},
        updatemenus=[dict(
            type="buttons", buttons=[dict(label="Play", method="animate", args=[None, ]), ], ),
        ],
    )


if __name__ == '__main__':
    units = {}
    for key, value in POSES.items():
        units[key] = []
        for i, pos in enumerate(value):
            units[key].append(Node(f'{key}{i}', pos, LAYERS[key], COLORS[key], SYMBOLS[key]))
    
    nodes = {}
    for key in units.keys():
        for unit in units[key]:
            x, y = unit.pos
            z = unit.layer
            name = unit.id
            color = unit.color
            symbol = unit.type
            nodes[name] = go.Scatter3d(name=name, x=[x], y=[y, ], z=[z], mode='markers',
                                       showlegend=False,
                                       marker={'color': color, 'size': 10, 'symbol': symbol, "opacity": 0.7}, )
    
    edges = {}
    pairs = itertools.combinations(list(units.keys()), 2)
    for key1, key2 in pairs:
        if abs(LAYERS[key1] - LAYERS[key2]) == 1:
            for u1 in units[key1]:
                x1, y1 = u1.pos
                z1 = u1.layer
                id1 = u1.id
                color = u1.color
                
                for u2 in units[key2]:
                    x2, y2 = u2.pos
                    z2 = u2.layer
                    id2 = u2.id
                    
                    if np.linalg.norm(np.array([x1 - x2, y1 - y2])) <= CONNECTION_RADIUS:  # 在连接范围内
                        if np.random.uniform(0, 1) <= CONNECTION_RATE:  # 一定概率连
                            edges[id1 + '-' + id2] = go.Scatter3d(x=[x1, x2], y=[y1, y2], z=[z1, z2],
                                                                  mode='lines',
                                                                  showlegend=False,
                                                                  line={'width': 3,
                                                                        'color': color, })
    
    print(len(list(nodes.keys())))
    print(len(list(edges.keys())))
    
    fig_data = list(nodes.values()) \
               + list(edges.values())
    
    fig = go.Figure(
        data=fig_data,
        # layout=make_layout(),
        # frames=fig_frames,
    )
    fig.show("browser")
