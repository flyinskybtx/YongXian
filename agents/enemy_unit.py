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
