import pyglet
from pyglet import shapes
from backend.Levels import Levels
from backend.PianoGame import PianoGame


class Main(pyglet.window.Window):
    def __init__(self):
        super().__init__(fullscreen=True)

        self.label = pyglet.text.Label("Main Window", x=10, y=self.height - 20)
        self.set_visible(False)
        self.levels = Levels(self)
        self.game = PianoGame(self)
        self.screenNumber = 0
        self.happend = False
        self.do_draw = False
        self.done = False
    def hide(self):
        del self.game
        del self.levels
        self.levels = Levels(self)
        self.game = PianoGame(self)
        self.happend = False
        self.screenNumber = 0
        self.do_draw = False
        self.set_visible(False)
    def show(self):
        self.done = False
        self.happend = False
        self.levels.reset()
        del self.game
        del self.levels
        self.levels = Levels(self)
        self.game = PianoGame(self)
        self.happend = False
        self.screenNumber = 0
        self.do_draw = True
        self.set_visible(True)
    def freeplay(self):
        self.done = False
        self.happend = False
        self.levels.reset()
        del self.game
        del self.levels
        self.levels = Levels(self, freeplay = True)
        self.game = PianoGame(self)
        self.happend = False
        self.screenNumber = 0
        self.do_draw = True
        self.set_visible(True)
    def getDone(self):
        return self.done 
    def on_draw(self):
        if self.do_draw:
            self.clear()
            if int(self.get_screen()) == 0:
                end = self.levels.isEnded()
                if end[0]:
                    self.screenNumber = str(1) + str(end[1])
                self.levels.draw()
            elif int(list(str(self.get_screen()))[0]) == 1:
                if not self.happend:
                    temp = ""
                    level = list(str(self.get_screen()))[1:]
                    for i in level:
                        temp += i
                    self.game.start(temp)
                    self.happend = True
                draw = self.game.draw()
                if draw[0] == True:
                    self.levels.reset()
                    del self.game
                    del self.levels
                    self.levels = Levels(self, last_score=draw[1])
                    self.game = PianoGame(self)
                    self.happend = False
                    self.screenNumber = 0 
    def on_key_press(self, symbol, modifiers):
        if self.do_draw:
            if int(self.get_screen()) == 0:
                if symbol != 65307: #65307 = esc
                    self.levels.key_pressed(symbol, modifiers)
                else:
                    self.done = True
                
            elif int(list(str(self.get_screen()))[0]) == 1:
                if symbol != 65307: #65307 = esc
                    self.game.key_pressed(symbol, modifiers)
                else:     
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

if __name__ == "__main__":
    window = Main()
    pyglet.app.run()
