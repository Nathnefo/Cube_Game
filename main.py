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
        

class Food(Entity):
    def __init__(self, _window, _width = 20, _height = 20, _speed = 1, _color = Color.black):
        self.window = _window
        x = random.randint(0, self.window.width)
        y = random.randint(0, self.window.height)
        super().__init__(x, y, _width, _height, _speed, _color) 
    
    def eated(self):
        self.x = random.randint(0, self.window.width)
        self.y = random.randint(0, self.window.height)

class Scene:
    def __init__(self, _num, _background_colour, _entity_render_list, _gui_render_list):
        self.num = _num
        self.background_colour = _background_colour
        self.entity_render_list = _entity_render_list
        self.gui_render_list = _gui_render_list
    
    def on_quit(self):
        pass

class Game_State(Scene):
    def __init__(self, engine):
        window = engine.window
        self.player = Player(0, 0, window)
        self.ennemy = Ennemy(500, 500, 25, 25, 2, Color.red)
        self.foods = [Food(window) for _ in range(8)]
        self.point = 0

        super().__init__(1, Color.white, [self.ennemy, self.player] + self.foods, [])

    def add_point(self):
        self.point += 1


class Main_Menu(Scene):
    def __init__(self, engine):
        window = engine.window
        self.play_button = Button(window.width//2- 100, window.height//2- 25, _text="Play", _on_click=engine.change_scene, _arg = 1)
        self.settings_button = Button(window.width//2- 100, window.height//2 + 30, _text="Settings (Soon)", _hover_color=Color.grey)
        self.leave_button = Button(window.width//2- 100, window.height//2 + 85, _text="Quit", _hover_color=Color.red, _on_click=engine.stop_all)

        self.buttons = [self.play_button, self.settings_button, self.leave_button]

        super().__init__(0, Color.l_grey, [], [self.play_button, self.settings_button, self.leave_button])

    def on_quit(self):
        for button in self.buttons:
            if button.mouse_was_hover:
                button.on_mouse_quit()
                button.mouse_was_hover = False

class Retry_Menu(Scene):
    def __init__(self, engine):
        window = engine.window
        self.retry_button = Button(window.width//2- 100, window.height//2 - 55, _text="Retry", _on_click=engine.change_scene,_arg = 1 )
        self.main_menu_button = Button(window.width//2- 100, window.height//2, _text="Main Menu", _hover_color=Color.grey, _on_click=engine.change_scene, _arg = 0)
        self.leave_button = Button(window.width//2- 100, window.height//2 + 55, _text="Quit", _hover_color=Color.red, _on_click=engine.stop_all)

        self.buttons = [self.retry_button, self.main_menu_button, self.leave_button]

        super().__init__(2, Color.l_grey, [], [self.retry_button, self.main_menu_button, self.leave_button])
    
    def on_quit(self):
        for button in self.buttons:
            if button.mouse_was_hover:
                button.on_mouse_quit()
                button.mouse_was_hover = False


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

class Window:
    def __init__(self, title, _width, _height):
        self.width = _width
        self.height = _height
        self.screen = pygame.display.set_mode((_width, _height))
        pygame.display.set_caption(title)

class Render:
    def __init__(self, engine):
        self.window = engine.window
        self.font = pygame.font.SysFont(None, 24)
        self.title_font = pygame.font.SysFont(None, 70)

    def update(self, scene):
        if scene.num == 0 or scene.num == 1:
            self.window.screen.fill(scene.background_colour)

        for obj in scene.entity_render_list:
            self.window.screen.blit(obj.surface, (obj.x, obj.y))

        for button in scene.gui_render_list:
            pygame.draw.rect(window.screen, button.current_color, [button.x,button.y, button.width, button.height])
            button_text = self.font.render(button.text, True, Color.white)
            text_rect = button_text.get_rect(center=button.get_center())
            self.window.screen.blit(button_text, text_rect)
  
        if scene.num == 0 :
            title_text = self.title_font.render("The Cube Game", True, Color.blue)
            title_text_rect = title_text.get_rect(center=(window.width//2, window.height//4))
            self.window.screen.blit(title_text, title_text_rect)
    
        if scene.num == 1:
            img = self.font.render(f'Points : {scene.point}', True, (0,0,0))
            self.window.screen.blit(img, (20, 20))
    
        fps = self.font.render(f'Fps : {round(engine.clock.get_fps())}', True, (0,0,0))
        self.window.screen.blit(fps, (window.width - 100, 20))

        pygame.display.flip()

class Engine:
    def __init__(self, _window):
        self.window = _window
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.render = Render(self)
        self.main_menu = Main_Menu(self)
        self.game_state = Game_State(self)
        self.retry_menu = Retry_Menu(self)
        self.scenes = [self.main_menu, self.game_state, self.retry_menu]
        self.current_scene_num = 0
        self.current_scene = self.main_menu
        self.before_click = False
    
    def detect_collide(self, obj1, obj2):
        if obj1.x < obj2.x + obj2.width and obj1.x + obj1.width > obj2.x: #if = (more strict)
            if obj1.y < obj2.y + obj2.height and obj1.y + obj1.height > obj2.y:
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
    
    def eng_menu(self):
        self.update_buttons(self.current_scene)

        click = self.is_click()

        if click:
            for button in self.current_scene.buttons:
                if button.mouse_was_hover and button.on_click != None:
                    if button.arg == None:
                        button.on_click()
                    else:
                        button.on_click(button.arg)
       
    
    def eng_game(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.current_scene.player.move("l")
        if keys[pygame.K_RIGHT]:
            self.current_scene.player.move("r")
        if keys[pygame.K_UP]:
            self.current_scene.player.move("u")
        if keys[pygame.K_DOWN]:
            self.current_scene.player.move("d")
            
        pos_player = self.current_scene.player.get_center()
        self.current_scene.ennemy.move(pos_player[0], pos_player[1])
        
        for food in self.current_scene.foods:
            if self.detect_collide(self.current_scene.player, food):
                food.eated()
                self.current_scene.add_point()
        
        if self.detect_collide(self.current_scene.player, self.current_scene.ennemy):
            self.render.update(self.current_scene)
            self.change_scene(2)

    def update(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False

            if self.current_scene_num == 0 or self.current_scene_num == 2:
                self.eng_menu()
            elif self.current_scene_num == 1:
                self.eng_game()
            self.render.update(self.current_scene)
            self.clock.tick(180)
    
    def change_scene(self, num):
        self.current_scene.on_quit()
        if num == 1:
            self.scenes[1] = Game_State(self)
        self.current_scene = self.scenes[num]
        self.current_scene_num = num
    
    def stop_all(self):
        self.is_running = False

#(width, height) = (1200, 700)
(width, height) = (1920, 1080)

pygame.init()
window = Window("Cube_game", width, height)
engine = Engine(window)

engine.update()