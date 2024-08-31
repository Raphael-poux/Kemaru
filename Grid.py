import pygame
import numpy as np


screen_info = pygame.display.Info()
width = screen_info.current_w
height = screen_info.current_h
grid_height = 600
y_default = int(height - grid_height)/2
x_default = int(width - grid_height)/2
cell_color = (220, 220, 220)


# +
class cell:
    def __init__(self, x, y, i, j, width, height, value_and_group):
        self.x_pos = x + j*width
        self.y_pos = y + i*height
        self.pos = (i, j)
        self.surface = pygame.Rect(self.x_pos, self.y_pos, width, height)
        self.color = cell_color
        self.found = False
        self.useful = False
        self.height = height
        self.width = width
        self.value = value_and_group[0]
        self.modify = False
        if not self.value:
            self.modify = True
        self.police_2 = pygame.font.Font(None, int(height/4))
        self.police = pygame.font.Font(None, int(height/1.2))
        self.text = self.police.render(str(self.value), True, (0, 0, 0))
        self.rect_text = self.text.get_rect(center=self.surface.center)
        self.text_possible_values = False
        self.rect_text_possible_values = False
        self.group = value_and_group[1]
        self.clicked_on = False
        if i == 0 and j == 0:
            self.clicked_on = True


    def cell_display(self, screen, grid_dico, ai):
        if self.clicked_on and not ai:
            pygame.draw.rect(screen, self.color, self.surface)
        if self.useful:
            pygame.draw.rect(screen, 'red', self.surface)
        if self.found:
            pygame.draw.rect(screen, 'blue', self.surface)
        pygame.draw.rect(screen, self.color, self.surface, 1)
        if self.value:
            screen.blit(self.text, self.rect_text)
        if not self.text_possible_values == False and not self.value and grid_dico:
             self.rect_text_possible_values = self.text_possible_values.get_rect(center= (self.surface.center[0], self.surface.center[1] - int(self.height/8*3)))
             screen.blit(self.text_possible_values, self.rect_text_possible_values)
    

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
      
        
            
def grid_and_groups_creation(file, list_x, list_y):
    nb_grilles = len(list_x)
    matrix, number_of_groups = file
    h = len(matrix)
    w = len(matrix[0])
    real_grid_height = min(2*grid_height/nb_grilles, 600)
    cell_height = real_grid_height/h
    cell_width = real_grid_height/w
    groups = [[] for i in range(number_of_groups)]
    for i in range(w):
        for j in range(h):
            groups[matrix[j][i][1]].append((j, i))
    grid = []
    for i in range(nb_grilles):
        grid.append([[cell(list_x[i], list_y[i], k, j, cell_width, cell_height, matrix[k][j]) for j in range(w)] for k in range(h)])
    return grid, groups, cell_width, cell_height, h, w


def grid_display(grids, screen, grid_dico, ai):
    for grid in grids:
        for row in grid:
            for cell in row:
                cell.cell_display(screen, grid_dico,ai)


def groups_display(groups, screen, cell_width, cell_height, list_x = [x_default], list_y = [y_default]):
    for i in range(len(list_x)):
        x = list_x[i]
        y = list_y[i]
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
        self.current_pos = (0, 0)
        self.past_pos = (0, 0)

    def cell_is_keydown_on(self, event, grid, i, j):
        x, y = self.current_pos
        if event.key == pygame.K_UP:
            x = (x - 1) % i
        if event.key == pygame.K_DOWN:
            x = (x + 1) % i
        if event.key == pygame.K_RIGHT:
            y = (y + 1) % j
        if event.key == pygame.K_LEFT:
            y = (y - 1) % j
        self.cell_change(grid[x][y], grid)
        
    def cell_change(self, cell, grid):
        self.past_pos = self.current_pos
        grid[self.past_pos[0]][self.past_pos[1]].clicked_on = False 
        self.current_pos = cell.pos
        grid[self.current_pos[0]][self.current_pos[1]].clicked_on = True 

        
    def new_number(self, grids, event, grille, grid_dico_state, grid_dico):
        grid = grids[0]
        if not self.current_pos == 0:
            i = self.current_pos[0]
            j = self.current_pos[1]
        touche = False
        dico_change = False
        if event.key == pygame.K_1:
            if grid[i][j].modify and (not grid_dico_state or grid[i][j].value):
                grid[i][j].value = 1
                touche = True
            if grid[i][j].modify and grid_dico_state and len(grid_dico[(i, j)]) > 0:
                dico_change = True
                grid_dico[(i, j)][0] = not grid_dico[(i, j)][0]
        if event.key == pygame.K_2:
            if grid[i][j].modify and (not grid_dico_state or grid[i][j].value):
                grid[i][j].value = 2
                touche = True
            if grid[i][j].modify and grid_dico_state and len(grid_dico[(i, j)]) > 1:
                dico_change = True
                grid_dico[(i, j)][1] = not grid_dico[(i, j)][1]
        if event.key == pygame.K_3:
            if grid[i][j].modify and (not grid_dico_state or grid[i][j].value):
                grid[i][j].value = 3
                touche = True
            if grid[i][j].modify and grid_dico_state and len(grid_dico[(i, j)]) > 2:
                dico_change = True
                grid_dico[(i, j)][2] = not grid_dico[(i, j)][2]
        if event.key == pygame.K_4:
            if grid[i][j].modify and (not grid_dico_state or grid[i][j].value):
                grid[i][j].value = 4
                touche = True
            if grid[i][j].modify and grid_dico_state and len(grid_dico[(i, j)]) > 3:
                dico_change = True
                grid_dico[(i, j)][3] = not grid_dico[(i, j)][3]
        if event.key == pygame.K_5:
            if grid[i][j].modify and (not grid_dico_state or grid[i][j].value):
                grid[i][j].value = 5
                touche = True
            if grid[i][j].modify and grid_dico_state and len(grid_dico[(i, j)]) > 4:
                dico_change = True
                grid_dico[(i, j)][4] = not grid_dico[(i, j)][4]
        if event.key == pygame.K_6:
            if grid[i][j].modify and (not grid_dico_state or grid[i][j].value):
                grid[i][j].value = 6
                touche = True
            if grid[i][j].modify and grid_dico_state and len(grid_dico[(i, j)]) > 5:
                dico_change = True
                grid_dico[(i, j)][5] = not grid_dico[(i, j)][5]
        if event.key == pygame.K_7:
            if grid[i][j].modify and (not grid_dico_state or grid[i][j].value):
                grid[i][j].value = 7
                touche = True
            if grid[i][j].modify and grid_dico_state and len(grid_dico[(i, j)]) > 6:
                dico_change = True
                grid_dico[(i, j)][6] = not grid_dico[(i, j)][6]
        if event.key == pygame.K_8:
            if grid[i][j].modify and (not grid_dico_state or grid[i][j].value):
                grid[i][j].value = 8
                touche = True
            if grid[i][j].modify and grid_dico_state and len(grid_dico[(i, j)]) > 7:
                dico_change = True
                grid_dico[(i, j)][7] = not grid_dico[(i, j)][7]
        if event.key == pygame.K_9:
            if grid[i][j].modify and (not grid_dico_state or grid[i][j].value):
                grid[i][j].value = 9
                touche = True
            if grid[i][j].modify and grid_dico_state and len(grid_dico[(i, j)]) > 8:
                dico_change = True
                grid_dico[(i, j)][8] = not grid_dico[(i, j)][8]
        if touche:
            grid[i][j].text = grid[i][j].police.render(str(grid[i][j].value), True, (0, 0, 0))
            grid[i][j].rect_text =grid[i][j].text.get_rect(center=grid[self.current_pos[0]][self.current_pos[1]].surface.center)
            grille[i][j][0] = grid[i][j].value
        if dico_change:
            mise_a_jour_cellules2(grids, grid_dico, grille)

def positions_true(bool_list):
    positions = [str(index  + 1) for index, value in enumerate(bool_list) if value]
    return ','.join(positions)

def mise_a_jour_cellules(grids, steps, grille):
    for grid in grids:
        cellules = steps[0]
        dico = steps[1]
        i, j = steps[2]
        for x in range(len(grid)):
            for y in range(len(grid[0])):
                grid[x][y].useful = False
                grid[x][y].found = False
        for position in cellules:
                grid[position[0]][position[1]].useful = True
        grid[i][j].found = True
        if not grid[i][j].value > 0:
            text = str(positions_true(dico[(i, j)]))
            grid[i][j].text_possible_values = grid[i][j].police_2.render(text, True, (0, 0, 0))
            if len(text) == 1:
                grid[i][j].value = int(text)
                grid[i][j].text = grid[i][j].police.render(str(grid[i][j].value), True, (0, 0, 0))
                grid[i][j].rect_text = grid[i][j].text.get_rect(center = grid[i][j].surface.center)
                grille[i][j][0] = grid[i][j].value
        

def mise_a_jour_cellules2(grids, dico, grille):
    for grid in grids:
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if not grid[i][j].value > 0:
                    text = str(positions_true(dico[(i, j)]))
                    grid[i][j].text_possible_values = grid[i][j].police_2.render(text, True, (0, 0, 0))
                    if len(text) == 1:
                        grid[i][j].value = int(text)
                        grid[i][j].text = grid[i][j].police.render(str(grid[i][j].value), True, (0, 0, 0))
                        grid[i][j].rect_text = grid[i][j].text.get_rect(center = grid[i][j].surface.center)
                        grille[i][j][0] = grid[i][j].value

            
        
