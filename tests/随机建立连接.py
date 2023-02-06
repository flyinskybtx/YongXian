import functools
import itertools
from collections import namedtuple
from enum import unique

import numpy as np
import yaml
from tqdm import tqdm

from agents import from_yaml, to_yaml
from config import RULES


def create_network():
    pass


if __name__ == '__main__':
    enemies = from_yaml(stream='创建任务.yml', )
    allies = from_yaml(stream='创建节点.yml', )
    
    edges = []
    Edge = namedtuple('Edge', ['start', 'end'])
    
    pairs = list(itertools.combinations(list(allies.keys()), 2))
    pairs += [(k, k) for k in allies.keys()]
    
    # 先根据距离约束全连，再根据数量限制随机剪枝
    for key1, key2 in pairs:
        key1, key2 = sorted([key1, key2])
        if key1 + '-' + key2 in RULES:  # 符合连接规则
            nodes1 = allies[key1]
            nodes2 = allies[key2]
            
            for n1 in nodes1:
                # 先全连接
                connectable_n2 = [n2 for n2 in nodes2 if np.linalg.norm(n1.pos - n2.pos) <= n1.radius[
                    n2.unit_type]]  # 一定记得在类别相同时做自我排除！！
                if n1 in connectable_n2:
                    connectable_n2.remove(n1)
                
                for n2 in connectable_n2:
                    edge = '<==>'.join(sorted([n1.name, n2.name]))  # 无向图
                    if edge not in edges:
                        edges.append(edge)
    
    # 保存边
    with open('连接关系.yml', 'w') as f:
        yaml.dump(edges, f)
    
    with open('连接关系.yml', 'r') as f:
        edges = yaml.safe_load(f)
    
    # 将连接添加到节点
    all_nodes = functools.reduce(list.__add__, allies.values(), )
    all_nodes = {n.name: n for n in all_nodes}
    
    for edge in edges:
        name1, name2 = edge.split('<==>')
        n1, n2 = all_nodes[name1], all_nodes[name2]
        if n2.name not in n1.connections[n2.unit_type]:
            n1.connections[n2.unit_type].append(n2.name)
        if n1.name not in n2.connections[n1.unit_type]:
            n2.connections[n1.unit_type].append(n1.name)
    
    # 根据数量约束剪枝
    for n1 in tqdm(all_nodes.values()):
        for c_type, c_nodes in n1.connections.items():
            if c_type + '-' + n1.unit_type in RULES:
                rule = RULES[c_type + '-' + n1.unit_type]
            else:
                rule = RULES[n1.unit_type + '-' + c_type]
            if len(c_nodes) > rule:
                to_drop = np.random.choice(c_nodes, len(c_nodes) - rule, replace=False)
                for n2_name in to_drop:
                    # 双向删除边
                    all_nodes[n2_name].connections[n1.unit_type].remove(n1.name)
                    n1.connections[all_nodes[n2_name].unit_type].remove(n2_name)
    
    # 保存
    filename = '创建节点2.yml'
    stream = to_yaml(allies, filename)
