import pygame
from color import *

class Gui():
    def __init__(self, _engine, _x, _y, _width, _height, _color):
        self.engine = _engine
        self.x = _x
        self.y = _y
        self.width = _width
        self.height = _height
        self.color = _color

    def get_center(self):
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    def draw(self):
        pass

class Button(Gui):
    def __init__(self, _engine, _x, _y, _width = 200, _height = 50, _text= "", _color = Color.black, _hover_color = Color.l_green, _on_click = None, _arg = None):
        super().__init__(_engine, _x, _y, _width, _height, _color)
        self.font = pygame.font.SysFont(None, 25)

        center = self.get_center()
        self.text = Text(_engine, center[0], center[1], _text=_text, _color= Color.white, _centered=True)
        self.regular_color = _color
        self.hover_color = _hover_color
        self.mouse_was_hover = False
        self.on_click = _on_click
        self.arg = _arg
    
    def on_mouse_hover(self):
        self.color = self.hover_color
    
    def on_mouse_quit(self):
        self.color = self.regular_color
    
    def draw(self):
        """Draw current button with his text in the center"""
        pygame.draw.rect(self.engine.display.screen, self.color, [self.x,self.y, self.width, self.height])
        self.text.draw()


class Text(Gui):
    def __init__(self, _engine, _x, _y, _width = 200, _height = 50, _text= "", _color = Color.black, _size = 25, _centered = False, _fstring = False):
        super().__init__(_engine, _x, _y, _width, _height, _color)
        self.font = pygame.font.SysFont(None, _size)
        self.text = _text
        self.centered = _centered
        self.fstring = _fstring
    
    def draw(self):
        """Draw current text, if it's fstring execute it"""
        if self.fstring:
            render_text = self.font.render(eval(f'f"""{self.text}"""'), True, self.color)
        else:
            render_text = self.font.render(self.text, True, self.color)
        if self.centered:
            center = self.get_center()
            text_rect = render_text.get_rect(center=(self.x, self.y))
        else:
            text_rect = (self.x, self.y)
        self.engine.display.screen.blit(render_text, text_rect)

class Check_mark(Gui):
    def __init__(self, _engine, _x, _y, _width = 50, _height = 50, _color = Color.black, _state = False):
        super().__init__(_engine, _x, _y, _width, _height, _color)
        center = self.get_center()
        self.state = _state
        self.display = self.engine.display

        self.mouse_was_hover = False
        self.on_click = self.toggle_check_mark
        self.arg = None
    
    def on_mouse_hover(self):
        pass
    
    def on_mouse_quit(self):
        pass
    
    def toggle_check_mark(self):
        self.state = not(self.state)

    def draw(self):
        """Draw current button with his text in the center"""
        pygame.draw.rect(self.display.screen, self.color, [self.x,self.y, self.width, self.height], 3)
        if self.state:
            pygame.draw.line(self.display.screen, self.color, (self.x + self.width // 5, self.y + self.height // 5) , (self.x + self.width - self.width // 5, self.y + self.height - self.height // 5), 5)
            pygame.draw.line(self.display.screen, self.color, (self.x + self.width // 5 ,self.y + self.height - self.height // 5) , (self.x + self.width - self.width // 5, self.y + self.height // 5), 5)