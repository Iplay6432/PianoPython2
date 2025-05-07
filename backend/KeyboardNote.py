from threading import Thread
import pyglet
import time

class KeyboardNote(pyglet.shapes.BorderedRectangle):
    def __init__(
        self,
        note: str,
        x: int,
        y: int,
        width: int,
        height: int,
        border_width: int,
        vol=.5,
        color=(255, 255, 255),
        border_color=(0, 0, 0),
        anchor_x="bottom left",
    ):
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

        note = list(note)
        self.volume = vol
        if len(note) == 3:
            self.octive = note[2]
            self.note_name = note[0] + note[1]
        else:
            self.octive = note[1]
            self.note_name = note[0]
        self.sound = pyglet.media.load(
            f"backend/notes/{self.note_name}{self.octive}.wav", streaming=False
        )
        self.start_time = time.time()
        self.threads = []
        self.locked = False
        self.playing = False
    def set_volume(self, vol: int):
        self.volume = vol
        return self.volume
    def getNote(self):
        return self.note_name + self.octive
    def is_note_not_octave(self, note, octave):
        if note == self.note_name and octave != self.octive:
            return True
        else:
            return False
    def do_stop(self):
        self.locked = False
        self.color= self.colorr
        self.stop()
    def is_pressed(self, note : str):
        if len(note) == 3:
            octive = note[2]
            name = note[0] + note[1]
        else:
            octive = note[1]
            name = note[0]
        if self.note_name+self.octive == note and not self.locked:
            self.locked = True
            self.color = (199,0,57)
            self.play()
    def key_released(self, note: str): 
        if self.note_name+self.octive == note:
            self.locked = False
            self.color= self.colorr
            self.stop()
    def is_playing(self):
        return self.playing
    def play(self):
        self.threads.append(PlayNote(self.sound, self.volume))
        self.threads[-1].start()
    def _stop(self):
        if len(self.threads) == 0:
            return
        self.threads[0].stop()
        self.threads[0].join(timeout=0.1)
        self.threads.pop(0)
    def stop(self):
        Thread(target=self._stop).start()
    def note(self) -> str:
        return self.note_name + self.octive
class PlayNote(Thread):
    def __init__(self, sound, volume):
        super().__init__()
        self.running = True
        self.sound = sound
        self.volume = volume
        self.start_time = time.time()
         
        self.player = pyglet.media.Player()
    def run(self):
        self.playing = True
        self.player.queue(self.sound)
        self.player.volume = self.volume
        self.player.play()
        self.max_vol = self.volume
        self.start_time = time.time()
    def logistic_curve(self,timee, curr):
            return self.max_vol / (1 + 2.718 ** (4*(timee-(curr- self.start_time))))
    def short_curve(self, timee, curr):
        return self.max_vol / (1 + 2.718 ** (4*(timee-(curr- self.start_time))))

    def stop(self):
        self.playing = False
        curr = time.time()
        descent_time = time.time()
        if curr-self.start_time < .1:
            while self.player.volume > .05:
                self.player.volume = self.logistic_curve(time.time()-descent_time, curr)
                time.sleep(1/1000)
            self.player.pause()
        else:
            while self.player.volume > .05:
                self.player.volume = self.logistic_curve(time.time()-descent_time, curr)
                time.sleep(1/1000)
            self.player.pause()

        

        