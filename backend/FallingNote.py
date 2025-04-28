from threading import Thread
from time import sleep
import time as t
import pyglet
import json
import random
# top space is 1 mesures! all in 4/4 may implement others later
class FaillingNote(pyglet.shapes.BorderedRectangle):
    def __init__(self, note: str, height: int, width: int,
                 border_width: int,vol=50,color=(255, 255, 255),
                 border_color=(0, 0, 0),
                 anchor_x="bottom left",
        durr: float = 2, bpm: int = 100, time: float = 2):  # time is in beats
        
        x = 0
        y = height
        self.screen_height = height
        height = durr * ((height/2)/bpm)*4
        with open("backend/data/note_pos.json", "r") as file:
            data = json.load(file)
            x = (data[note]-1)*width
            file.close()
        if "b" in note:
            width = width * 0.5
        if anchor_x == "center":
            x = x + width/2
        self.colorr = tuple(color)
        super().__init__(
            x,
            y,
            width,
            height,
            border=border_width,
            color=color,
            border_color=border_color
        )
        self.volume = vol
        self.time = time
        note = note
        self.durr = durr
        self.bpm = bpm
        self.played = False
        if len(note) == 3:
            self.octive = note[2]
            self.note = note[0] + note[1]
        else:
            self.octive = note[1]
            self.note = note[0]
        self.player = pyglet.media.Player()
    def get_note(self) -> str:
        return self.note

    def get_octive(self) -> int:
        return self.octive
    def get_x(self) -> int:
        return self.x
    def get_y(self) -> int:
        return self.y
    def get_width(self) -> int:
        return self.width
    def get_height(self) -> int:
        return self.height
    def get_pos(self) -> int:
        return self.pos
    def get_time(self) -> int:
        return self.time
    def get_durr(self) -> int:
        return self.durr
    def dy(self, fps, beat): #runs every frame at 60fps
        if self.y > self.screen_height/2 - self.height and beat >= self.time:
            self.y -= ((self.screen_height/2)/float(fps))/4
            if not self.played and self.y <= self.screen_height/2:
                self.play()
                self.played = True
                self.done = True
                return self.played
        elif self.y <= self.screen_height/2 - self.screen_height and self.done:
                self.done = False
                return False
    def play(self):
        sound = pyglet.media.load(f"backend/notes/{self.note}{self.octive}.wav")
        durr = 60 / self.bpm * self.durr
        self.thread = Thread(
            target=self._play,
            args=(
                sound,
                durr,
            ),
        )
        self.thread.start()
    def draw(self):
        if self.y > self.screen_height/2 - self.height:
            super().draw()
        else:
            pass
    def _play(self, sound: pyglet.media.load, time: int):
        self.player.queue(sound)
        self.player.play()
        sleep(time)
        # while self.player.volume > .5:
        #     self.player.volume = self.logistic_curve(time)
        self.player.pause()
        
    def logistic_curve(self,timee):
        return 75 / (1 + 2.718 ** (8*(timee-(timee/2))))