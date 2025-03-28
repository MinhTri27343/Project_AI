import pygame
from const import *

class InfoRecord:
    def __init__(self, screen, nameAlgorithm, search_time, expand_node, current_memory, peak_memory):
        self.screen = screen
        self.search_time = search_time
        self.expand_node = expand_node
        self.current_memory = current_memory
        self.peak_memory = peak_memory
        self.font = pygame.font.Font(None, 30)
        self.box_rect = pygame.Rect(100, 100, 400, 220)
        self.nameAlgorithm = nameAlgorithm
    def printStringToBox(self, y_offset, content, value):
        text_surface = self.font.render(f"{content}: {value}", True, BLACK)
        self.screen.blit(text_surface, (self.box_rect.x + 20, y_offset))
    def showRecord(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
            pygame.draw.rect(self.screen, (255, 165, 0), self.box_rect, border_radius=10)
            y_offset = 120
            self.printStringToBox(y_offset, "Name algorith", self.nameAlgorithm)
            y_offset += 40
            self.printStringToBox(y_offset, "Search time", self.search_time)
            y_offset += 40
            self.printStringToBox(y_offset, "Current memory", self.current_memory)
            y_offset += 40
            self.printStringToBox(y_offset, "Peak memory", self.peak_memory)
            y_offset += 40
            self.printStringToBox(y_offset, "Expand node", self.expand_node)
            pygame.display.flip()  # Cập nhật màn hình