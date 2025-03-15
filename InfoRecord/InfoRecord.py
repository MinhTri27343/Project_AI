import pygame
from const import *
import sys
class InfoRecord:
    def __init__(self, screen, nameAlgorithm, search_time, expand_node, current_memory, peak_memory):
        self.screen = screen
        self.search_time = search_time
        self.expand_node = expand_node
        self.current_memory = current_memory
        self.peak_memory = peak_memory
        self.font = pygame.font.Font(None, 30)
        self.box_rect = pygame.Rect(100, 100, 400, 265)
        self.nameAlgorithm = nameAlgorithm
        self.isShowRecord = False
    def printStringToBox(self, y_offset, content, value):
        text_surface = self.font.render(f"{content}: {value}", True, BLACK)
        self.screen.blit(text_surface, (self.box_rect.x + 20, y_offset))
    def printStringToBoxVariant(self, y_offset, content):
        text_surface = self.font.render(f"{content}", True, (255, 0, 0))
        self.screen.blit(text_surface, (self.box_rect.x + 20, y_offset))
    def showRecord(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    running = False
                    return False
            pygame.draw.rect(self.screen, (211, 211, 211), self.box_rect, border_radius=10)
            y_offset = 120
            self.printStringToBox(y_offset, "Name algorithm", self.nameAlgorithm)
            y_offset += 40
            self.printStringToBox(y_offset, "Search time (s)", self.search_time)
            y_offset += 40
            self.printStringToBox(y_offset, "Current memory (MB)", self.current_memory)
            y_offset += 40
            self.printStringToBox(y_offset, "Peak memory (MB)", self.peak_memory)
            y_offset += 40
            self.printStringToBox(y_offset, "Expanded node", self.expand_node)
            y_offset += 40
            self.printStringToBoxVariant(y_offset, "Press any key to continue ...")
            pygame.display.flip()  # Cập nhật màn hình
            return True