import numpy as np
import plotly.graph_objects as go


def create_pheudo_random_pos(numbers, radius, circle_split=8):
    thetas = (np.arange(numbers) + np.random.uniform(-0.5, 0.5, numbers)) * 2 * np.pi / circle_split
    factors = np.array([i // circle_split + np.random.rand() for i in range(numbers)]) * circle_split / numbers
    x = np.cos(thetas) * factors * radius
    y = np.sin(thetas) * factors * radius
    pos = np.stack([x, y])
    return pos.T


def create_random_pos(numbers, half_length):
    return np.random.uniform(-1, 1, (numbers, 2)) * half_length


def create_plotly_nodes(name, pos, size, color='#636efa', z=0, symbol='circle'):
    return go.Scatter3d(name=name, x=pos[:, 0], y=pos[:, 1],
                        z=z * np.ones(pos.shape[0]),
                        mode='markers',
                        marker={
                            'color': color,
                            'size': size * np.ones(pos.shape[0]),
                            'symbol': symbol}, )
