import pyglet
from pyglet import shapes
from backend.Level import Level

class Levels:
    def __init__(self, window):
        self.window = window
        
        self.TOTAL_NUMBER_OF_LEVELS = 20
        self.LEVEL_SIZE  = self.window.width/5
        self.LEVEL_COLOR = (255,255,255)
        self.LEVEL_RADIUS = self.window.width/60
        self.NUMBER_OF_HORIZONTAL_LEVELS = 4
        self.NUMBER_OF_VERTICAL_LEVELS = 2
        self.LEVEL_WIDTH_BETWEEN_LEVELS = (self.window.width -self.LEVEL_SIZE*self.NUMBER_OF_HORIZONTAL_LEVELS)/(self.NUMBER_OF_HORIZONTAL_LEVELS + 1)
        self.LEVEL_HEIGHT_BETWEEN_LEVELS = (self.window.height -self.LEVEL_SIZE*self.NUMBER_OF_VERTICAL_LEVELS)/(self.NUMBER_OF_VERTICAL_LEVELS + 1)
        self.LEVELS_PER_PAGE = 8
        self.levels = []
        self.order = [5,6,7,8,1,2,3,4]
        self.zero_order =[4,5,6,7,0,1,2,3]
        self.pos = 0
        m = 0
        self.end = False
        for k in range(self.NUMBER_OF_VERTICAL_LEVELS):
            for i in range(self.NUMBER_OF_HORIZONTAL_LEVELS):
                temp = Level(self.order[m],self.LEVEL_WIDTH_BETWEEN_LEVELS + (self.LEVEL_WIDTH_BETWEEN_LEVELS+self.LEVEL_SIZE)*i,
                             self.LEVEL_HEIGHT_BETWEEN_LEVELS + (self.LEVEL_HEIGHT_BETWEEN_LEVELS+self.LEVEL_SIZE)*k, 
                             radius =self.LEVEL_RADIUS, 
                             size=self.LEVEL_SIZE)
                self.levels.append(temp)
                m+=1   
        self.select(self.pos) 
    def key_pressed(self, symbol, modifiers):
        if(symbol == 65363):
            self.pos = self.pos + 1 if self.pos < self.LEVELS_PER_PAGE -1 else self.pos
            self.select(self.pos)
        if(symbol == 65361):
            self.pos = self.pos -1 if self.pos > 0 else  self.pos
            self.select(self.pos)
        if(symbol  == 65293):
            self.end = True
    def draw(self):
        shapes.Rectangle(0,0, self.window.width, self.window.height, color=(255,255,255)).draw()
        
        for l in self.levels:
            r = l.getRect()
            r[0].draw()
            r[1].draw()
            l.getText().draw()
    def select(self, n: int):
        for l in self.levels:
            l.setColor(self.LEVEL_COLOR)
        self.levels[self.zero_order[n]].setColor((142,172,180))
    def isEnded(self):
        return [bool(self.end), int(self.pos)+1]
        
        