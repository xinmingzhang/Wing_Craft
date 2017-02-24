from . import enemy
from . import explosion
from ..prepare import MAP1,MAP2,MAP3,MAP4,MAP5

transfor_dict = {'1': enemy.Private0,
                 '2': enemy.Private1,
                 '3': enemy.Corporal0,
                 '4': enemy.Sergeant0,
                 '5': enemy.Sergeant1,
                 '6': enemy.SecondLieutenant0,
                 '7': enemy.SecondLieutenant1,
                 '8': enemy.FirstLieutenant0,
                 '9': enemy.FirstLieutenant1,
                 '10': enemy.Captain0,
                 '11': enemy.Captain1,
                 '12': enemy.Major0,
                 '13': enemy.Major1,
                 '14': enemy.Colonel0,
                 '15': enemy.Colonel1,
                 '16': enemy.Boss1,
                 '17': enemy.Boss2,
                 '18': enemy.Boss3,
                 '19': enemy.Boss4,
                 '20': enemy.Boss5,
                 '21': explosion.Emerge1,
                 '22': explosion.Emerge2,
                 '23': explosion.WarningSign}


def get_enemies_from_map(game,frame,level):
        if level == 1:
            map = MAP1
        elif level == 2:
            map = MAP2
        elif level == 3:
            map = MAP3
        elif level == 4:
            map = MAP4
        elif level == 5:
            map = MAP5
        enemy = map.get(str(frame))
        if enemy is None:
            return
        else:
            for key in enemy.keys():
                return transfor_dict.get(key)(game,enemy[key])
