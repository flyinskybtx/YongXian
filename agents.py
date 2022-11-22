from dataclasses import dataclass, field
from typing import List

import numpy as np


@dataclass
class Radar:
    _id: str
    pos: np.ndarray
    detect_dist: float = 2e2
    connected_commanders: list = field(init=False)
    _activated: bool = field(init=False)
    t: int = 0
    
    def can_detect(self, enemy):
        if enemy.pos is None:
            return False
        else:
            return np.linalg.norm(enemy.pos - self.pos) < self.detect_dist
    
    def update(self, enemy_list: List):
        self.t += 1
        detected_enemy_list = [e for e in enemy_list if self.can_detect(e)]
        if len(detected_enemy_list) > 0:
            self._activated = True
            self.broadcast(detected_enemy_list)
        else:
            self._activated = False
    
    def broadcast(self, enemy_list):
        for commander in self.connected_commanders:
            commander.receive_enemy(enemy_list)


@dataclass
class Missile:
    _id: str
    pos: np.ndarray
    amount: int = 10
    _activated: bool = field(init=False)
    aim_dist: float = 1e2
    t: int = 0
    
    def update(self):
        self.t += 1
    
    def is_avail(self, enemy_pos):
        return np.linalg.norm(enemy_pos - self.pos) < self.aim_dist and self.amount > 0
    
    def launch(self, enemy):
        self._activated = True
        enemy.set_destroyed()
        self.amount -= 1
    

@dataclass
class Enemy:
    _id: str
    start_pos: np.ndarray
    target_pos: np.ndarray
    vel: float = 3
    t0: int = 0
    te: int = field(init=False)
    traj: np.ndarray = field(init=False)
    _destroyed: bool = field(init=False)
    t: int = 0
    
    def __post_init__(self):
        steps = np.round(np.linalg.norm(self.target_pos - self.start_pos) / self.vel).astype(int)
        self.traj = np.linspace(self.start_pos, self.target_pos, steps + 1)
        self.te = self.t0 + self.traj.shape[0] - 1
        self._destroyed = False
    
    def update(self):
        self.t += 1
        if self.t >= self.te:
            self._destroyed = True
    
    @property
    def pos(self):
        if not self._destroyed and self.t >= self.t0:
            return self.traj[self.t - self.t0]
        else:
            return None
    
    @property
    def past_traj(self):
        if not self._destroyed and self.t >= self.t0:
            return self.traj[:min(self.t, self.te) - self.t0]
        else:
            return None
    
    def set_destroyed(self):
        self._destroyed = True


@dataclass
class Commander:
    _id: str
    pos: np.ndarray
    connect_dist: float = 4e2
    _activated: bool = field(init=False)
    connected_commanders: list = field(init=False)
    connected_missiles: list = field(init=False)
    active_list: list = field(default_factory=lambda: [])
    inactive_list: list = field(default_factory=lambda: [])
    received_list: list = field(default_factory=lambda: [])
    t: int = 0
    
    def receive_enemy(self, enemy_list):
        for enemy in enemy_list:
            if enemy not in self.received_list:
                self.received_list.append(enemy)
    
    def decide_enemy(self, enemy):
        """决策"""
        action = np.random.choice(
            [self.fire, self.postpone, self.transfer], p=np.array([0.2, 0.2, 0.6])
        )
        return action
    
    def update(self):
        self.t += 1
        # 更新active_list 和 inactive_list
        for enemy in self.received_list:
            if enemy in self.inactive_list and enemy not in self.active_list:
                self.active_list.append(enemy)
        
        # 决策
        for enemy in self.active_list:
            action = self.decide_enemy(enemy)
            action(enemy)
        
        self._activated = True if len(self.active_list) else False
        
        # 清空
        self.received_list = []
    
    def fire(self, enemy):
        avail_missiles = [m for m in self.connected_missiles if m.is_avail(enemy.pos_t(self.t))]
        if len(avail_missiles):
            missile = np.random.choice(avail_missiles)  # 随机选一个
            missile.launch(enemy)
        else:
            self.transfer(enemy)
        self.active_list.remove(enemy)
        self.inactive_list.append(enemy)
    
    def postpone(self, enemy):
        pass
    
    def transfer(self, enemy):
        next_commander = np.random.choice(self.connected_commanders)
        next_commander.receive_enemy([enemy])
        self.active_list.remove(enemy)
        self.inactive_list.append(enemy)
