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


if __name__ == '__main__':
    radar = AlarmRadar(name="预警探测-1", pos=np.array([1, 2, 3]), delay=10, radius=100)
    print(radar.__dict__)
