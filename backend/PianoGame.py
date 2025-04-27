import pyglet
import mido
import json
from backend.Piano import PianoKeyboard
import backend.FallingNote as fn 
import pyglet.window.key as key
import time as t
# top space is 1 mesures!
# always in 4/4, may implement others later
class PianoGame:
    def __init__(self, window):
        self.window = window
        self.OCTIVES = 3
        self.WHITE_KEY_WIDTH = window.width / (7 * self.OCTIVES)
        self.BLACK_KEY_WIDTH = self.WHITE_KEY_WIDTH * 0.5
        self.WHITE_KEY_HEIGHT = window.height / 2
        self.BLACK_KEY_HEIGHT = self.WHITE_KEY_HEIGHT * 0.64
        self.BORDER_WIDTH = int(window.width / 500)
        
        self.Start = False
        self.level = 1
        self.level_data = None
        self.notes = []
        self.p = PianoKeyboard(self.window)
        self.bpm = 0
        self.fps_display = pyglet.window.FPSDisplay(window=self.window)
        self.beat = 0
        self.last_beat = 0
    def key_pressed(self, symbol, modifiers):
        self.p.key_pressed(symbol, modifiers)
    def key_released(self, symbol, modifiers):
        self.p.key_released(symbol, modifiers)
    def start(self, level):
        self.Start = True
        self.level = level
        # # self, note: str, width: int, height: int, 
        #          border_width: int,vol=75,color=(255, 255, 255),
        #          border_color=(0, 0, 0),
        #          anchor_x="bottom left",
        # time: int = 2, bpm: int = 100, 
        
        with open (f"backend/jsons/{self.level}.json", "r") as file:
            self.level_data = json.load(file)
            file.close()
        self.bpm = self.level_data["bpm"]
        for notes in self.level_data["notes"]:
            for time, note_list in notes.items():
                for note in note_list:
                    if "b" in note["note"]:
                        temp = fn.FaillingNote(note["note"], self.window.height, self.WHITE_KEY_WIDTH, self.BORDER_WIDTH, border_color=(65,29,124), color=(137,89,217), anchor_x="center", time=note["time"], durr=note["duration"], bpm=self.bpm)
                        self.notes.append(temp)
                    else:
                        temp = fn.FaillingNote(note["note"], self.window.height, self.WHITE_KEY_WIDTH, self.BORDER_WIDTH, color=(169, 217, 89), border_color=(73, 104, 24), anchor_x="bottom left", time=note["time"], durr=note["duration"], bpm=self.bpm)
                        self.notes.append(temp)
        self.last_beat = t.time()
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
            pyglet.shapes.Rectangle(0, 0, self.window.width, self.window.height, color=(225, 123, 136)).draw()
            for note in self.notes:
                note.dy(self.fps_display.label.text, self.beat)
                note.draw()
                
            self.beat= (t.time()- self.last_beat)*(self.bpm/60)
            # if t.time() - self.last_beat > 60/self.bpm:
            #     self.beat += 1
            #     self.last_beat = t.time()
            self.p.draw()
        # How to get fps, for future use 
        # self.fps_display = pyglet.window.FPSDisplay(window=self)
        # print("FPS: ", self.fps_display.label.text)
        # Make sure to time draw so that its once per frame, probably do it in the Main loop
            

    def set_level(self, level: int):
        self.level = level
