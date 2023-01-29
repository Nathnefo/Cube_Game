import random
from color import *
from entities import *
from gui import *

class Scene:
    def __init__(self, _num, _background_colour, _entity_render_list, _gui_render_list, _buttons):
        self.num = _num
        self.background_colour = _background_colour
        self.entity_render_list = _entity_render_list
        self.gui_render_list = _gui_render_list + _buttons
        self.buttons = _buttons

    def on_quit(self):
        for button in self.buttons:
            if button.mouse_was_hover:
                button.on_mouse_quit()
                button.mouse_was_hover = False

class Game(Scene):
    def __init__(self, _engine):
        self.engine = _engine
        display = _engine.display
        self.player = Player(display.width//2, display.height//2, display)
        self.ennemy = Ennemy(1800, 0, 25, 25, 2, Color.red)
        self.foods = [Food(display) for _ in range(5)]
        self.point = 0
        self.text_point = Text(self.engine, 20, 20, _text="Points : {self.engine.game.point}", _color=Color.black, _size=50, _fstring=True)
        self.upgrade_button = Button(self.engine, display.width - 200, 85, _text="Upgrade speed (cost 20)", _color=Color.black, _hover_color=Color.l_grey, _on_click=self.upgrade_speed)
        self.food_button = Button(self.engine, display.width - 200, 150, _text="Upgrade food (cost 5)", _color=Color.black, _hover_color=Color.l_grey, _on_click=self.upgrade_food)

        super().__init__(1, Color.white, [self.ennemy, self.player], [self.text_point], [self.upgrade_button, self.food_button])

    def add_point(self):
        self.point += 1
    
    def upgrade_speed(self):
        if self.point >= 20:
            self.point-= 20
            self.player.speed += 1
    
    def upgrade_food(self):
        if self.point >= 5:
            self.point-=5
            self.foods += [Food(self.engine.display)]

class Main_Menu(Scene):
    def __init__(self, engine):
        display = engine.display
        self.title = Text(engine, display.width//2, display.height//4, _text="The Cube Game", _color=Color.blue, _size=70, _centered=True)
        self.play_button = Button(engine, display.width//2- 100, display.height//2- 25, _text="Play", _on_click=engine.change_scene, _arg = 1)
        self.settings_button = Button(engine, display.width//2- 100, display.height//2 + 30, _text="Settings", _hover_color=Color.grey, _on_click=engine.change_scene, _arg = 3)
        self.leave_button = Button(engine, display.width//2- 100, display.height//2 + 85, _text="Quit", _hover_color=Color.red, _on_click=engine.stop_all)

        super().__init__(0, Color.l_grey, [], [self.title], [self.play_button, self.settings_button, self.leave_button])


class Settings_Menu(Scene):
    def __init__(self, engine):
        self.engine = engine
        display = engine.display
        self.title = Text(engine, display.width//2, 150, _text="Settings", _color=Color.blue, _size=70, _centered=True)
        self.back_button = Button(engine, 50, 50, _width=75, _text="Back", _on_click=engine.change_scene, _arg = 0)
        self.fullscreen_text = Text(engine, 50, display.height // 5, _text="Fullscreen", _color=Color.black, _size=40)
        self.check_mark_fullscreen = Check_mark(engine, 225, display.height // 5, 30, 30, _state=engine.prefs.data["fullscreen"])
        self.apply_button = Button(engine, display.width//2- 100, display.height//2 + 85, _text="Apply", _hover_color=Color.l_green, _on_click=self.apply)
    
        super().__init__(3, Color.l_grey, [], [self.title, self.fullscreen_text], [self.back_button, self.check_mark_fullscreen, self.apply_button])
        
    def apply(self):
        prefs = {"fullscreen" : self.check_mark_fullscreen.state, "resolution" : (pygame.display.Info().current_w, pygame.display.Info().current_h)}
        self.engine.change_settings(prefs)


class Retry_Menu(Scene):
    def __init__(self, engine):
        display = engine.display
        self.retry_button = Button(engine, display.width//2- 100, display.height//2 - 55, _text="Retry", _on_click=engine.change_scene,_arg = 1 )
        self.main_menu_button = Button(engine, display.width//2- 100, display.height//2, _text="Main Menu", _hover_color=Color.grey, _on_click=engine.change_scene, _arg = 0)
        self.leave_button = Button(engine, display.width//2- 100, display.height//2 + 55, _text="Quit", _hover_color=Color.red, _on_click=engine.stop_all)

        super().__init__(2, None, [], [], [self.retry_button, self.main_menu_button, self.leave_button])