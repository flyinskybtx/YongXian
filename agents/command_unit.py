from dataclasses import dataclass, field
from typing import Union

from .alarm_radar import AlarmRadar
from .base_unit import BaseUnit, read_decorator, request_decorator, write_decorator
from .enemy_unit import EnemyUnit
from .firing_unit import FiringUnit
from .tracking_radar import TrackingRadar


@dataclass
class CommandUnit(BaseUnit):
    connected_command_units: list = field(default_factory=list, init=False)
    connected_alarm_radars: list = field(default_factory=list, init=False)
    connected_tracking_radars: list = field(default_factory=list, init=False)
    connected_firing_units: list = field(default_factory=list, init=False)
    
    def __post_init__(self):
        super(CommandUnit, self).__post_init__()
        self.observed_set = {}
        self.enemy_set = {}
        self.tracked_set = {}
    
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
