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
        self.keys: KeyboardNote = []
        White = ["C", "D", "E", "F", "G", "A", "B"]
        Black = ["Db", "Eb", "Gb", "Ab", "Bb"]
        Octive = ["3", "4", "5"]
        self.octive  = 4
        o=0
        temp = []
        with open("settings.txt", "r") as f:
            for line in f.readlines():
                temp.append(float(line.strip()))
        self.volume = temp[1]
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
                vol=self.volume,
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
                        color= (0,0,0),
                        vol=self.volume
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
                        color= (0,0,0),
                        vol=self.volume
                    )
                )
                m += 1

    def draw(self):
        for m in self.keys:
            m.draw()
        pyglet.text.Label("Current Octave: " + str(self.octive) ,font_name="Times New Roman", font_size=self.BLACK_KEY_WIDTH/2, x=self.window.width/100, y = self.window.height/2,anchor_x="left",anchor_y="baseline", color=(0,0,0)).draw()

    def key_pressed(self, symbol, modifer):
        key_str = key.symbol_string(symbol).replace("_", "")
        if key_str in self.keybinds:
            p = self.keybinds[key_str]
            if p == "up" and self.octive < 5:
                self.octive += 1
            elif p == "down" and self.octive > 3:
                self.octive -= 1
            elif "*" in p and modifer == 1:
                self.playing = True
                change = 0
                if self.octive == 3:
                    change = 2
                elif self.octive == 5:
                    change = -2
                elif self.octive == 4:
                    change = 1
                target_octave = str(self.octive + change)
                note_name = p.replace("*", target_octave)
                for note in self.keys:
                    if note.getNote() == note_name:
                        note.is_pressed(note_name)
                        note.alt_key = True
                        return note_name
            elif "*" in p and modifer == 0:
                self.playing = True
                change = 0
                if self.octive == 3:
                    change = 1
                elif self.octive == 5:
                    change = -1
                elif self.octive == 4:
                    change = -1
                target_octave = str(self.octive + change)
                note_name = p.replace("*", target_octave)
                for note in self.keys:
                    if note.getNote()== note_name:
                        note.is_pressed(note_name)
                        note.alt_key = True
                        return note_name
            else:
                note_name = p + str(self.octive)
                for note in self.keys:
                    if note.getNote() == note_name:
                        note.reg_key = True
                        note.is_pressed(note_name)
                        return note_name
    def key_released(self, symbol, modifer):
        if key.symbol_string(symbol).replace("_", "") in self.keybinds:
            p = str(self.keybinds[key.symbol_string(symbol).replace("_", "")])
            if "*" in p and p != "*up" and p != "*down":
                note_name = ""
                note_name = p.replace("*", "")
                played_note = ""
                for note in self.keys:
                    if note.alt_key:
                        if note.note_name == note_name:
                            if note.is_playing():
                                played_note = note.getNote()
                                note.alt_key = False
                            note.do_stop()
                return played_note
            elif p != "up" and p != "down":
                for note in self.keys:
                    if note.reg_key and note.note_name == p:
                        note.do_stop()
                        note.reg_key = False
                return p +str(self.octive)