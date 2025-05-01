import argparse
import pyglet
from pyglet import shapes
from backend.Levels import Levels
from backend.PianoGame import PianoGame


class Main(pyglet.window.Window):
    def __init__(self):
        super().__init__(fullscreen=True)

        self.label = pyglet.text.Label("Main Window", x=10, y=self.height - 20)
        self.parser = argparse.ArgumentParser(
            prog="PianoPython2",
            description="A piano video game",
            epilog="Imagine not knowing what everything does",
        )
        self.levels = Levels(self)
        self.game = PianoGame(self)
        self.screenNumber = self.get_input_screen()
        self.happend = False

    def on_draw(self):
        self.clear()
        if int(self.get_screen()) == 0:
            end = self.levels.isEnded()
            if end[0]:
                self.screenNumber = str(1) + str(end[1])
            self.levels.draw()
        elif int(list(str(self.get_screen()))[0]) == 1:
            level = list(str(self.get_screen()))[1]
            if not self.happend:
                self.game.start(level)
                self.happend = True
            temp = self.game.draw()
            if temp == True:
                self.game.stop()
                self.levels.reset()
                del self.game
                del self.levels
                self.levels = Levels(self)
                self.game = PianoGame(self)
                self.happend = False
                self.screenNumber = 0 
    def on_key_press(self, symbol, modifiers):
        if int(self.get_screen()) == 0:
            self.levels.key_pressed(symbol, modifiers)
        elif int(list(str(self.get_screen()))[0]) == 1:
            if symbol != 65307: #65307 = esc
                self.game.key_pressed(symbol, modifiers)
            else:
                self.game.stop()
                self.levels.reset()
                del self.game
                del self.levels
                self.levels = Levels(self)
                self.game = PianoGame(self)
                self.happend = False
                self.screenNumber = 0    
    def on_key_release(self, symbol, modifiers):
        if int(list(str(self.get_screen()))[0]) == 1:
            self.game.key_released(symbol, modifiers)

    def get_screen(self) -> int:
        return self.screenNumber

    def set_screen(self, screenNumber: int) -> int:
        self.screenNumber = screenNumber
        return self.screenNumber

    def get_input_screen(self) -> int:  # 0: Levels 1: Freeplay 2: Game
        self.parser.add_argument("-s", "--screen")
        args = self.parser.parse_args()
        return args.screen


if __name__ == "__main__":
    window = Main()
    pyglet.app.run()
