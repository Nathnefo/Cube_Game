import pygame
import json
from color import *
from scenes import *

class Display:
    def __init__(self, title, resolution, fullscreen):
        self.set_display(resolution, fullscreen)
        pygame.display.set_caption(title)
    
    def set_display(self, resolution, fullscreen):
        self.width = resolution[0]
        self.height = resolution[1]
        if fullscreen:
            self.screen = pygame.display.set_mode((self.width , self.height), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((self.width , self.height))

class Render:
    def __init__(self, engine):
        self.display = engine.display
        self.font = pygame.font.SysFont(None, 24)
        self.title_font = pygame.font.SysFont(None, 70)

    def update(self, scene):
        """Rendering the current scene by filling the background color, blitting the entities, 
        and drawing the GUI elements, renders the fps in the top right corner"""
        if scene.background_colour != None:
            self.display.screen.fill(scene.background_colour)

        if scene.num == 1:
            for obj in engine.game.foods:
                self.display.screen.blit(obj.surface, (obj.x, obj.y))
            
            for obj in engine.game.bullets:
                self.display.screen.blit(obj.surface, (obj.x, obj.y))

        for obj in scene.entity_render_list:
            self.display.screen.blit(obj.surface, (obj.x, obj.y))
        

        for gui in scene.gui_render_list:
            gui.draw()
    
        fps = self.font.render(f'Fps : {round(engine.clock.get_fps())}', True, Color.blue)
        self.display.screen.blit(fps, (display.width - 100, 20))

        pygame.display.flip()

class Engine:
    def __init__(self, _display, _prefs):
        self.prefs = _prefs
        self.display = _display
        self.is_running = True
        self.clock = pygame.time.Clock()
        self.render = Render(self)
        self.main_menu = Main_Menu(self)
        self.game = Game(self)
        self.retry_menu = Retry_Menu(self)
        self.settings_menu = Settings_Menu(self)
        self.scenes = [self.main_menu, self.game, self.retry_menu, self.settings_menu]
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

    def update(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
            
            self.update_left_click()

            self.update_buttons()

            self.current_scene.loop()
            self.render.update(self.current_scene)
            self.clock.tick(180)
    
    def change_scene(self, num):
        """When load scene 1, make a new game"""
        self.left_click = False
        self.current_scene.on_quit()
        if num == 1:
            self.game = Game(self)
            self.scenes[1] = self.game
        self.current_scene = self.scenes[num]
        self.current_scene_num = num

    def change_settings(self, new_data):
        old_data = self.prefs.data
        prefs.load(new_data)

        if old_data["fullscreen"] != new_data["fullscreen"] or old_data["resolution"] != new_data["resolution"]:
            self.display.set_display(new_data["resolution"], new_data["fullscreen"])

    def stop_all(self):
        self.is_running = False


class Preferences():
    def __init__(self):
        """Load preferences with the file preferences.txt if an occurrence doesn't exist, create it"""
        with open('preferences.txt', "r") as f:
            raw = f.read()
        try:
            prefs = json.loads(raw)
        except:
            prefs = {}
        
        if not("fullscreen" in prefs):
            prefs["fullscreen"] = True

        if not("resolution") in prefs:
            prefs["resolution"] = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        
        with open("preferences.txt", "w") as outfile:
            json.dump(prefs, outfile)
        
        self.data = prefs
    
    def load(self, _data):
        with open("preferences.txt", "w") as outfile:
            json.dump(_data, outfile)
        self.data = _data

pygame.init()
prefs = Preferences()
display = Display("Cube_game", prefs.data["resolution"], prefs.data["fullscreen"])
engine = Engine(display, prefs)

engine.update()
pygame.quit()