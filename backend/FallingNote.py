from threading import Thread
from time import sleep, time
import pyglet
import json
# top space is 1 mesures! all in 4/4 may implement others later
class FaillingNote(pyglet.shapes.BorderedRectangle):
    def __init__(self, note: str, height: int, width: int,
                 border_width: int,vol=75,color=(255, 255, 255),
                 border_color=(0, 0, 0),
                 anchor_x="bottom left",
        time: int = 2, bpm: int = 100):  # time is in beats

        x = 0
        y = height
        height = time * ((height/2)/bpm)
        with open("backend/data/note_pos.json", "r") as file:
            data = json.load(file)
            x = data[note]*width - width
            file.close()
        if int(width) != width:
            width = width/2
        if anchor_x == "center":
            x = x-width/2
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
        note = note
        self.time = time
        self.bpm = bpm
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
    def dx(self, fps): #
        self.y += 1
    def play(self):
        sound = pyglet.media.load(f"backend/notes/{self.note}{self.octive}.wav")
        time = 60 / self.bpm * self.time
        thread = Thread(
            target=self._play,
            args=(
                sound,
                time,
            ),
        )
        thread.start()

    def _play(self, sound: pyglet.media.load, time: int):
        self.player.queue(sound)
        self.player.play()
        sleep(time)
        curr = time()
        while self.player.volume > .5:
            self.player.volume = self.logistic_curve(time, curr)
        self.player.pause()
        del self.player
    def logistic_curve(self,timee, curr):
        return 75 / (1 + 2.718 ** (8*(timee-(curr- self.start_time))))