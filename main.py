import pygame
from color import *
from scenes import *

RESOLUTION = (1920, 1080)

class Window:
    def __init__(self, title, _resolution):
        self.width = _resolution[0]
        self.height = _resolution[1]
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)

class Render:
    def __init__(self, engine):
        self.window = engine.window
        self.font = pygame.font.SysFont(None, 24)
        self.title_font = pygame.font.SysFont(None, 70)

    def update(self, scene):
        """Rendering the current scene by filling the background color, blitting the entities, 
        and drawing the GUI elements. Also renders the fps in the top right corner"""
        if scene.background_colour != None:
            self.window.screen.fill(scene.background_colour)

        for obj in scene.entity_render_list:
            self.window.screen.blit(obj.surface, (obj.x, obj.y))
        
        if scene.num == 1:
            for obj in engine.game.foods:
                self.window.screen.blit(obj.surface, (obj.x, obj.y))

        for gui in scene.gui_render_list:
            gui.draw()
    
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
        self.game = Game(self)
        self.retry_menu = Retry_Menu(self)
        self.scenes = [self.main_menu, self.game, self.retry_menu]
        self.current_scene_num = 0
        self.current_scene = self.main_menu

        self.left_click = False
        self.left_was_pressed = False
    
    def detect_collide(self, obj1, obj2):
        """Detect if two objects collide by checking if their coordinates overlap"""
        if obj1.x < obj2.x + obj2.width and obj1.x + obj1.width > obj2.x:
            if obj1.y < obj2.y + obj2.height and obj1.y + obj1.height > obj2.y:
                return True
        return False
    
    def mouse_hover(self, x, y, element):
        if (x > element.x and x < element.x + element.width) and (y > element.y and y < element.y + element.height):
            return True
        return False

    def update_buttons(self):
        mouse = pygame.mouse.get_pos()
        for button in self.current_scene.buttons:
            mouse_is_hover = self.mouse_hover(mouse[0], mouse[1], button)

            """Button click event"""
            if mouse_is_hover and self.left_click and button.on_click != None:
                if button.arg == None:
                    button.on_click()
                else:
                    button.on_click(button.arg)
            
            """Mouse hover events"""
            if not(button.mouse_was_hover) and mouse_is_hover:
                button.on_mouse_hover()
                button.mouse_was_hover = True
            elif button.mouse_was_hover and not(mouse_is_hover):
                button.on_mouse_quit()
                button.mouse_was_hover = False


    def update_left_click(self):
        """Detect if the left key is pressed and make a detection of a click"""
        left_pressed, middle, right = pygame.mouse.get_pressed()
        if self.left_click:
            self.left_click = False
        elif not(self.left_was_pressed) and left_pressed:
            self.left_click = True
        if self.left_was_pressed != left_pressed:
            self.left_was_pressed = left_pressed
    
    def main_game_loop(self):
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
        
        """On collision between the player and the enemy, end the game"""
        if self.detect_collide(self.current_scene.player, self.current_scene.ennemy):
            self.render.update(self.current_scene)
            self.change_scene(2)

    def update(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
            
            self.update_left_click()
    
            self.update_buttons()

            if self.current_scene_num == 1:
                self.main_game_loop()
            self.render.update(self.current_scene)
            self.clock.tick(180)
    
    def change_scene(self, num):
        """When load scene 1, make a new game"""
        self.current_scene.on_quit()
        if num == 1:
            self.game = Game(self)
            self.scenes[1] = self.game
        self.current_scene = self.scenes[num]
        self.current_scene_num = num
    
    def stop_all(self):
        self.is_running = False

pygame.init()
window = Window("Cube_game", RESOLUTION)
engine = Engine(window)

engine.update()