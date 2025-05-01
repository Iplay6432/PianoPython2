import pyglet
import mido
import json
from backend.Piano import PianoKeyboard
import backend.FallingNote as fn 
import pyglet.window.key as key
import time as t
from number_line import NumberLine
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
        self.notes_done = 0
    def stop(self):
        self.beat = 0
        self.level = 1
        self.level_data = None
        self.bpm = 0
        self.Start = False
        self.notes = []
        self.notes_done = 0
    def key_pressed(self, symbol, modifiers):
        note = self.p.key_pressed(symbol, modifiers)
        if note != None:
            self.user_note_times[self.note_pos.index(note)].append(([t.time(), t.time() +1]))
    def key_released(self, symbol, modifiers):
        note = self.p.key_released(symbol, modifiers)
        if note != None:
            self.user_note_times[self.note_pos.index(note)][-1][1] = t.time()
    def start(self, level):
        self.Start = True
        self.level = level
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
        self.game_note_times = []
        self.user_note_times = []
        
        with open("backend/data/note_pos.json", "r") as file:
            self.note_pos = json.load(file)
            self.note_pos = list(self.note_pos.items())
            file.close()
        temp = []
        for item in self.note_pos:
            temp.append(item[0])
        self.note_pos = temp
        for i in range(36):
            self.game_note_times.append([])
            self.user_note_times.append([])
            
        self.last_beat = t.time()
    def get_score(self, user, game, index): 
        closest = 0
        if user[index] == []:
            return 0
        for i in range(len(user[index])):
            distance = abs(user[index][i][0]-game[0])
            last_distance =abs(user[index][closest][0] -game[0])
            if distance <= last_distance:
                closest = i
        score = ((abs(user[index][closest][0] - game[0]) +abs(user[index][closest][1] - game[1])))/ abs(game[1]-game[0])
        if score > 1:
            return 0
        return 1- score
    def draw(self):
        if self.level == -1:
            scores = []
            i = 0
            dist = 0
            for n in self.game_note_times:
                for note in n:
                    scores.append(self.get_score(self.user_note_times, note, i))
                i+=1
            total = 0
            for score in scores:
                total += score
            score = ((total/len(scores)))
            score = 1 if score > 1 else score
            data: json
            with open("backend/data/data.json", "r") as f:
                data = json.load(f)
                f.close()
            if self.og_level in data["levels"]:
                if data["levels"][str(self.og_level)]["accuracy"] < score:
                    data["levels"][str(self.og_level)]["done"] =1
                    data["levels"][str(self.og_level)]["accuracy"] = score
            else:
                # implement later
                new_data = {"done": 1, "accuracy": score}
                data["levels"][self.og_level] = new_data
            with open ("backend/data/data.json", "w") as f:
                json.dump(data,f)
                f.close()
            return True
        elif self.level == -2:
            # beat game, go to credits or rickroll or smt idk
            pass
        else:
            pyglet.shapes.Rectangle(0, 0, self.window.width, self.window.height, color=(225, 123, 136)).draw()
            for note in self.notes:
                value =note.dy(self.fps_display.label.text, self.beat)
                if value != None:
                    if value == True:
                        note.start_time = t.time()
                    elif value == False:
                        temp = [note.start_time, t.time()]
                        self.notes_done += 1
                        self.game_note_times[self.note_pos.index(note.get_note()+ note.get_octive())].append(temp)
                note.draw()
                
            self.beat= (t.time()- self.last_beat)*(self.bpm/60)
            self.p.draw()
            if self.notes_done == len(self.notes):
                t.sleep(1)
                self.og_level = self.level
                self.level = -1
    def set_level(self, level: int):
        self.level = level
