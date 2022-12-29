import random

from pyecharts import options as opts
from pyecharts.charts import GraphGL

nodes = []
for i in range(3):
    for j in range(3):
        nodes.append(opts.GraphGLNode(
            x=random.random() * 10,
            y=random.random() * 20,
            value=f'{i}-{j}',
            itemstyle_opts=opts.ItemStyleOpts(
                color="rgba(255,255,0,0.8)",
                border_radius=5,
                border_width=2,
                border_color="rgba(255,0,0,0.8)",
                area_color="rgba(255,0,0,0.8)",
            ),
        ))

links = []
for i in range(3):
    for j in range(3):
        if i < 3 - 1:
            links.append(opts.GraphGLLink(
                source=i + j * 5,
                target=i + 1 + j * 5,
                value=i,
                linestyle_opts=opts.LineStyleOpts(color="rgba(0,255,255,0.8)", width=3),
            ))
        if j < 3 - 1:
            links.append(opts.GraphGLLink(
                source=i + j * 5,
                target=i + (j + 1) * 5,
                value=i,
                linestyle_opts=opts.LineStyleOpts(color="rgba(255,0,255,0.8)", width=3),
            ))

g = GraphGL(init_opts=opts.InitOpts())
g.add(
    series_name="第一类",
    nodes=nodes,
    links=links,
    symbol="diamond",
    symbol_size=20,
    force_atlas2_opts=opts.GraphGLForceAtlas2Opts(
        steps=1,
        stop_threshold=10,
        edge_weight_influence=4,
    ),
    z_level=1,

)

g.set_dark_mode()
g.render("basic_graphgl.html")

print(len(links), len(nodes))
