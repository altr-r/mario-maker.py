import pygame
import sys

from settings import *
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos

class Editor:
    def __init__(self):

        # main setup
        self.display_surface = pygame.display.get_surface()

        # navigation
        self.origin = vector()

        # pan
        self.pan_active = False
        self.pan_offset = vector()

        # support lines
        self.support_lines_surface = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.support_lines_surface.set_colorkey('green')
        self.support_lines_surface.set_alpha(30)
    
    # event loop method // input
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            self.pan_input(event)
    
    def pan_input(self, event):
        #middle mouse button pressed or released
        if event.type == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]:
            self.pan_active = True
            self.pan_offset = vector(mouse_pos()) - self.origin
        if not mouse_buttons()[1]:
            self.pan_active = False
        
        # mouse wheels
        if event.type == pygame.MOUSEWHEEL:
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.origin.y -= event.y * 50
            else:
                self.origin.x -= event.y * 50
            
        
        if self.pan_active:
            self.origin = vector(mouse_pos()) - self.pan_offset
        
    # drawing
    def draw_tile_lines(self):
        cols = WINDOW_WIDTH // TILE_SIZE
        rows = WINDOW_HEIGHT // TILE_SIZE

        origin_offset = vector(
            x = self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE,
            y = self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE
        )

        self.support_lines_surface.fill('green')

        for col in range(cols + 1):
            x = origin_offset.x + col * TILE_SIZE
            pygame.draw.line(self.support_lines_surface, LINE_COLOR, (x, 0), (x, WINDOW_HEIGHT))

        for row in range(rows + 1):
            y = origin_offset.y + row * TILE_SIZE
            pygame.draw.line(self.support_lines_surface, LINE_COLOR, (0, y), (WINDOW_WIDTH, y))
        
        self.display_surface.blit(self.support_lines_surface, (0,0))

    
    def run(self, dt):
        self.display_surface.fill('white')
        self.event_loop()

        # drawing
        self.display_surface.fill('white')
        self.draw_tile_lines()
        pygame.draw.circle(self.display_surface, 'red', self.origin, 10)