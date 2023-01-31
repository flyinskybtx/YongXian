from dataclasses import dataclass, field

import numpy as np

from .base_unit import BaseUnit, read_decorator, request_decorator, write_decorator
from .enemy_unit import EnemyUnit


@dataclass
class AlarmRadar(BaseUnit):
    delay: int = 10
    radius: float = 500
    connected_alarm_radars: list = field(default_factory=list, init=False)
    connected_command_units: list = field(default_factory=list, init=False)
    
    def __post_init__(self):
        super(AlarmRadar, self).__post_init__()
        self.targets = {}
        self.observed_list = []
    
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


from dataclasses import dataclass, field

import numpy as np

from .base_unit import BaseUnit, read_decorator, request_decorator, write_decorator


@dataclass
class EnemyUnit(BaseUnit):
    tar_pos: np.ndarray = field(init=False)
    speed: float = 7
    
    def __post_init__(self):
        super(EnemyUnit, self).__post_init__()
        self.alarmed = False
        self.alive = True
        self.hit = False
        # todo: 运动曲线
    
    def update(self):
        self.info[self.t] = {'alarmed': self.alarmed, }  # todo: 位置信息
        super(EnemyUnit, self).update()
    
    @property
    def cur_pos(self):
        pass
    
    def check_hit(self):
        pass
    
    def set_alarmed(self):
        self.alarmed = True
    
    def set_destroyed(self):
        self.alive = False


from dataclasses import dataclass, field

from .base_unit import BaseUnit, read_decorator, write_decorator
from .tracking_radar import CommandUnit
from .enemy_unit import EnemyUnit


@dataclass
class FiringUnit(BaseUnit):
    volume: int = 4
    radius: int = 100
    speed: int = 7
    connected_command_units: list = field(default_factory=list, init=False)
    
    def __post_init__(self):
        super(FiringUnit, self).__post_init__()
        self.enemy_firing_data = {}
        self.enemy_set = {}
    
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
    def recv_target_set(self, command_unit: CommandUnit):
        pass
    
    @read_decorator
    def recv_tracked_set(self, command_unit: CommandUnit, ):
        pass
    
    @read_decorator
    def recv_fire_signal(self, command_unit: CommandUnit, enemy_unit: EnemyUnit):
        pass
    
    @write_decorator
    def send_ready_signal(self, command_unit: CommandUnit):
        pass


from dataclasses import dataclass, field

from .base_unit import BaseUnit, read_decorator, write_decorator
from .command_unit import CommandUnit
from .enemy_unit import EnemyUnit


@dataclass
class TrackingRadar(BaseUnit):
    radius: float = 200
    connected_command_units: list = field(default_factory=list, init=False)
    connected_tracking_radars: list = field(default_factory=list, init=False)
    
    def __post_init__(self):
        super(TrackingRadar, self).__post_init__()
        
        self.tracking_enemies = {}
        self.target_enemies = {}
    
    def update(self):
        # todo: 更新消息
        super(TrackingRadar, self).update()
        # --- 敌方单元
    
    def is_within_range(self, enemy: EnemyUnit):
        pass
    
    # --- 指控
    @read_decorator
    def recv_target_enemies(self, command_unit: CommandUnit, ):
        pass
    
    # --- 其他跟踪
    @write_decorator
    def send_tracking_enemies(self, tracking_radar):
        pass
    
    @read_decorator
    def recv_tracking_enemies(self, tracking_radar):
        pass