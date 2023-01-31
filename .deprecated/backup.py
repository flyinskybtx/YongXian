
enemy_nodes = []
for enemy in enemies:
    if enemy.src_pos is not None:
        x, y = enemy.src_pos
        _nodes = [go.Scatter3d(x=[x], y=[y], z=[z], mode='markers', showlegend=False,
                               marker={'color': '#19d3f3',
                                       'size': 5,
                                       'symbol': 'diamond', },
                               ) for z in [10, 0, -10]]
        enemy_nodes += _nodes

enemy_trajs = []
for enemy in enemies:
    if not enemy._destroyed:
        x, y = enemy.past_traj.T
        _edges = [go.Scatter3d(x=x, y=y, z=z * np.ones_like(x), mode='lines', showlegend=False,
                               line={'width': 2, 'color': '#19d3f3', },
                               ) for z in [10, 0, -10]]
        enemy_trajs += _edges

frame_data += enemy_nodes
frame_data += enemy_trajs
fig_frames.append(
    go.Frame(data=frame_data)
)

# for t in trange(10):
#     # 更新
#     for enemy in enemies:
#         enemy.update()
#
#     for radar in radars:
#         radar.update(enemies)
#
#     for commander in commanders:
#         commander.update()
#
#     for missile in missiles:
#         missile.update()
#
#     # 显示

# ------------------------------------------------
