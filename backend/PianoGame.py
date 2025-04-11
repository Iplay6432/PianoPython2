import pyglet

class PianoGame:
    def __init__(self, window):
        self.window = window
        self.Start = False
        self.level = 0
    def key_pressed(self, symbol, modifiers):
        pass
    def start(self):
        self.Start = True
    def draw(self):
      print("wow!")
      pass
    def set_level(self, level: int):
        self.level = level        
        