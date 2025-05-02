from threading import Thread
from time import sleep, time
import pyglet
import json
import pyglet.window.key as key
import time
from backend.KeyboardNote import KeyboardNote
class PianoKeyboard:
    def __init__(self, window):
        self.window = window
        self.OCTIVES = 3
        self.WHITE_KEY_WIDTH = window.width / (7 * self.OCTIVES)
        self.BLACK_KEY_WIDTH = self.WHITE_KEY_WIDTH * 0.5
        self.WHITE_KEY_HEIGHT = window.height / 2
        self.BLACK_KEY_HEIGHT = self.WHITE_KEY_HEIGHT * 0.64
        self.BORDER_WIDTH = int(window.width / 500)
        self.keys = []
        White = ["C", "D", "E", "F", "G", "A", "B"]
        Black = ["Db", "Eb", "Gb", "Ab", "Bb"]
        Octive = ["3", "4", "5"]
        self.octive  = 4
        self.last_octive = 3 
        o=0
        with open("backend/data/keybinds.json", "r") as file:
            self.keybinds = json.load(file)
            file.close()
        for i in range(self.OCTIVES * 7):  # white keys
            if(i%7 ==0 and i != 0):
                o +=1
            self.keys.append(KeyboardNote(
                list(White)[i % 7] + Octive[o],
                self.WHITE_KEY_WIDTH * i,
                0,
                self.WHITE_KEY_WIDTH,
                self.WHITE_KEY_HEIGHT,
                self.BORDER_WIDTH,
            ))
        m = 0
        for i in range(3):
            for t in range(2):
                self.keys.append(
                    KeyboardNote(
                        Black[m % 5]+ Octive[i],
                        self.WHITE_KEY_WIDTH
                        + t * self.WHITE_KEY_WIDTH
                        + i * (7 * self.WHITE_KEY_WIDTH),
                        self.WHITE_KEY_HEIGHT - self.BLACK_KEY_HEIGHT,
                        self.BLACK_KEY_WIDTH,
                        self.BLACK_KEY_HEIGHT,
                        self.BORDER_WIDTH,
                        anchor_x="center",
                        color= (0,0,0)
                    )
                )
                m += 1
            for n in range(3):
                temp = (
                self.WHITE_KEY_WIDTH * 4
                + i * self.WHITE_KEY_WIDTH*7
                + n * self.WHITE_KEY_WIDTH
                )
                self.keys.append(
                    KeyboardNote(
                        Black[m % 5]+ Octive[i],
                        temp,
                        self.WHITE_KEY_HEIGHT - self.BLACK_KEY_HEIGHT,
                        self.BLACK_KEY_WIDTH,
                        self.BLACK_KEY_HEIGHT,
                        self.BORDER_WIDTH,
                        anchor_x="center",
                        color= (0,0,0)
                    )
                )
                m += 1

    def draw(self):
        for m in self.keys:
            m.draw()

    def key_pressed(self, symbol, modifer):
        if key.symbol_string(symbol).replace("_", "") in self.keybinds:
            p = self.keybinds[key.symbol_string(symbol).replace("_", "")]
            if p == "up":
                if self.octive < 5:
                    self.last_octive =self.octive
                    self.octive+=1
            if p == "down" and self.octive > 3:
                self.last_octive = self.octive
                self.octive-=1
            if "*" in p:
                if self.octive ==3:
                    for note in self.keys:
                        note.is_pressed(p.replace("*", str(self.octive +1)))
                    return p.replace("*", str(self.octive +1))
                else:
                    for note in self.keys:
                        note.is_pressed(p.replace("*", str(self.octive -1)))
                    return p.replace("*", str(self.octive -1))
            elif p != "up" and p != "down":
                for note in self.keys:
                    note.is_pressed(p+str(self.octive))
                return p +str(self.octive)
    
    def key_released(self, symbol, modifer):
        if key.symbol_string(symbol).replace("_", "") in self.keybinds:
            p = self.keybinds[key.symbol_string(symbol).replace("_", "")]
            if "*" in p:
                if self.octive ==3:
                    for note in self.keys:
                        note.key_released(p.replace("*", str(self.octive +1)))
                        note.key_released(p+str(self.last_octive))
                    return p.replace("*", str(self.octive +1))
                else:
                    for note in self.keys:
                        note.key_released(p.replace("*", str(self.octive -1)))
                        note.key_released(p+str(self.last_octive))
                    return p.replace("*", str(self.octive -1))
            elif p != "up" and p != "down":
                for note in self.keys:
                    note.key_released(p+str(self.octive))
                    note.key_released(p+str(self.last_octive))
                return p +str(self.octive)