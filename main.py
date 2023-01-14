import pygame
from color import *
from scenes import *

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
        self.before_click = False
    
    def detect_collide(self, obj1, obj2):
        if obj1.x < obj2.x + obj2.width and obj1.x + obj1.width > obj2.x:
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
        
            self.update_buttons(self.current_scene)
            click = self.is_click()
            if click:
                for button in self.current_scene.buttons:
                    if button.mouse_was_hover and button.on_click != None:
                        if button.arg == None:
                            button.on_click()
                        else:
                            button.on_click(button.arg)
        
            elif self.current_scene_num == 1:
                self.eng_game()
            self.render.update(self.current_scene)
            self.clock.tick(180)
    
    def change_scene(self, num):
        self.current_scene.on_quit()
        if num == 1:
            self.game = Game(self)
            self.scenes[1] = self.game
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