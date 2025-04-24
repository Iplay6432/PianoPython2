from threading import Thread
from time import sleep, time
import pyglet

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
        o=0
        for i in range(self.OCTIVES * 7):  # white keys
            self.keys.append(KeyboardNote(
                list(White)[i % 7] + Octive[o],
                self.WHITE_KEY_WIDTH * i,
                0,
                self.WHITE_KEY_WIDTH,
                self.WHITE_KEY_HEIGHT,
                self.BORDER_WIDTH,
            ))
            if(i%7 ==0 and i != 0):
                o +=1
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
                        Black[m % 5]+ Octive[n],
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

    def key_pressed(key: str):
        pass


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


class KeyboardNote(pyglet.shapes.BorderedRectangle):
    def __init__(
        self,
        note: str,
        x: int,
        y: int,
        width: int,
        height: int,
        border_width: int,
        vol=75,
        color=(255, 255, 255),
        border_color=(0, 0, 0),
        anchor_x="bottom left",
    ):
        if anchor_x == "center":
            x = x-width/2
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

    def set_volume(self, vol: int):
        self.volume = vol

    def play(self):
        sound = pyglet.media.load(
            f"backend/notes/{self.note_name}{self.octive}.wav", streaming=False
        )
        self.thread = Thread(target=self._play, args=(sound,))
        self.thread.start()

    def _play(self, sound: pyglet.media.load):
        self.plays = sound.play().volume = self.volume

    def stop(self):
        self.thread.join(timeout=0.1)

    def note(self) -> str:
        return self.note_name + self.octive


# note = KeyboardNote("A4")
# note.play()
# sleep(1)
# note.stop()

note = FaillingNote()
note.play()
