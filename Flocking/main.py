import pygame
import pygame_gui
import time
from pygame_gui.elements import UILabel, UIButton
from pygame.locals import QUIT
from member import *
from setting import *

# Khởi tạo Pygame
pygame.init()
pygame.font.init()
font = pygame.font.Font(None, 24)  # Tạo đối tượng Font với kích thước 24
screen = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()

# Khởi tạo UIManager
ui_manager = pygame_gui.UIManager((1200, 700))

class GameController:
    def __init__(self):
        self.members = pygame.sprite.Group()
        self.init_members()
        
    def init_members(self):
        for _ in range(NUMBER_OF_MEMBERS):
            member = Member(self)
            self.members.add(member)
    def update(self):
        self.members.update()

    def clear_members(self):
        self.members.empty()

    def draw(self, surface):
        surface.fill((0, 0, 0))
        self.members.draw(surface)

    def handle_events(self):
        global NUMBER_OF_MEMBERS
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == slider_1:
                        VALUE[2] = event.value
                    elif event.ui_element == slider_2:
                        VALUE[3] = event.value
                    elif event.ui_element == slider_3:
                        VALUE[4] = event.value
                    elif event.ui_element == slider_0:
                        VALUE[1] = (int)(event.value)
                elif event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == button:
                        NUMBER_OF_MEMBERS = 50
                        self.clear_members()
                        self.init_members()
                    elif event.ui_element == button1:
                        NUMBER_OF_MEMBERS = 100
                        self.clear_members()
                        self.init_members()
                    elif event.ui_element == button2:
                        NUMBER_OF_MEMBERS = 200
                        self.clear_members()
                        self.init_members()
                    elif event.ui_element == button3:
                        NUMBER_OF_MEMBERS = 350
                        self.clear_members()
                        self.init_members()
                    
            ui_manager.process_events(event)

    def run(self):
        while True:
            time_delta = clock.tick(fps*LEVEL[VALUE[1]]) / 1000.0

            self.handle_events()

            self.update()

            ui_manager.update(time_delta)

            self.draw(screen)
            ui_manager.draw_ui(screen)

            pygame.display.flip()

title = ["Speed", "Wander priority", "Cohesion priority", "Alignment priority", "Numbers enemy"]
game_controller = GameController()
text_label = UILabel(relative_rect=pygame.Rect((300, 0), (300, 100)),
                     text="Simulate the flocking",
                     manager=ui_manager)
text_label = UILabel(relative_rect=pygame.Rect((800, 0), (200, 100)),
                     text="SETTING",
                     manager=ui_manager)
for i in range(0, 5):
    text_label = UILabel(relative_rect=pygame.Rect((800, 50*i + 75), (200, 20)),
                        text=title[i],
                        manager=ui_manager)
slider_0 = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((800, 100), (200, 20)),
                                                  start_value=VALUE[1],
                                                  value_range=(0, 4),
                                                  manager=ui_manager)
slider_1 = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((800, 150), (200, 20)),
                                                  start_value=VALUE[2],
                                                  value_range=(0.25, 4),
                                                  manager=ui_manager)
slider_2 = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((800, 200), (200, 20)),
                                                  start_value=VALUE[3],
                                                  value_range=(0, 4),
                                                  manager=ui_manager)
slider_3 = pygame_gui.elements.UIHorizontalSlider(relative_rect=pygame.Rect((800, 250), (200, 20)),
                                                  start_value=VALUE[4],
                                                  value_range=(0, 4),
                                                  manager=ui_manager)
button = UIButton(relative_rect=pygame.Rect((800, 300), (100, 30)),
                  text="50",
                  manager=ui_manager)
button1 = UIButton(relative_rect=pygame.Rect((900, 300), (100, 30)),
                  text="100",
                  manager=ui_manager)
button2 = UIButton(relative_rect=pygame.Rect((800, 350), (100, 30)),
                  text="200",
                  manager=ui_manager)
button3 = UIButton(relative_rect=pygame.Rect((900, 350), (100, 30)),
                  text="350",
                  manager=ui_manager)              
game_controller.run()