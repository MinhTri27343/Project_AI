import pygame
import time
from utils import *
from const import *
class EndGameScreen:
    def __init__(self, text):
        self.text = text
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.colors = colors
        self.font = pygame.font.Font(None, 100)
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def animate_text(self):
        for i in range(10):  # Lặp để tạo hiệu ứng
            self.screen.fill((0, 0, 0))  # Xóa màn hình
            color = self.colors[i % len(self.colors)]
            text_surface = self.font.render(self.text, True, color)
            text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)
            pygame.display.flip()
            time.sleep(0.3)  # Dừng lại 0.3 giây để tạo hiệu ứng

    # def run(self):
    #     """Chạy màn hình Game Over và chờ người dùng thoát"""
    #     self.animate_text()
    #     running = True
    #     while running:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
    #                 running = False  # Nhấn phím bất kỳ để thoát

    #     pygame.quit()


# # Chạy chương trình
# if __name__ == "__main__":
#     game_over = EndGameScreen:()
#     game_over.run()
