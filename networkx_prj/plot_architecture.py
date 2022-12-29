import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from config import *

POSES = {
    "火力": np.random.uniform([-1, -1], [0, 1], (NUM_NODES["火力"], 2)) * DEFEND_RADIUS,
    "网络攻防": np.random.uniform([0, -1], [1, 1], (NUM_NODES["网络攻防"], 2)) * DEFEND_RADIUS,
    "指挥控制": np.random.uniform(-1, 1, (NUM_NODES["指挥控制"], 2)) * DEFEND_RADIUS,
    "预警探测": np.random.uniform(-1, 1, (NUM_NODES["预警探测"], 2)) * DEFEND_RADIUS,
    "跟踪识别": np.random.uniform([-1, -1], [0, 1], (NUM_NODES["跟踪识别"], 2)) * DEFEND_RADIUS,
    "电子对抗": np.random.uniform([0, -1], [1, 1], (NUM_NODES["电子对抗"], 2)) * DEFEND_RADIUS,
}

if __name__ == '__main__':

    graph_dict = {}
    for name in NAMES:
        G = nx.Graph(name=name)
        for i, pos in enumerate(POSES[name]):
            G.add_node(f'{name}-{i}', type=name, pos=pos)
        
        graph_dict[name] = G
    
    options = {"edgecolors": "tab:gray",
               "node_size": 100,
               "alpha": 0.9}
    
    for name in NAMES:
        G = graph_dict[name]
        pos = {n: G.nodes()[n]['pos'] for n in list(G.nodes)}
        # pos = {f'{name}-{i}': v for i, v in enumerate(POSES[name])}
        nx.draw_networkx_nodes(G, pos, node_color=f"tab:{COLORS[name]}", **options)
    plt.show()
    #
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    for name in NAMES:
        G = graph_dict[name]
        pos = {n: G.nodes()[n]['pos'] for n in list(G.nodes)}
        node_xyz = np.array([pos[v] for v in sorted(G)])
        z = np.ones(shape=(node_xyz.shape[0], 1)) * LAYERS[name]
        
        node_xyz = np.concatenate([node_xyz, z], axis=-1)
        ax.scatter(*node_xyz.T, s=10,
                   # ec="w"
                   )
        fig.tight_layout()
    plt.show()
