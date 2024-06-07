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
pygame.init()
import State_machine
import Interface
import Grid
import Game
import solver



pygame.display.set_caption("Kemaru")
#screen_info = pygame.display.Info()
#width = screen_info.current_w
#height = screen_info.current_h
width = 900
height = 720

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
police = pygame.font.Font(None, int(30))
black = (0, 0, 0)
white = (255, 255, 255)

Buttons = Interface.initialising()
game_state = State_machine.statemachine('menu')
cell_last_clicked_on = Grid.cell_last_clicked_on()
steps = None
cpt_steps = 0
while running:
    clock.tick(10)
    x_mouse, y_mouse = pygame.mouse.get_pos()
    screen.fill(white)
    
   
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            game_state.reset_counter()
            for button in Buttons:
                game_state.button_is_clicked_on(event, button)
            if game_state.transition_state:
                if game_state.transition == ('difficulty_level', 'game'):
                    file = Game.read_random_file(filepath = "instances/v10_b1_15.txt")
                    filepath = file[0] #I only keep the path
                    grid, groups, cell_width, cell_height = Grid.grid_and_groups_creation(file[1:]) #we can replace random by the file we want(not obligatory)
                    grille_useless, steps = solver.lancement_interface(filepath)
                    cpt_steps = 0
                    print(len(steps))
            if game_state.current_state == 'game' and not game_state.transition_state :
                for row in grid:
                    for cell in row:
                        cell.cell_is_clicked_on(event, cell_last_clicked_on, grid)
        if event.type == pygame.KEYDOWN and game_state.current_state == 'game':
            cell_last_clicked_on.new_number(grid, event)
            if event.key == pygame.K_SPACE:
                Grid.mise_a_jour_cellules(grid, steps[cpt_steps])
                cpt_steps += 1

        
    for button in Buttons:
        button.button_display(game_state.current_state, screen)
        button.mouse_over_it(x_mouse, y_mouse)


    if game_state.current_state == 'game':
        #Grid.grid_filled(grid, game_state)
        Grid.grid_display(grid, screen)
        Grid.groups_display(groups, screen, cell_width, cell_height)
                
        
    if game_state.current_state == 'quit':
        running = False

    game_state.state_apply(screen, width, height)
        
    pygame.display.update()

pygame.quit()
