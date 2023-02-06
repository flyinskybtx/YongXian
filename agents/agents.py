from dataclasses import dataclass, field
from typing import Union, Dict

import numpy as np

from .base_unit import BaseUnit, MISSING, write_decorator, read_decorator, request_decorator


@dataclass
class EnemyUnit(BaseUnit):
    tar_pos: np.ndarray = field(init=True, default=MISSING)
    speed: float = 7
    
    def __post_init__(self):
        super(EnemyUnit, self).__post_init__()
        self.alarmed_flag = False
        self.alive_flag = True
        self.hit_flag = False
        self.yaml_fields += ['tar_pos', 'speed']
        
        # todo: 运动曲线
    
    def update(self):
        self.info[self.t] = {'alarmed': self.alarmed_flag, }  # todo: 位置信息
        super(EnemyUnit, self).update()
    
    @property
    def cur_pos(self):
        pass
    
    def check_hit(self):
        pass
    
    def set_alarmed(self):
        self.alarmed_flag = True
    
    def set_destroyed(self):
        self.alive_flag = False


@dataclass
class AlarmRadar(BaseUnit):
    delay: int = 10
    radius: dict = field(default_factory=dict, init=True)
    connections: dict = field(default_factory=dict, init=True)
    
    # connected_alarm_radars: list = field(default_factory=list, init=False)
    # connected_command_units: list = field(default_factory=list, init=False)

    def __post_init__(self):
        super(AlarmRadar, self).__post_init__()
        self.radius = self.radius or {'预警探测': 200,
                                      '指挥控制': 200,
                                      '敌方单位': 400, }
        self.target_list = []
        self.observed_list = []
        for _type in ['预警探测', '指挥控制']:
            if _type not in self.connections:
                self.connections[_type] = []
        self.yaml_fields += ['delay', 'radius', 'connections']
    
    def update(self):
        # todo：更新预警列表
        super(AlarmRadar, self).update()
    
    # --- 敌方单元
    def is_within_range(self, enemy: EnemyUnit) -> bool:
        pass
    
    def is_alarmed(self):
        pass
    
    def update_alarmed_list(self):
        pass
    
    @property
    def num_tracking_enemies(self):
        pass
    
    # --- 指控
    @write_decorator
    def send_in_range_enemies(self, command_unit):
        pass
    
    @write_decorator
    def send_alarmed_enemies(self, command_unit):
        pass
    
    @read_decorator
    def recv_stop_enemies(self, command_unit):
        pass
    
    # --- 其他预警雷达
    @write_decorator
    def send_observed_enemies(self, alarm_radar):
        pass
    
    @read_decorator
    def recv_observed_enemies(self, alarm_radar):
        pass


@dataclass
class FiringUnit(BaseUnit):
    volume: int = 4
    radius: dict = field(default_factory=dict, init=True)
    speed: int = 7
    connections: dict = field(default_factory=dict, init=True)

    # connected_command_units: list = field(default_factory=list, init=False)
    
    def __post_init__(self):
        super(FiringUnit, self).__post_init__()
        self.radius = self.radius or {'指挥控制': 200,
                                      '敌方单位': 100, }
        self.enemy_list = []
        for _type in ['指挥控制']:
            if _type not in self.connections:
                self.connections[_type] = []
        self.yaml_fields += ['volume', 'radius', 'speed', 'connections']
    
    def update(self):
        super(FiringUnit, self).update()
    
    # --- 敌方单元
    def calculate_firing_data(self, enemy, t0):
        pass
    
    def fire(self, enemy):
        pass
    
    def is_enemy_hit(self, enemy):
        pass
    
    # --- 指控
    @read_decorator
    def recv_target_set(self, command_unit: BaseUnit):
        pass
    
    @read_decorator
    def recv_tracked_set(self, command_unit: BaseUnit, ):
        pass
    
    @read_decorator
    def recv_fire_signal(self, command_unit: BaseUnit, enemy_unit: EnemyUnit):
        pass
    
    @write_decorator
    def send_ready_signal(self, command_unit: BaseUnit):
        pass


@dataclass
class TrackingRadar(BaseUnit):
    radius: dict = field(default_factory=dict, init=True, )
    connections: dict = field(default_factory=dict, init=True)

    # connected_command_units: list = field(default_factory=list, init=False)
    # connected_tracking_radars: list = field(default_factory=list, init=False)
    
    def __post_init__(self):
        super(TrackingRadar, self).__post_init__()
        self.radius = self.radius or {'指挥控制': 200,
                                      '跟踪识别': 200,
                                      '敌方单位': 200, }
        for _type in ['跟踪识别', '指挥控制']:
            if _type not in self.connections:
                self.connections[_type] = []
        self.tracking_list = []
        self.target_list = []
        self.yaml_fields += ['radius', 'connections']
    
    def update(self):
        # todo: 更新消息
        super(TrackingRadar, self).update()
        # --- 敌方单元
    
    def is_within_range(self, enemy: EnemyUnit):
        pass
    
    # --- 指控
    @read_decorator
    def recv_target_enemies(self, command_unit: BaseUnit, ):
        pass
    
    # --- 其他跟踪
    @write_decorator
    def send_tracking_enemies(self, tracking_radar):
        pass
    
    @read_decorator
    def recv_tracking_enemies(self, tracking_radar):
        pass


@dataclass
class CommandUnit(BaseUnit):
    radius: dict = field(default_factory=dict, init=True)
    # connected_command_units: list = field(default_factory=list, init=False)
    # connected_alarm_radars: list = field(default_factory=list, init=False)
    # connected_tracking_radars: list = field(default_factory=list, init=False)
    # connected_firing_units: list = field(default_factory=list, init=False)
    connections: dict = field(default_factory=dict, init=True)

    def __post_init__(self):
        super(CommandUnit, self).__post_init__()
        self.radius = self.radius or {'指挥控制': 200,
                                      '预警探测': 200,
                                      '跟踪识别': 200,
                                      '火力': 200,
                                      '网络攻防': 200,
                                      '电子对抗': 200, }
        for _type in ['预警探测', '指挥控制', '跟踪识别', '火力']:
            if _type not in self.connections:
                self.connections[_type] = []
        self.observed_list = []
        self.enemy_list = []
        self.tracked_list = []
        self.yaml_fields += ['radius', 'connections']
    
    def update(self):
        # todo
        super(CommandUnit, self).update()
    
    # --- 预警雷达
    @read_decorator
    def recv_observed_enemies(self, alarm_radar: AlarmRadar):
        pass
    
    @read_decorator
    def recv_alarmed_enemies(self, alarm_radar: AlarmRadar):
        pass
    
    def allocate_alarm_tasks(self):
        pass
    
    def update_threats(self):
        pass
    
    # --- 跟踪雷达
    @write_decorator
    def send_enemy_set(self, unit: Union[BaseUnit, TrackingRadar]):
        """ 同时适用于 tracking_radar 和 command_unit"""
        pass
    
    @read_decorator
    def recv_tracked_signal(self, unit: Union[BaseUnit, TrackingRadar]):
        """ 同时适用于 tracking_radar 和 command_unit"""
        
        pass
    
    # --- 火力单元
    @write_decorator
    def send_target_set(self, fire_unit: FiringUnit):
        pass
    
    @request_decorator
    def request_capability_signal(self, fire_unit: FiringUnit, enemy_unit: EnemyUnit):
        pass
    
    @read_decorator
    def recv_ready_signal(self, fire_unit: FiringUnit, enemy_unit: EnemyUnit):
        pass
    
    @write_decorator
    def send_fire_signal(self, fire_unit: FiringUnit, enemy_unit: EnemyUnit):
        pass
    
    # --- 指控
    @write_decorator
    def send_threat_set(self, command_unit):
        pass
    
    @read_decorator
    def recv_threat_set(self, command_unit):
        pass
    
    @read_decorator
    def recv_enemy_set(self, command_unit):
        pass
    
    @write_decorator
    def send_tracked_set(self, command_unit):
        pass
    
    @read_decorator
    def recv_tracked_set(self, command_unit):
        pass


@dataclass
class NetworkDefense(BaseUnit):
    pass


@dataclass
class ElectricDefense(BaseUnit):
    pass
