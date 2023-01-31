import numpy as np
import yaml

from .agents import TrackingRadar, EnemyUnit, FiringUnit, CommandUnit, AlarmRadar, NetworkDefense, ElectricDefense
from .base_unit import BaseUnit


def _decode(data):
    return data.tolist() if isinstance(data, np.ndarray) else data


def _encode(data):
    return np.array(data) if isinstance(data, list) else data


def to_yaml(unit: BaseUnit):
    data = {key: _decode(unit.__getattribute__(key)) for key in unit.yaml_fields}
    return yaml.dump({unit.name: data})


UNIT_CLASS_MAPPING = {
    "火力": FiringUnit,
    "网络攻防": NetworkDefense,
    "指挥控制": CommandUnit,
    "预警探测": AlarmRadar,
    "跟踪识别": TrackingRadar,
    "电子对抗": ElectricDefense,
    "敌方单位": EnemyUnit,
}


def from_yaml(data: dict):
    name = list(data.keys())[0]
    _data = data[name]
    unit_type = _data['unit_type']
    UnitClass = UNIT_CLASS_MAPPING[unit_type]
    _data = {k: _encode(v) for k, v in _data.items()}
    _data.pop('unit_type')
    return UnitClass(name=name, **_data)
