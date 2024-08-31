import pygame
import numpy as np
pygame.init()
import State_machine
import Interface
import Grid
import Game
import sol_int
pygame.display.set_caption("Kemaru")
screen_info = pygame.display.Info()
width = screen_info.current_w
height = screen_info.current_h
y_default = int(height - 600)/2
x_default = int(width - 600)/2


screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
running = True
police = pygame.font.Font(None, int(20*height/720))
black = (0, 0, 0)
white = (255, 255, 255)

Buttons = Interface.initialising()
game_state = State_machine.statemachine('menu')
cell_last_clicked_on = Grid.cell_last_clicked_on()
steps = None
list_x = [x_default]
list_y = [y_default]


while running:
    clock.tick(10)
    x_mouse, y_mouse = pygame.mouse.get_pos()
    screen.fill(white)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            game_state.reset_counter()
            for button in Buttons:
                game_state.button_is_clicked_on(event, button)
            if game_state.transition_state:
                if game_state.transition == ('difficulty_level_ai','game'):
                    game_state.ai = True
                if game_state.transition == ('difficulty_level','game'):
                    game_state.ai = False
                if game_state.transition == ('difficulty_level', 'game') or game_state.transition == ('difficulty_level_ai','game'):
                    file = Game.read_random_file('instances/example.txt')
                    filepath = file[0] #I only keep the path
                    # gestion d'une grille
                    grids, groups, cell_width, cell_height, imax, jmax = Grid.grid_and_groups_creation(file[1:], list_x, list_y)
                    grille = sol_int.transformation(filepath)
                    grid_dico = sol_int.lancement_interface(grille, return_dico = True)
                    if game_state.ai:
                        #instruction
                        instruction_string = sol_int.plus_court_chemin_non_récursif_maximisation_informations(grille)
                        instructions = sol_int.string_conversion(instruction_string)
                        cpt_instruction_max = len(instructions)
                        cpt_instruction = 0
                        donnees = sol_int.données_grille(grille)
                        steps = sol_int.niveau_0_interface(grille, *donnees)[1]
                        cpt_steps = 0
                        cpt_steps_max = len(steps)
                        game_state.grid_dico = not game_state.grid_dico
                        Grid.mise_a_jour_cellules2(grids, grid_dico, grille)
                        print(instructions)
            if game_state.current_state == 'game' and not game_state.ai:
                for row in grids[0]:
                    for cell in row:
                        cell.cell_is_clicked_on(event, cell_last_clicked_on, grids[0])
        if event.type == pygame.KEYDOWN and game_state.current_state == 'game':
            if not game_state.ai:
                cell_last_clicked_on.cell_is_keydown_on(event, grids[0], imax, jmax)
                cell_last_clicked_on.new_number(grids, event, grille, game_state.grid_dico, grid_dico)
            if event.key == pygame.K_SPACE:
                game_state.grid_dico = not game_state.grid_dico
                Grid.mise_a_jour_cellules2(grids, grid_dico, grille)
            if event.key == pygame.K_s and game_state.ai:
                if game_state.niveau_0:
                    if cpt_steps < cpt_steps_max :
                        grid_dico = steps[cpt_steps][1]
                        Grid.mise_a_jour_cellules(grids, steps[cpt_steps], grille)
                        cpt_steps += 1
                    elif cpt_instruction < cpt_instruction_max - 1:
                        cpt_instruction += 1
                        game_state.niveau_0 = False
                        donnees = sol_int.données_grille(grille)
                        donnees[0] = grid_dico
                        explo_niveau_1 = sol_int.niveau_1_interface(instructions[cpt_instruction][1], grille, *donnees)
                        correspondance = [key for key in explo_niveau_1 if key != 0]
                        cpt_steps_max = [len(explo_niveau_1[i]) for i in correspondance]
                        cpt_steps = [0]*len(explo_niveau_1)                        
                        nb_grilles = len(explo_niveau_1) - 1
                        if nb_grilles == 2:
                            list_x = [ int(width/4 - 300), int(3*width/4 - 300)]
                            list_y = [y_default, y_default]
                        if nb_grilles == 3:
                            list_x = [int(width/4 - 200), int(3*width/4 - 200), int(width/2 - 200)]
                            list_y = [int(height/4 - 150), int(height/4 - 150), int(3*height/4 - 150)]
                        if nb_grilles == 4:
                            list_x = [int(width/4 - 150), int(3*width/4 - 150), int(width/4 - 150), int(3*width/4 - 150)]
                            list_y = [int(height/4 - 150), int(height/4 - 150), int(3*height/4 - 150), int(3*height/4 - 150)]
                        
                        grids, groups, cell_width, cell_height, imax, jmax = Grid.grid_and_groups_creation(file[1:], list_x, list_y)
                        for i in range(nb_grilles):
                            Grid.mise_a_jour_cellules2([grids[i]], explo_niveau_1[correspondance[i]][0][1], grille)
                if not game_state.niveau_0:
                    in_progress = False
                    for i in range(nb_grilles):
                        if cpt_steps[i] < cpt_steps_max[i]:
                            Grid.mise_a_jour_cellules([grids[i]], explo_niveau_1[correspondance[i]][cpt_steps[i]], grille)
                            cpt_steps[i] += 1
                            in_progress = True
                    if not in_progress:
                        grid_dico = explo_niveau_1[0]
                        cpt_instruction += 1
                        game_state.niveau_0 = True
                        donnees = sol_int.données_grille(grille)
                        donnees[0] = grid_dico
                        list_x = [x_default]
                        list_y = [y_default]
                        grids, groups, cell_width, cell_height, imax, jmax = Grid.grid_and_groups_creation(file[1:], list_x, list_y)
                        Grid.mise_a_jour_cellules2(grids, grid_dico, grille)
                        steps = sol_int.niveau_0_interface(grille, *donnees)[1]
                        cpt_steps = 0
                        cpt_steps_max = len(steps)
                    


                                                          
    for button in Buttons:
        button.button_display(game_state.current_state, screen)
        button.mouse_over_it(x_mouse, y_mouse)


    if game_state.current_state == 'game':
        Grid.grid_display(grids, screen, game_state.grid_dico, game_state.ai)
        Grid.groups_display(groups, screen, cell_width, cell_height, list_x, list_y)      
        
    if game_state.current_state == 'quit':
        running = False

    game_state.state_apply(screen, width, height)
        
    pygame.display.update()

pygame.quit()
