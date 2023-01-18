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
        self.text = _text
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
        pygame.draw.rect(self.engine.window.screen, self.color, [self.x,self.y, self.width, self.height])
        button_text = self.font.render(self.text, True, Color.white)
        text_rect = button_text.get_rect(center=self.get_center())
        self.engine.window.screen.blit(button_text, text_rect)


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
        self.engine.window.screen.blit(render_text, text_rect)