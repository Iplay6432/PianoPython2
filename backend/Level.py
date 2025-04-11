from pyglet import shapes, text
import pyglet

class Level:    
    def __init__(self, level: int, x: float, y:float , radius: float, size: float):
        self.color = (255,255,255)
        self.radius = radius
        self.LEVEL_SIZE = size
        self.level = str(level) 
        self.x = x
        self.y = y
        self.border_width = 4
        self.rect1 = shapes.RoundedRectangle(x,y,self.LEVEL_SIZE,self.LEVEL_SIZE, radius=self.radius, color=(0,0,0))
        self.rect2 = shapes.RoundedRectangle(x+self.border_width,y+self.border_width, self.LEVEL_SIZE-2*self.border_width,self.LEVEL_SIZE-2*self.border_width, radius= self.radius-1, color=self.color)
        self.text_color =(0,0,0)
    def px_to_pt(self, px, dpi=96) -> int:
        return int(px * 72 / dpi)    
    def getText(self) -> text.Label:
        label = pyglet.text.Label(self.level, font_name="Times New Roman", font_size=self.px_to_pt(self.LEVEL_SIZE/5), x = self.x +self.LEVEL_SIZE/2, y = self.y + self.LEVEL_SIZE/2,anchor_x="center", anchor_y="center", color = self.text_color)
        return label
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