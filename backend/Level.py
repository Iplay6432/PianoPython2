from pyglet import shapes, text
import pyglet
import json
import sys
import os
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
class Level:    
    def __init__(self, level: int, x: float, y:float , radius: float, size: float):
        self.color = (255,255,255)
        self.radius = radius
        self.LEVEL_SIZE = size
        self.level = str(level) 
        self.x = x
        self.y = y
        self.border_width = 4
        self.text_color =(0,0,0)
        self.stars = [None,None,None,None,None]
        self.hint = "Oh well, No hint for you!"
        with open(resource_path(f"backend/jsons/{self.level}.json"), "r") as f:
           data = json.load(f)
           self.hint = data["hint"]
           self.level_name =  data["name"]
           f.close()
        best_score = "Not Played Yet"
        score =0
        with open(resource_path("backend/data/data.json"), "r") as f:
            data = json.load(f)
            if self.level in data["levels"]:
                score=data["levels"][self.level]["accuracy"]
                best_score = str(round(data["levels"][self.level]["accuracy"]*100, 1)) + "%"
            f.close()
        if best_score != "Not Played Yet":
            num_of_stars = int(float(score)*100/20)
            if float(score)*100 > 95:
                num_of_stars = 5
            for i in range(num_of_stars):
                self.stars[i] = shapes.Star(x+(1/8)*size + (3/4)/5*size*i + 1/16*size, y +3/8*size,1/16*size, 1/32*size, 5,55 ,color=(0,0,0))
        self.title = text.Label(self.level_name, font_name="Times New Roman", font_size=self.px_to_pt((7/8 * 1/16*size)), x = x + size/2, y = y + size*15/16, anchor_x="center", anchor_y="center", color = self.text_color)
        self.score1 = text.Label("Best Score:", font_name="Times New Roman", font_size=self.px_to_pt(size*7/8*1/8*1/2), x=x+size/2, y=y+size*3/16, anchor_x="center", color = self.text_color)
        self.score2 = text.Label(str(best_score), font_name="Times New Roman", font_size=self.px_to_pt(size*7/8*1/8*1/2), x=x+size/2, y=y+size*3/32, anchor_x="center", anchor_y="center",color = self.text_color)
        self.rect1 = shapes.RoundedRectangle(x,y,self.LEVEL_SIZE,self.LEVEL_SIZE, radius=self.radius, color=(0,0,0))
        self.rect2 = shapes.RoundedRectangle(x+self.border_width,y+self.border_width, self.LEVEL_SIZE-2*self.border_width,self.LEVEL_SIZE-2*self.border_width, radius= self.radius-1, color=self.color)
        self.label = pyglet.text.Label(self.level, font_name="Times New Roman", font_size=self.px_to_pt(size*7/8*3/8), x = self.x + size/2, y = self.y + size*11/16,anchor_x="center", anchor_y="center", color = self.text_color)
    def getHint(self) -> str:
        return self.hint
    def update(self):
        with open(resource_path(f"backend/jsons/{self.level}.json"), "r") as f:
           data = json.load(f)
           self.level_name =  data["name"]
           f.close()
        best_score = "Not Played Yet"
        score = 0
        x = self.x
        y= self.y
        size = self.LEVEL_SIZE
        with open(resource_path("backend/data/data.json"), "r") as f:
            data = json.load(f)
            if self.level in data["levels"]:
                score =data["levels"][self.level]["accuracy"]
                best_score = str(round(data["levels"][self.level]["accuracy"]*100, 1)) + "%"
            f.close()
        if best_score != "Not Played Yet":
            num_of_stars = 0
            self.stars = [None,None,None,None,None]
            if float(score)*100 >= 99:
                num_of_stars = 5
            for i in range(num_of_stars):
                self.stars[i] = (shapes.Star(x+(1/8)*size + (3/4)/5*size*i + 1/16*size, y +3/8*size,1/16*size, 1/32*size, 5,55 ,color=(0,0,0),))
        size = self.LEVEL_SIZE
        self.title = text.Label(self.level_name, font_name="Times New Roman", font_size=self.px_to_pt((7/8 * 1/16*size)), x = x + size/2, y = y + size*15/16, anchor_x="center", anchor_y="center", color = self.text_color)
        self.score1 = text.Label("Best Score:", font_name="Times New Roman", font_size=self.px_to_pt(size*7/8*1/8*1/2), x=x+size/2, y=y+size*3/16, anchor_x="center", color = self.text_color)
        self.score2 = text.Label(str(best_score), font_name="Times New Roman", font_size=self.px_to_pt(size*7/8*1/8*1/2), x=x+size/2, y=y+size*3/32, anchor_x="center", anchor_y="center",color = self.text_color)
        self.rect1 = shapes.RoundedRectangle(x,y,self.LEVEL_SIZE,self.LEVEL_SIZE, radius=self.radius, color=(0,0,0))
        self.rect2 = shapes.RoundedRectangle(x+self.border_width,y+self.border_width, self.LEVEL_SIZE-2*self.border_width,self.LEVEL_SIZE-2*self.border_width, radius= self.radius-1, color=self.color)
        self.label = pyglet.text.Label(self.level, font_name="Times New Roman", font_size=self.px_to_pt(size*7/8*3/8), x = self.x + size/2, y = self.y + size*11/16,anchor_x="center", anchor_y="center", color = self.text_color)
    def px_to_pt(self, px, dpi=96) -> int:
        return int(px * 72 / dpi)    
    def getObjects(self):
        return [self.rect1, self.rect2, self.title, self.score1, self.score2, self.label]
    def getStars(self):
        return self.stars
    def getText(self) -> text.Label:
        return self.label
    def getX(self):
        return self.x
    def getY(self):
        return self.y
    def getRect(self) -> tuple[shapes.RoundedRectangle, shapes.RoundedRectangle]:
        return self.rect1, self.rect2
    def isClicked(self, mx, my) -> bool:
        if mx >= self.x and mx <=self.x + self.LEVEL_SIZE:
            if my >= self.y and my <=self.y + self.LEVEL_SIZE:
                return True
        return False
    def getLevel(self) -> int:
        return int(self.level)
    def setColor(self, color: tuple[int, int, int]):
        self.color = color
        self.rect2 = shapes.RoundedRectangle(self.x+self.border_width,self.y+self.border_width, self.LEVEL_SIZE-2*self.border_width,self.LEVEL_SIZE-2*self.border_width, radius= self.radius-1, color=self.color)