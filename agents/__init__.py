import functools
import itertools
from typing import Sequence, Dict, Union

import numpy as np
import yaml

from .agents import TrackingRadar, EnemyUnit, FiringUnit, CommandUnit, AlarmRadar, NetworkDefense, ElectricDefense
from .base_unit import BaseUnit

UNIT_CLASS_MAPPING = {
    "火力": FiringUnit,
    "网络攻防": NetworkDefense,
    "指挥控制": CommandUnit,
    "预警探测": AlarmRadar,
    "跟踪识别": TrackingRadar,
    "电子对抗": ElectricDefense,
    "敌方单位": EnemyUnit,
}


def _decode(data):
    return data.tolist() if isinstance(data, np.ndarray) else data


def _encode(data):
    return np.array(data) if isinstance(data, list) else data


def to_yaml(units: Union[Dict, Sequence[BaseUnit]], filename=None):
    if isinstance(units, dict):
        return to_yaml(functools.reduce(list.__add__, units.values(), ), filename)
    else:
        data = {}
        for unit in units:
            data.update({
                unit.name: {key: _decode(unit.__getattribute__(key)) for key in unit.yaml_fields}
            })
        if filename:
            with open(filename, 'w') as fp:
                return yaml.dump(data, stream=fp)
        return yaml.dump(data)


def from_yaml(stream):
    if stream.endswith('.yml'):
        with open(stream, 'r') as fp:
            data = yaml.safe_load(fp)
    else:
        data = yaml.safe_load(stream)
    
    names = list(data.keys())
    units = []
    for name in names:
        _data = data[name]
        unit_type = _data['unit_type']
        UnitClass = UNIT_CLASS_MAPPING[unit_type]
        _data = {k: _encode(v) for k, v in _data.items()}
        _data.pop('unit_type')
        units.append(UnitClass(name=name, **_data))
    
    all_nodes = {k: list(v) for k, v in itertools.groupby(units, lambda unit: unit.unit_type)}
    return all_nodes
