import numpy as np

from networkx_prj.config import *

from agents import *

if __name__ == '__main__':
    def get_enemy_poses_random(num, radius, ):
        theta = np.random.uniform(-np.pi, np.pi, num)
        poses = np.stack([np.cos(theta), np.sin(theta)]).T * radius
        return poses
    
    def generate_tasks(num, end_time):
        poses = get_enemy_poses_random(num, DEFEND_AREA_RADIUS * 2)
        start_times = np.random.randint(0, end_time, num, dtype=int)
        tar_poses = np.random.uniform(-1, 1, size=(num, 2)) * DEFEND_AREA_RADIUS / 2
        return poses, tar_poses, start_times
    
    tasks = []
    
    for i, (pos, tar_pos, start) in enumerate(zip(*generate_tasks(num=NUM_NODES['敌方单位'], end_time=100))):
        name = f'敌方单位-{i:03d}'
        enemy_unit = EnemyUnit(name=name, pos=pos, tar_pos=tar_pos)
        tasks.append(enemy_unit)
    
    stream = to_yaml(tasks[0])
    print(stream)
    
    data = yaml.safe_load(stream)
    print(from_yaml(data))
    

