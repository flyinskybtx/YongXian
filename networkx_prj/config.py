import numpy as np

DEFEND_AREA_RADIUS = int(1e3)
CONNECTION_RADIUS = 4e2
CONNECTION_RATE = 0.2

NAMES = ["预警探测", "跟踪识别", "指挥控制", "火力", "电子对抗", "网络攻防", ]

NUM_NODES = {
    "预警探测": 300,
    "跟踪识别": 200,
    "指挥控制": 200,
    "火力": 500,
    "电子对抗": 200,
    "网络攻防": 200,
    "敌方单位": 100,
}

# NUM_NODES = {
#    "预警探测": 300,
#    "跟踪识别": 200,
#    "指挥控制": 200,
#    "火力": 500,
#    "电子对抗": 200,
#   "网络攻防": 200,
# }
LAYERS = {
    "火力": 4,
    "网络攻防": 4,
    "指挥控制": 3,
    "预警探测": 2,
    "跟踪识别": 1,
    "电子对抗": 1,
    "敌方单位": 5,
}

SYMBOLS = {
    "火力": "circle",
    "网络攻防": "circle",
    "指挥控制": "circle",
    "预警探测": "circle",
    "跟踪识别": "circle",
    "电子对抗": "circle",
    "敌方单位": "circle",
}

COLORS = {
    "火力": "orange",
    "网络攻防": "purple",
    "指挥控制": "blue",
    "预警探测": "pink",
    "跟踪识别": "cyan",
    "电子对抗": "olive",
    "敌方单位": "green",
}

COLORS_EDGE = {
    '预警探测-预警探测': COLORS['预警探测'],
    '预警探测-指挥控制': COLORS['指挥控制'],
    '跟踪识别-指挥控制': COLORS['跟踪识别'],
    '跟踪识别-跟踪识别': COLORS['跟踪识别'],
    '指挥控制-指挥控制': COLORS['指挥控制'],
    '指挥控制-火力': COLORS['火力'],
    '电子对抗-预警探测': COLORS['电子对抗'],
    '电子对抗-跟踪识别': COLORS['电子对抗'],
    '网络攻防-指挥控制': COLORS['网络攻防'],
    "敌方单位-火力": COLORS['敌方单位'],
    "敌方单位-预警探测": COLORS['预警探测'],
    "敌方单位-跟踪识别": COLORS['跟踪识别'],
}

RULES = {
    '预警探测-预警探测': 16,
    '电子对抗-预警探测': 8,
    '预警探测-指挥控制': 32,
}

# RULES = {
# '预警探测-预警探测': 16,
# '电子对抗-预警探测': 8,
# '预警探测-指挥控制': 32,
# '指挥控制-指挥控制': 16,
# '网络攻防-指挥控制': 8,
# }

# RULES = {
# '预警探测-预警探测': 16,
# '电子对抗-预警探测': 8,
# '预警探测-指挥控制': 32,
# '指挥控制-指挥控制': 16,
# '网络攻防-指挥控制': 8,
# '跟踪识别-跟踪识别': 8,
# '跟踪识别-指挥控制': 8,
# '电子对抗-跟踪识别': 8,
# }

# RULES = {
# '预警探测-预警探测': 16,
# '电子对抗-预警探测': 8,
# '预警探测-指挥控制': 32,
# '指挥控制-指挥控制': 16,
# '网络攻防-指挥控制': 8,
# '跟踪识别-跟踪识别': 8,
# '跟踪识别-指挥控制': 8,
# '电子对抗-跟踪识别': 8,
# '指挥控制-火力': 16
# }
