from random import choice
from DungeonEscape.entities.enemies.demon_red import DemonRed
# from DungeonEscape.entities.enemies.skeleton_archer import SkeletonArcher
# from DungeonEscape.entities.enemies.slime_blue import SlimeBlue

def get_enemies_for_stage(stage: int, positions: list, wave: int = 1):
    enemies = []

    base_hp = 40 + (stage - 1) * 10 + (wave - 1) * 5
    base_dmg = 10 + (stage - 1) * 2 + (wave - 1) * 1
    base_speed = 1.2 + (stage - 1) * 0.1 + (wave - 1) * 0.05

    count = min(2 + wave + stage, len(positions))

    # stage
    enemy_types = [DemonRed]
    if stage >= 3:
        # enemy_types.append(SkeletonArcher)
        pass
    if stage >= 5:
        # enemy_types.append(SlimeBlue)
        pass

    for i in range(count):
        x, y = positions[i]
        EnemyClass = choice(enemy_types)
        enemy = EnemyClass(x, y)
        enemy.health = base_hp
        enemy.damage = base_dmg
        enemy.speed = base_speed
        enemies.append(enemy)

    return enemies