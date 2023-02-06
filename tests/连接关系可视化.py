import functools

import networkx as nx
from matplotlib import pyplot as plt

from agents import from_yaml, BaseUnit
from config import COLORS_EDGE

if __name__ == '__main__':
    filename = '创建节点2.yml'
    all_nodes = from_yaml(stream=filename, )
    all_nodes = functools.reduce(list.__add__, all_nodes.values(), )
    
    GG = nx.Graph(name='all')
    
    # 节点
    for node in all_nodes:
        assert isinstance(node, BaseUnit)
        GG.add_node(node.name, type=node.unit_type, pos=node.pos, color=node.color, symbol=node.symbol,
                    layer=node.layer)
    
    # 边
    all_nodes_dict = {n.name:n for n in all_nodes}
    for node in all_nodes:
        start = node.name
        ends = functools.reduce(list.__add__, node.connections.values(), )
        for end in ends:
            GG.add_edge(start, end,
                        color=COLORS_EDGE['-'.join(sorted([all_nodes_dict[start].unit_type,
                                                           all_nodes_dict[end].unit_type]))])
    
    # 展示
    options = {
        "node_size": 20,
        "alpha": 0.9
    }
    plt.figure()
    pos = {n: GG.nodes()[n]['pos'] for n in list(GG.nodes)}
    color = [GG.nodes()[n]['color'] for n in list(GG.nodes)]
    nx.draw_networkx_nodes(GG, pos, node_color=color, **options)
    plt.show()
    
    edge_color = [GG.edges()[e]['color'] for e in list(GG.edges)]
    nx.draw_networkx_edges(GG, pos, edge_color=edge_color, width=1.0, alpha=0.5)
    plt.show()
