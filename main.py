import pygame
import random
from datetime import datetime


class Color:
    red = (255, 0, 0)
    green = (0, 255, 0)
    l_green = (0, 100, 0)
    blue = (0, 0, 255)
    white = (255, 255, 255)
    black = (0, 0, 0)
    grey = (100, 100, 100)
    l_grey = (200, 200, 200)

class Window:
    def __init__(self, title, _width, _height):
        self.width = _width
        self.height = _height
        self.screen = pygame.display.set_mode((_width, _height))
        pygame.display.set_caption(title)

class Render:
    def __init__(self, _window):
        self.window = _window
        self.font = pygame.font.SysFont(None, 24)
        self.title_font = pygame.font.SysFont(None, 70)

    def update(self, scene, clock):
        if scene.num == 0 or scene.num == 1:
            self.window.screen.fill(scene.background_colour)

        for obj in scene.obj_render_list:
            self.window.screen.blit(obj.surface, (obj.x, obj.y))

        if scene.num == 0 or scene.num == 2:
            for button in scene.buttons:
                pygame.draw.rect(window.screen, button.current_color, [button.x,button.y, button.width, button.height])
                button_text = self.font.render(button.text, True, Color.white)
                text_rect = button_text.get_rect(center=button.get_center())
                self.window.screen.blit(button_text, text_rect)
                """ title_text = self.title_font.render("The Cube Game", True, Color.blue)
                        title_text_rect = title_text.get_rect(center=(window.width//2, window.height//4))
                        self.window.screen.blit(title_text, title_text_rect)"""
        elif scene.num == 1:
            img = self.font.render(f'Points : {scene.point}', True, (0,0,0))
            self.window.screen.blit(img, (20, 20))
    
        fps = self.font.render(f'Fps : {round(clock.get_fps())}', True, (0,0,0))
        self.window.screen.blit(fps, (window.width - 100, 20))

        pygame.display.flip()

class Player:
    def __init__(self, _x, _y, _width = 50, _height = 50, _speed = 1, _color = Color.black): 
        self.x = _x
        self.y = _y
        self.width = _width
        self.height = _height
        self.speed = _speed
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(_color)
    
    def get_center(self):
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    def move(self, direction):
        if direction =="l":
            self.x -= self.speed
        elif direction == "r":
            self.x += self.speed
        elif direction == "u":
            self.y -= self.speed
        elif direction == "d":
            self.y += self.speed

class Ennemy(Player):
    def move(self, target_x, target_y):
        center_x = self.x + self.width // 2
        center_y = self.y + self.width // 2
        if target_x < center_x:
            if center_x- target_x < self.speed:
                self.x -= center_x - target_x
            self.x -= self.speed
        if target_x > center_x:
            if target_x - center_x < self.speed:
                 self.x += target_x - center_x
            self.x += self.speed
        if target_y > center_y:
            if target_y - center_y < self.speed:
                 self.x += target_y - center_y
            self.y += self.speed
        if target_y < center_y:
            if center_y - target_y < self.speed:
                self.y += center_y - target_y
            self.y -= self.speed
        

class Food:
    def __init__(self, _window):
        self.window = _window
        self.x = random.randint(0, self.window.width)
        self.y = random.randint(0, self.window.height)
        self.width = 20
        self.height = 20
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill((0,0,0))
    
    def eated(self):
        self.x = random.randint(0, self.window.width)
        self.y = random.randint(0, self.window.height)


class Game_State():
    def __init__(self, window):
        self.background_colour = Color.white
        self.num = 1

        self.player = Player(0, 0, 50, 50, 5, Color.blue)
        self.ennemy = Ennemy(500, 500, 25, 25, 2, Color.red)
        self.foods = [Food(window), Food(window), Food(window), Food(window), Food(window)]
        self.point = 0

        self.obj_render_list = [self.ennemy, self.player] + self.foods

    def add_point(self):
        self.point += 1

class Main_Menu():
    def __init__(self, window, engine):
        self.background_colour = Color.l_grey
        self.num = 0

        self.play_button = Button(window.width//2- 100, window.height//2- 25, _text="Play", _on_click=engine.change_scene, _arg = 1)
        self.settings_button = Button(window.width//2- 100, window.height//2 + 30, _text="Settings (Soon)", _hover_color=Color.grey)
        self.leave_button = Button(window.width//2- 100, window.height//2 + 85, _text="Quit", _hover_color=Color.red, _on_click=engine.stop_all)

        self.buttons = [self.play_button, self.settings_button, self.leave_button]

        self.obj_render_list = []
        self.gui_render_list = [self.play_button, self.settings_button, self.leave_button]


class Retry_Menu():
    def __init__(self, window, engine):
        self.background_colour = Color.l_grey
        self.num = 2

        self.retry_button = Button(window.width//2- 100, window.height//2 - 55, _text="Retry", _on_click=engine.change_scene,_arg = 1 )
        self.main_menu_button = Button(window.width//2- 100, window.height//2, _text="Main Menu", _hover_color=Color.grey, _on_click=engine.change_scene, _arg = 0)
        self.leave_button = Button(window.width//2- 100, window.height//2 + 55, _text="Quit", _hover_color=Color.red, _on_click=engine.stop_all)

        self.buttons = [self.retry_button, self.main_menu_button, self.leave_button]

        self.obj_render_list = []
        self.gui_render_list = [self.retry_button, self.main_menu_button, self.leave_button]


class Button():
    def __init__(self, _x, _y, _width = 200, _height = 50, _text= "", _color = Color.black, _hover_color = Color.l_green, _on_click = None, _arg = None):
        self.x = _x
        self.y = _y
        self.width = _width
        self.height = _height
        self.text = _text
        self.current_color = _color
        self.regular_color = _color
        self.hover_color = _hover_color
        self.mouse_was_hover = False
        self.on_click = _on_click
        self.arg = _arg
    
    def get_center(self):
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    def on_mouse_hover(self):
        self.current_color = self.hover_color
    
    def on_mouse_quit(self):
        self.current_color = self.regular_color


class Engine:
    def __init__(self, window):
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.game_state = None
        self.render = Render(window)
        self.main_menu = Main_Menu(window, self)
        self.retry_menu = Retry_Menu(window, self)
        self.current_scene = 0
        self.before_click = False
    
    def detect_collide(self, obj1, obj2):
        if obj1.x <= obj2.x + obj2.width and obj1.x + obj1.width >= obj2.x: #if = (more strict)
            if obj1.y <= obj2.y + obj2.height and obj1.y + obj1.height >= obj2.y:
                return True
        return False
    
    def mouse_hover(self, x, y, button):
        if (x > button.x and x < button.x + button.width) and (y > button.y and y < button.y + button.height):
            return True
        return False

    
    def update_buttons(self, scene):
        mouse = pygame.mouse.get_pos()
        for button in scene.buttons:
            if self.mouse_hover(mouse[0], mouse[1], button):
                if not(button.mouse_was_hover):
                    button.on_mouse_hover()
                    button.mouse_was_hover = True
            elif button.mouse_was_hover:
                button.on_mouse_quit()
                button.mouse_was_hover = False

    def is_click(self):
        left, middle, right = pygame.mouse.get_pressed()
        if self.before_click and not(left):
            self.before_click = False
        elif not(self.before_click) and left:
            self.before_click = True
            return True
        return False
    
    def eng_menu(self, scene):
        self.update_buttons(scene)

        click = self.is_click()

        if click:
            for button in scene.buttons:
                if button.mouse_was_hover and button.on_click != None:
                    if button.arg == None:
                        button.on_click()
                    else:
                        button.on_click(button.arg)
        
        self.render.update(scene, self.clock)
       
    
    def eng_game(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.game_state.player.move("l")
        if keys[pygame.K_RIGHT]:
            self.game_state.player.move("r")
        if keys[pygame.K_UP]:
            self.game_state.player.move("u")
        if keys[pygame.K_DOWN]:
            self.game_state.player.move("d")
            
        pos_player = self.game_state.player.get_center()
        self.game_state.ennemy.move(pos_player[0], pos_player[1])

        if self.detect_collide(self.game_state.player, self.game_state.ennemy):
            self.change_scene(2)
        
        for food in self.game_state.foods:
            if self.detect_collide(self.game_state.player, food):
                food.eated()
                self.game_state.add_point()
        
        self.render.update(self.game_state, self.clock)

    def update(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            if self.current_scene == 0:
                self.eng_menu(self.main_menu)
            elif self.current_scene == 1:
                self.eng_game()
            elif self.current_scene == 2:
                self.eng_menu(self.retry_menu)
            self.clock.tick(180)
    
    def change_scene(self, num):
        if self.current_scene == 0:
            for button in self.main_menu.buttons:
                if button.mouse_was_hover:
                    button.on_mouse_quit()
                    button.mouse_was_hover = False
        if self.current_scene == 2:
            for button in self.retry_menu.buttons:
                if button.mouse_was_hover:
                    button.on_mouse_quit()
                    button.mouse_was_hover = False
        if num == 1:
            self.game_state = Game_State(window) #make a new game
        self.current_scene = num
    
    def stop_all(self):
        self.is_running = False

#(width, height) = (1200, 700)
(width, height) = (1920, 1080)

pygame.init()
window = Window("Cube_game", width, height)
engine = Engine(window)

engine.update()