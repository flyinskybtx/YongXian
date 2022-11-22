from copy import deepcopy

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

radar_pos = create_random_pos(NUM_RADAR, DEFEND_RADIUS, )
missile_pos = create_random_pos(NUM_MISSILE, DEFEND_RADIUS, )
commander_pos = create_random_pos(NUM_COMMANDER, DEFEND_RADIUS, )

# eg_radar_pos = create_pheudo_random_pos(NUM_RADAR, DEFEND_RADIUS, )
# eg_missile_pos = create_pheudo_random_pos(NUM_MISSILE, DEFEND_RADIUS, )
# eg_commander_pos = create_pheudo_random_pos(NUM_COMMANDER, DEFEND_RADIUS, )

# radar_nodes = create_plotly_nodes("radar", radar_pos, 10, '#636efa', RADAR_Z, 'circle')
# commander_nodes = create_plotly_nodes("commander", commander_pos, 10, '#EF553B', COMMANDER_Z, 'square')
# missile_nodes = create_plotly_nodes("missile", missile_pos, 5, '#00cc96', MISSILE_Z, 'diamond')

radars = []
for i, pos in enumerate(radar_pos):
    radars.append(Radar(f'r{i}', pos, ))

commanders = []
for i, pos in enumerate(commander_pos):
    commanders.append(Commander(f'c{i}', pos, ))

missiles = []
for i, pos in enumerate(missile_pos):
    missiles.append(Missile(f'm{i}', pos, ))

sources = np.random.uniform(0, 2 * np.pi, NUM_ENEMY)
targets = np.random.uniform(0, 2 * np.pi, NUM_ENEMY)
sources = np.stack([np.sin(sources), np.cos(sources)]).T * BATTLE_GROUD_SIZE
targets = np.stack([np.sin(targets), np.cos(targets)]).T * DEFEND_RADIUS / 2
enemies = []
for i, (source, target) in enumerate(zip(sources, targets)):
    enemies.append(Enemy(f'e{i}', source, target))

# 建立边连接关系
for r in radars:
    connected_commanders = []
    for commander in commanders:
        if np.linalg.norm(r.pos - commander.pos) < R2C_DIST:
            connected_commanders.append(commander)
    r.connected_commanders = connected_commanders

for c in commanders:
    connected_commanders = []
    for commander in commanders:
        if np.linalg.norm(c.pos - commander.pos) < C2C_DIST:
            connected_commanders.append(commander)
    c.connected_commanders = connected_commanders
    connected_missiles = []
    for missile in missiles:
        if np.linalg.norm(c.pos - missile.pos) < C2M_DIST:
            connected_missiles.append(missile)
    c.connected_missiles = connected_missiles

edges = {}
nodes = {}
for radar in radars:
    x, y = radar.pos
    z = RADAR_Z
    nodes[radar._id] = go.Scatter3d(name=radar._id, x=[x], y=[y, ], z=[z], mode='markers',
                                    showlegend=False,
                                    marker={'color': '#636efa', 'size': 10, 'symbol': 'circle'}, )
    for commander in radar.connected_commanders:
        x_c, y_c = commander.pos
        z_c = COMMANDER_Z
        edges[radar._id + '-' + commander._id] = go.Scatter3d(x=[x, x_c], y=[y, y_c], z=[z, z_c], mode='lines',
                                                              showlegend=False,
                                                              line={'width': 2, 'color': '#636efa', })
for commander in commanders:
    x, y = commander.pos
    z = COMMANDER_Z
    nodes[commander._id] = go.Scatter3d(name=commander._id, x=[x], y=[y, ], z=[z], mode='markers',
                                        showlegend=False,
                                        marker={'color': '#ffa15a', 'size': 10, 'symbol': 'square'}, )
    for _commander in commander.connected_commanders:
        x_c, y_c = _commander.pos
        z_c = COMMANDER_Z
        edges[commander._id + '-' + _commander._id] = go.Scatter3d(x=[x, x_c], y=[y, y_c], z=[z, z_c], mode='lines',
                                                                   showlegend=False,
                                                                   line={'width': 2, 'color': '#ffa15a', })
    for missile in commander.connected_missiles:
        x_c, y_c = missile.pos
        z_c = MISSILE_Z
        edges[commander._id + '-' + missile._id] = go.Scatter3d(x=[x, x_c], y=[y, y_c], z=[z, z_c], mode='lines',
                                                                showlegend=False,
                                                                line={'width': 2, 'color': '#00cc96', })

for missile in missiles:
    x, y = missile.pos
    z = MISSILE_Z
    nodes[missile._id] = go.Scatter3d(name=missile._id, x=[x], y=[y, ], z=[z], mode='markers',
                                      showlegend=False,
                                      marker={'color': '#00cc96', 'size': 5, 'symbol': 'diamond'}, )
# 图例占位的
# nodes['eg.radar'] = go.Scatter3d(name='radar', x=[0], y=[0], z=[RADAR_Z], mode='markers',
#                                  showlegend=True,
#                                  marker={'color': '#636efa', 'size': 0, 'symbol': 'diamond'}, )
# nodes['eg.commander'] = go.Scatter3d(name='commander', x=[0], y=[0], z=[COMMANDER_Z], mode='markers',
#                                      showlegend=True,
#                                      marker={'color': '#ffa15a', 'size': 0, 'symbol': 'diamond'}, )
# nodes['eg.missile'] = go.Scatter3d(name='missile', x=[0], y=[0], z=[MISSILE_Z], mode='markers',
#                                    showlegend=True,
#                                    marker={'color': '#00cc96', 'size': 0, 'symbol': 'diamond'}, )

if __name__ == '__main__':
    layout = go.Layout(
        xaxis=dict(range=[-DEFEND_RADIUS, DEFEND_RADIUS], autorange=False),
        yaxis=dict(range=[-DEFEND_RADIUS, DEFEND_RADIUS], autorange=False),
        title="涌现",
        # hovermode="closest",
        legend=dict(title="图例"),
        # {'#00cc96':'missile','#ffa15a':'commander','#636efa':'radar',},
        updatemenus=[
            dict(
                type="buttons",
                buttons=[
                    dict(label="Play",
                         method="animate",
                         args=[None,
                               # {"frame": {"duration": 500, "redraw": False},
                               #  "fromcurrent": True, "transition": {"duration": 300, }},
                               ]),
                    # dict(label="Pause",
                    #      method="animate",
                    #      args=[[None], {"frame": {"duration": 0, "redraw": False},
                    #                     "mode": "immediate",
                    #                     "transition": {"duration": 0}}]),
                ],
                # direction="left",
                # pad={"r": 10, "t": 87},
                # showactive=False,
                # x=0.1,
                # y=0,
                # xanchor="right",
                # yanchor="top"
            ),
        ],
    )
    fig_nodes = deepcopy(nodes)
    fig_edges = deepcopy(edges)
    k = [k for k in fig_nodes.keys() if k.startswith('r')][0]
    fig_nodes[k].name = 'radar'
    fig_nodes[k].showlegend = True
    k = [k for k in fig_nodes.keys() if k.startswith('c')][0]
    fig_nodes[k].name = 'commander'
    fig_nodes[k].showlegend = True
    k = [k for k in fig_nodes.keys() if k.startswith('m')][0]
    fig_nodes[k].name = 'missile'
    fig_nodes[k].showlegend = True
    
    fig_data = list(fig_nodes.values()) + list(fig_edges.values())
    # fig_data = [radar_nodes, commander_nodes, missile_nodes] + list(nodes.values()) + list(edges.values())
    
    fig_frames = []
    
    key = np.random.choice([k for k in nodes.keys() if k.startswith('r')])
    print(key)
    # Node
    frame_edges = deepcopy(edges)
    frame_nodes = deepcopy(nodes)
    frame_nodes[key].marker.color = "#ef553b"
    frame_data = list(frame_edges.values()) + list(frame_nodes.values())
    fig_frames.append(
        go.Frame(data=frame_data)
    )
    
    for _ in range(3):
        # Edge
        frame_edges = deepcopy(edges)
        frame_nodes = deepcopy(nodes)
        avail_keys = [k for k in frame_edges.keys() if k.split('-')[0] == key]
        # p = list(map(lambda x: 1 if x.split('-')[0].startswith('c') else 0, avail_keys))
        # p = p / np.sum(p)
        avail_keys = [k for k in avail_keys if k.split('-')[1].startswith('c')]
        key = np.random.choice(avail_keys)
        print(key)
        
        frame_edges[key].line.color = "#ef553b"
        frame_edges[key].line.width = 5
        frame_data = list(frame_edges.values()) + list(frame_nodes.values())
        fig_frames.append(
            go.Frame(data=frame_data)
        )
        
        # Node
        key = key.split('-')[-1]
        print(key)
        frame_edges = deepcopy(edges)
        frame_nodes = deepcopy(nodes)
        frame_nodes[key].marker.color = "#ef553b"
        frame_data = list(frame_edges.values()) + list(frame_nodes.values())
        fig_frames.append(
            go.Frame(data=frame_data)
        )
        
        if key.startswith('m'):
            break
    
    # Edge
    frame_edges = deepcopy(edges)
    frame_nodes = deepcopy(nodes)
    avail_keys = [k for k in frame_edges.keys() if k.split('-')[0] == key]
    # p = list(map(lambda x: 1 if x.split('-')[0].startswith('c') else 0, avail_keys))
    # p = p / np.sum(p)
    avail_keys = [k for k in avail_keys if k.split('-')[1].startswith('m')]
    key = np.random.choice(avail_keys)
    print(key)
    
    frame_edges[key].line.color = "#ef553b"
    frame_edges[key].line.width = 5
    frame_data = list(frame_edges.values()) + list(frame_nodes.values())
    fig_frames.append(
        go.Frame(data=frame_data)
    )
    
    # Node
    key = key.split('-')[-1]
    print(key)
    frame_edges = deepcopy(edges)
    frame_nodes = deepcopy(nodes)
    frame_nodes[key].marker.color = "#ef553b"
    frame_data = list(frame_edges.values()) + list(frame_nodes.values())
    fig_frames.append(
        go.Frame(data=frame_data)
    )
    #
    fig = go.Figure(
        data=fig_data,
        layout=layout,
        frames=fig_frames,
    )
    fig.show("browser")
