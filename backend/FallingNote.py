from threading import Thread
from time import sleep, time
import pyglet

class FaillingNote:
    def __init__(
        self, note: str = "A4", time: int = 2, bpm: int = 100
    ):  # time is in beats
        note = list(note)
        self.time = time
        self.bpm = bpm
        if len(note) == 3:
            self.octive = note[2]
            self.note = note[0] + note[1]
        else:
            self.octive = note[1]
            self.note = note[0]

    def get_note(self) -> str:
        return self.note

    def get_octive(self) -> int:
        return self.octive

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
        play = sound.play()
        sleep(time)
        play.delete()