# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.15.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
import pygame 
import sys

black = (0, 0, 0)
white = (255, 255, 255)
screen_info = pygame.display.Info()
#width = screen_info.current_w
#height = screen_info.current_h
width = 900
height = 720
police = pygame.font.Font(None, int(60/900*width))
button_width = int(150/900*width)
button_height = int(55/900*height)
x_middle = int((width - button_width)/2)
y_middle = int((height - button_height)/2)
gap = int(3/2*button_height)


# +
class button:
    def __init__(self, text, rect, main_state, *entry_states, secondary_state = False, text_police = police, text_color = black, 
                 surface_color = white, edge_color = black, filling = False, edge_width = 0):
        self.entry_states = entry_states
        self.main_state = main_state
        self.secondary_state = secondary_state
        self.surface = pygame.Rect(*rect)
        self.surface_color = surface_color
        self.text = text_police.render(text, True, text_color)
        self.rect_text = self.text.get_rect(center=self.surface.center)
        self.edge_width = edge_width
        self.filling = filling
        self.edge_color = edge_color
        self.rect = rect
        self.mouse_over = False
        
    def mouse_over_it(self, x, y):
        self.mouse_over = self.surface.collidepoint(x, y)

    def button_display_mouse_over(self, screen):
        pygame.draw.rect(screen, (0, 0, 0), self.surface, self.edge_width)
        screen.blit(self.text, self.rect_text)        
    
    def button_display(self, state, screen):
        if state in self.entry_states:
            if self.mouse_over:
                self.button_display_mouse_over(screen)
                return
            if self.filling:
                pygame.draw.rect(screen, self.surface_color, self.surface)
            if self.edge_width:
                pygame.draw.rect(screen, self.edge_color, self.surface, self.edge_width)
            screen.blit(self.text, self.rect_text)

        
class background:
    def __init__(self, state, path, width, height):
        self.state = state
        self.image = pygame.transform.scale(pygame.image.load(path), (width, height))

    def background_display(self, main_state, secondary_state, screen):
        if self.state == main_state or self.state == secondary_state:
            screen.blit(self.image, (0, 0))

def initialising():
    Play = button('Play', (x_middle, y_middle, button_width, button_height), 'difficulty_level', 'menu', edge_color = white, edge_width = 1)
    Rules = button('Rules', (x_middle, y_middle + gap, button_width, button_height), 'rules', 'menu', edge_color = white, edge_width = 1)
    Music = button('Music', (x_middle, y_middle + 2*gap, button_width, button_height), 'music', 'menu', edge_color = white, edge_width = 1)
    Easy = button('Easy', (x_middle, y_middle + gap, button_width, button_height), 'game', 'difficulty_level', secondary_state = 'easy', edge_color = white, edge_width = 1)
    Medium = button('Medium', (x_middle, y_middle + 2*gap, button_width, button_height), 'game', 'difficulty_level', secondary_state = 'medium', edge_color = white, edge_width = 1)
    Hard = button('Hard', (x_middle, y_middle + 3*gap, button_width, button_height), 'game', 'difficulty_level', secondary_state = 'hard', edge_color = white, edge_width = 1)
    Menu = button('Menu',(x_middle, y_middle, button_width, button_height), 'menu', 'victory', 'difficulty_level', 'rules', edge_color = white, edge_width = 1)
    Quit = button('Quit', (x_middle, y_middle + 3*gap, button_width, button_height), 'quit', 'menu', edge_color = white, edge_width = 1)
    return [Play, Rules, Music, Easy, Medium, Hard, Menu, Quit]
