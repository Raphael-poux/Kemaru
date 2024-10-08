import pygame

# On définit une machine à états afin de pourvoir connaître les paramètres de jeu et la fenêtre à afficher
# +
class statemachine:
    def __init__(self, initial_state):
        self.current_state = initial_state
        self.secondary_state = 'None'
        self.music = True
        self.transition = (initial_state, initial_state)
        self.transition_state = False
        self.grid_dico = False
        self.niveau_0 = True
        self.ai = False
    
    def button_is_clicked_on(self, event, button):
        if (not self.transition_state) and self.current_state in button.entry_states and button.surface.collidepoint(event.pos):
            self.transition = (self.current_state, button.main_state)
            self.current_state = button.main_state
            self.transition_state = True
            if button.secondary_state:
                self.secondary_state = button.secondary_state
                
        if self.current_state == 'music':
            self.current_state = 'menu'
            self.music = not self.music
            if self.music:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.stop()

    def reset_counter(self):
        self.transition_state = False    

    def state_apply(self, screen, width, height):
            
        if self.current_state == 'menu':
            title = pygame.font.Font(None, int(200/900*width)).render('Kemaru', True, (0, 0, 0))
            rect_title = title.get_rect(center=(int(width/2), int(height/4)))
            screen.blit(title, rect_title)
        
        if self.current_state == 'how_to_play':
            pass
        
    

        
    
