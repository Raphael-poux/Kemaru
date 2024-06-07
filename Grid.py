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
from copy import deepcopy
police = pygame.font.Font(None, int(30))

width = 900
height = 720
grid_width = 600
grid_height = 600
x = int(width - grid_width)/2
y = int(height - grid_height)/2
cell_color = (220, 220, 220)


# +
class cell:
    def __init__(self, x, y, i, j, width, height, value_and_group):
        self.x_pos = x + j*width
        self.y_pos = y + i*height
        self.pos = (i, j)
        self.surface = pygame.Rect(self.x_pos, self.y_pos, width, height)
        self.color = cell_color
        self.height = height
        self.width = width
        self.value = value_and_group[0]
        police = pygame.font.Font(None, int(height/1.2))
        self.text = police.render(str(self.value), True, (0, 0, 0))
        self.rect_text = self.text.get_rect(center=self.surface.center)
        self.group = value_and_group[1]
        self.clicked_on = False


    def cell_display(self, screen):
        if self.clicked_on:
            pygame.draw.rect(screen, self.color, self.surface)
        pygame.draw.rect(screen, self.color, self.surface, 1)
        if self.value:
            screen.blit(self.text, self.rect_text)

    def cell_is_clicked_on(self, event, cell_last_clicked_on, grid):
        if self.surface.collidepoint(event.pos):
            cell_last_clicked_on.cell_change(self, grid)

def grid_filled(grid, game_state):
    for row in grid:
        for cell in row:
            if not cell.value:
                return 
    game_state.transition = (game_state.current_state, 'menu')
    game_state.current_state = 'menu'
    game_state.secondary_state = False
        
        
            
def grid_and_groups_creation(file):
    matrix, number_of_groups = file
    h = len(matrix)
    w = len(matrix[0])
    cell_width = grid_width/w
    cell_height = grid_height/h
    groups = [[] for i in range(number_of_groups)]
    for i in range(h):
        for j in range(w):
            groups[matrix[j][i][1]].append((j, i))
    grid = [[cell(x, y, i, j, cell_width, cell_height, matrix[i][j]) for j in range(w)] for i in range(h)]
    return grid, groups, cell_width, cell_height


def grid_display(grid, screen):
    for row in grid:
        for cell in row:
            cell.cell_display(screen)


def groups_display(groups, screen, cell_width, cell_height):
    for group in groups:
        jmin = {}
        jmax = {}
        for i, j in group:
            if not i in jmin:
                jmin[i] = j
            jmax[i] = j
        for i in jmin:
            xg = x + jmin[i]*cell_width
            xd = x + (jmax[i] + 1)*cell_width
            yh = y + i*cell_height
            yb = y + (i+1)*cell_height
            if i == min(jmin):
                pygame.draw.line(screen, (0, 0, 0), (xg, yh), (xd, yh), 2)
            if i == max(jmin):
                pygame.draw.line(screen, (0, 0, 0), (xg, yb), (xd, yb), 2)
            if not i == min(jmin):
                pygame.draw.line(screen, (0, 0, 0), (xd, yh), (x + (jmax[i-1] + 1)*cell_width, yh), 2)
            pygame.draw.line(screen, (0, 0, 0), (xg, yh), (xg, yb), 2)
            pygame.draw.line(screen, (0, 0, 0), (xd, yh), (xd, yb), 2)
            
    
class cell_last_clicked_on:
    def __init__(self):
        self.current_pos = 0
        self.past_pos = 0

    def cell_change(self, cell, grid):
        self.past_pos = self.current_pos
        if self.past_pos:
            grid[self.past_pos[0]][self.past_pos[1]].clicked_on = False 
        self.current_pos = cell.pos
        grid[self.current_pos[0]][self.current_pos[1]].clicked_on = True 

        
    def new_number(self, grid, event):
        touche = False
        if event.key == pygame.K_1 and not grid[self.current_pos[0]][self.current_pos[1]].value:
            grid[self.current_pos[0]][self.current_pos[1]].value = 1
            touche = True
        if event.key == pygame.K_2 and not grid[self.current_pos[0]][self.current_pos[1]].value:
            grid[self.current_pos[0]][self.current_pos[1]].value = 2
            touche = True
        if event.key == pygame.K_3 and not grid[self.current_pos[0]][self.current_pos[1]].value:
            grid[self.current_pos[0]][self.current_pos[1]].value = 3
            touche = True
        if event.key == pygame.K_4 and not grid[self.current_pos[0]][self.current_pos[1]].value:
            grid[self.current_pos[0]][self.current_pos[1]].value = 4
            touche = True
        if event.key == pygame.K_5 and not grid[self.current_pos[0]][self.current_pos[1]].value:
            grid[self.current_pos[0]][self.current_pos[1]].value = 5
            touche = True
        if event.key == pygame.K_6 and not grid[self.current_pos[0]][self.current_pos[1]].value:
            grid[self.current_pos[0]][self.current_pos[1]].value = 6
            touche = True
        if event.key == pygame.K_7 and not grid[self.current_pos[0]][self.current_pos[1]].value:
            grid[self.current_pos[0]][self.current_pos[1]].value = 7
            touche = True
        if event.key == pygame.K_8 and not grid[self.current_pos[0]][self.current_pos[1]].value:
            grid[self.current_pos[0]][self.current_pos[1]].value = 8
            touche = True
        if event.key == pygame.K_9 and not grid[self.current_pos[0]][self.current_pos[1]].value:
            grid[self.current_pos[0]][self.current_pos[1]].value = 9
            touche = True
        if touche:
            police = pygame.font.Font(None, int(grid[self.current_pos[0]][self.current_pos[1]].height/1.2))
            grid[self.current_pos[0]][self.current_pos[1]].text = police.render(str(grid[self.current_pos[0]][self.current_pos[1]].value), True, (0, 0, 0))
            grid[self.current_pos[0]][self.current_pos[1]].rect_text = grid[self.current_pos[0]][self.current_pos[1]].text.get_rect(center=grid[self.current_pos[0]][self.current_pos[1]].surface.center)
            
        
def mise_a_jour_cellules(grid, steps):
    dico = steps[1]
    cellules = steps[0]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j].color = cell_color
    print(cellules)
    if not cellules == None:
        for position in cellules:
            grid[position[0]][position[1]].color = "red"

    def positions_true(bool_list):
        positions = [str(index  + 1) for index, value in enumerate(bool_list) if value]
        return ','.join(positions)
    
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if not grid[i][j].value > 0:
                grid[i][j].value = -1
                grid[i][j].text = police.render(str(positions_true(dico[(i, j)])), True, (0, 0, 0))

   