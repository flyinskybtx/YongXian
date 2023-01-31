## 存储、读取

```python
nx.write_edgelist(G, path="grid.edgelist", delimiter=":")
H = nx.read_edgelist(path="grid.edgelist", delimiter=":")
```

## 画图

```python
nx.draw(H, pos)
nx.draw(G, pos=pos, with_labels=True)
plt.show()

options = {
    "font_size": 36,
    "node_size": 3000,
    "node_color": "white",
    "edgecolors": "black",
    "linewidths": 5,
    "width": 5,
}
nx.draw_networkx(G, pos, **options)
```

## 显示

```python
ax = plt.gca()
ax.margins(0.20)
plt.axis("off")
plt.show()
```

## 取节点

```python
list(G.nodes)
list(G.edges)
list(G.adj[1])
G.degree[1] 
```

## 添加

点

```python
G.add_nodes_from([
    (4, {"color": "red"}),
    (5, {"color": "green"}),
])
G.add_nodes_from(H)
```

边

```python
G.add_edge(1, 2)

e = (2, 3)
G.add_edge(*e)  # unpack edge tuple*

G.add_edges_from([(1, 2), (1, 3)])
G.add_edges_from([(2, 3, {'weight': 3.1415})])

G.add_edge(n1, n2, object=x)  # object可以是各种对象
```

## 删除

```python
G.remove_node(2)
G.remove_nodes_from("spam")
G.remove_edge(1, 3)
G.clear()
```



## 设置位置

```python
pos = {1: (0, 0), 2: (-1, 0.3), 3: (2, 0.17), 4: (4, 0.255), 5: (5, 0.03)}
pos = nx.spring_layout(H, seed=200)
```

