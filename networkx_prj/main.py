import networkx as nx
import numpy as np
from matplotlib import pyplot as plt

# from networkx_prj.config import LAYERS
# from networkx_prj.create_scenario import build_group_edges, build_grouped_nodes, group_edges

from config import LAYERS
from create_scenario import build_group_edges, build_grouped_nodes, group_edges






def get_nodes_pos(GG, nodes_list):
    return {n: GG.nodes()[n]['pos'] for n in nodes_list}


def get_nodes_color(GG, nodes_list):
    return [GG.nodes()[n]['color'] for n in nodes_list]


def get_edges_color(GG, edges_list):
    return [GG.edges()[e]['color'] for e in list(edges_list)]


def build_group_graph(group_nodes):
    graph_dict = {}
    for group, nodes in group_nodes.items():
        G = nx.Graph(name=group)
        for node in nodes:
            G.add_node(node.id, type=group, pos=node.src_pos,
                       color=node.color, symbol=node.symbol, layer=node.layer)
        graph_dict[group] = G
    return graph_dict


def build_whole_graph(group_nodes, group_edges):
    GG = nx.Graph(name='all')
    # 节点
    for group, nodes in group_nodes.items():
        for node in nodes:
            GG.add_node(node.id, type=group, pos=node.src_pos,
                        color=node.color, symbol=node.symbol, layer=node.layer)
    # 边
    for group, edges in group_edges.items():
        for edge in edges:
            GG.add_edge(edge.start, edge.end, color=edge.color)
    return GG


def draw_networkx_graph(GG, show_nodes=True, show_edges=True, **options):
    plt.figure()
    pos = get_nodes_pos(GG, list(GG.nodes))
    node_color = get_nodes_color(GG, list(GG.nodes))
    edge_color = get_edges_color(GG, list(GG.edges))
    
    if show_nodes:
        nx.draw_networkx_nodes(GG, pos, node_color=node_color, **options)
    if show_edges:
        nx.draw_networkx_edges(GG, pos, edge_color=edge_color, width=1.0, alpha=0.5)
    
    plt.show()


def draw_matplot3d_graph(GG):
    pos = get_nodes_pos(GG, list(GG.nodes))
    node_color = get_nodes_color(GG, list(GG.nodes))
    edge_color = get_edges_color(GG, list(GG.edges))
    
    fig = plt.figure()
    ax3d = fig.add_subplot(111, projection="3d")
    ax3d.set_zlim([min(LAYERS.values()) - 1, max(LAYERS.values()) + 1])
    
    node_xyz = []
    for u in GG:
        x, y = pos[u]
        z = GG.nodes()[u]['layer']
        node_xyz.append(np.array([x, y, z]))
    node_xyz = np.array(node_xyz)
    
    edge_xyz = []
    for u, v in GG.edges():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        z1 = GG.nodes()[u]['layer']
        z2 = GG.nodes()[v]['layer']
        edge_xyz.append((np.array([x1, y1, z1]), np.array([x2, y2, z2])))
    edge_xyz = np.array(edge_xyz)
    
    ax3d.scatter(*node_xyz.T, s=10, c=node_color, alpha=0.5, )
    for vizedge, c in zip(edge_xyz, edge_color):
        ax3d.plot(*vizedge.T, color=c, alpha=0.1)
    
    fig.tight_layout()
    plt.show()


def draw_matplot3d_graph_by_group(GG, group_name):
    node_list = [n for n in list(GG.nodes) if group_name == n.split('-')[0]]
    edge_list = [(s, e) for s, e in list(GG.edges) if group_name == s.split('-')[0] or group_name == e.split('-')[0]]
    
    fig = plt.figure()
    ax3d = fig.add_subplot(111, projection="3d")
    ax3d.set_zlim([min(LAYERS.values()) - 1, max(LAYERS.values()) + 1])
    
    pos = get_nodes_pos(GG, list(GG.nodes))
    node_color = get_nodes_color(GG, node_list)
    edge_color = get_edges_color(GG, edge_list)
    
    node_xyz = []
    for u in node_list:
        x, y = pos[u]
        z = GG.nodes()[u]['layer']
        node_xyz.append(np.array([x, y, z]))
    node_xyz = np.array(node_xyz)
    
    edge_xyz = []
    for u, v in edge_list:
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        z1 = GG.nodes()[u]['layer']
        z2 = GG.nodes()[v]['layer']
        edge_xyz.append((np.array([x1, y1, z1]), np.array([x2, y2, z2])))
    edge_xyz = np.array(edge_xyz)
    
    ax3d.scatter(*node_xyz.T, s=10, c=node_color, alpha=0.5, )
    for vizedge, c in zip(edge_xyz, edge_color):
        ax3d.plot(*vizedge.T, color=c, alpha=0.1)
    
    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    group_nodes = build_grouped_nodes()
    group_edges = build_group_edges(group_nodes)
    
    options = {
        "node_size": 20,
        "alpha": 0.9
    }
    
    whole_graph = build_whole_graph(group_nodes, group_edges)
    
    draw_networkx_graph(whole_graph, **options)
    draw_matplot3d_graph(whole_graph)
    
    # ------------
    for group_name in group_nodes.keys():
        draw_matplot3d_graph_by_group(whole_graph, group_name)
