from . import prepare,tools
from .states import game, warning, title, control, select,scoreboard,entername,gameover

def main():
    controller = tools.Control(prepare.ORIGINAL_CAPTION)
    states = {'WARNING':warning.Warnings(),
              'TITLE':title.Title(),
              'CONTROL':control.Control(),
              'LEVEL1':game.Game(1),
              'LEVEL2': game.Game(2),
              'LEVEL3': game.Game(3),
              'LEVEL4': game.Game(4),
              'LEVEL5': game.Game(5),
              'SELECT':select.Select(),
              'SCORE':scoreboard.Scoreboard(),
              'LEVEL6':gameover.GameOver(),
              'NAME':entername.EnterName()}
    controller.setup_states(states, 'WARNING')
    controller.main()
