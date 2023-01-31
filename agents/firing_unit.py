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
