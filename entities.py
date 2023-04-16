import pygame
from random import randint
from color import *

class Entity:
    def __init__(self, _x, _y, _width, _height, _speed, _color): 
        self.x = _x
        self.y = _y
        self.width = _width
        self.height = _height
        self.speed = _speed
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(_color)

    def get_center(self):
        return (self.x + self.width // 2, self.y + self.height // 2)

class Player(Entity):
    def __init__(self, _x, _y, _display):
        self.display = _display
        self.bullet_speed_mult = 1
        super().__init__(_x, _y, 50, 50, 4, Color.blue) 
    
    def move(self, direction):
        if direction =="l" and self.x > 0:
            if self.x - self.speed < 0:
                self.x = 0
            else:
                self.x -= self.speed
        elif direction == "u" and self.y > 0:
            if self.y - self.speed < 0:
                self.y = 0
            else:
                self.y -= self.speed
        elif direction == "d" and self.y < self.display.height - self.height:
            if self.y + self.speed > self.display.height - self.height:
                self.y = self.display.height - self.height
            else:
                self.y += self.speed
        elif direction == "r" and self.x < self.display.width - self.width:
            if self.x + self.speed > self.display.width - self.width:
                self.x = self.display.width - self.width
            else:
                self.x += self.speed

class Ennemy(Entity):
    def __init__(self, _x, _y, _width = 50, _height = 50, _speed = 2, _color = Color.black):
        super().__init__(_x, _y, _width, _height, _speed, _color) 

    def move(self, target_x, target_y):
        """move towards target position and check that it does not exceed it"""
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        if target_x < center_x:
            if center_x - target_x < self.speed:
                self.x -= center_x - target_x
            else:
                self.x -= self.speed
        if target_x > center_x:
            if target_x - center_x < self.speed:
                self.x += target_x - center_x
            else:
                self.x += self.speed
        if target_y > center_y:
            if target_y - center_y < self.speed:
                self.y += target_y - center_y
            else:
                self.y += self.speed
        if target_y < center_y:
            if center_y - target_y < self.speed:
                self.y += center_y - target_y
            else:
                self.y -= self.speed
        

class Food(Entity):
    def __init__(self, _display, _width = 20, _height = 20, _speed = 1, _color = Color.black):
        """Spawn on a random location"""
        self.display = _display
        x = randint(0, self.display.width)
        y = randint(0, self.display.height)
        super().__init__(x, y, _width, _height, _speed, _color) 
    
    def eated(self):
        """If eaten, it teleport to a new random location"""
        self.x = randint(0, self.display.width)
        self.y = randint(0, self.display.height)

class Bullet(Entity):
    def __init__(self,  _display, _x, _y, v_director, _width = 20, _height = 20, _speed = 1, _color = Color.l_green):
        self.display = _display
        self.v_director = v_director
        super().__init__(_x - _width//2, _y - _height//2, _width, _height, _speed, _color)
    
    def update(self):
        self.x += self.v_director[0]
        self.y += self.v_director[1]