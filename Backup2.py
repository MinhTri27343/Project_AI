import pygame
import time

class GameOverScreen:
    def __init__(self, width=800, height=600):
        """Khởi tạo màn hình Game Over"""
        pygame.init()
        self.WIDTH, self.HEIGHT = width, height
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Game Over Screen")
        
        # Danh sách màu để đổi màu chữ
        self.colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0),
                       (0, 255, 0), (0, 255, 255), (0, 0, 255), (128, 0, 128)]
        
        # Load font
        self.font = pygame.font.Font(None, 100)

    def animate_text(self):
        """Hiệu ứng đổi màu chữ 'GAME OVER'"""
        for i in range(10):  # Lặp để tạo hiệu ứng
            self.screen.fill((0, 0, 0))  # Xóa màn hình
            color = self.colors[i % len(self.colors)]
            text_surface = self.font.render("GAME OVER", True, color)
            text_rect = text_surface.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2))
            self.screen.blit(text_surface, text_rect)
            pygame.display.flip()
            time.sleep(0.3)  # Dừng lại 0.3 giây để tạo hiệu ứng

    def run(self):
        """Chạy màn hình Game Over và chờ người dùng thoát"""
        self.animate_text()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    running = False  # Nhấn phím bất kỳ để thoát

        pygame.quit()


# Chạy chương trình
if __name__ == "__main__":
    game_over = GameOverScreen()
    game_over.run()
