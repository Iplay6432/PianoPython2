import pyglet
import mido
import json
from backend.Piano import PianoKeyboard
import pyglet.window.key as key

class PianoGame:
    def __init__(self, window):
        self.window = window
        self.Start = False
        self.level = 1
        self.p = PianoKeyboard(self.window)

    def key_pressed(self, symbol, modifiers):
        self.p.key_pressed(symbol, modifiers)
    def key_released(self, symbol, modifiers):
        self.p.key_released(symbol, modifiers)
    def start(self, level):
        self.Start = True
        self.level = level

    def draw(self):
        if self.level == -1:
            # won level, go to next level
            pass
        elif self.level == -2:
            # lost level go to next
            pass
        elif self.level == -3:
            # beat game, go to credits or rickroll or smt idk
            pass
        else:
            self.p.draw()

    def set_level(self, level: int):
        self.level = level
