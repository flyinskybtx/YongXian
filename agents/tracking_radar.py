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
