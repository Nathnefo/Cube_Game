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
    def __init__(self, _x, _y, window):

        super().__init__(_x, _y, 50, 50, 5, Color.blue) 
    
    def move(self, direction):
        if direction =="l":
            self.x -= self.speed
        elif direction == "r":
            self.x += self.speed
        elif direction == "u":
            self.y -= self.speed
        elif direction == "d":
            self.y += self.speed

class Ennemy(Entity):
    def __init__(self, _x, _y, _width = 50, _height = 50, _speed = 1, _color = Color.black):
        super().__init__(_x, _y, _width, _height, _speed, _color) 

    def move(self, target_x, target_y):
        """move towards target position and check that it does not exceed it"""
        center_x = self.x + self.width // 2
        center_y = self.y + self.width // 2
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
                 self.x += target_y - center_y
            else:
                self.y += self.speed
        if target_y < center_y:
            if center_y - target_y < self.speed:
                self.y += center_y - target_y
            else:
                self.y -= self.speed
        

class Food(Entity):
    def __init__(self, _window, _width = 20, _height = 20, _speed = 1, _color = Color.black):
        """Spawn on a random location"""
        self.window = _window
        x = randint(0, self.window.width)
        y = randint(0, self.window.height)
        super().__init__(x, y, _width, _height, _speed, _color) 
    
    def eated(self):
        """If eaten, it teleport to a new random location"""
        self.x = randint(0, self.window.width)
        self.y = randint(0, self.window.height)