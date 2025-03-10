import json
import pygame
from const import *
import sys
class LeaderBoard:
    def __init__(self, screen, rank_file, player):
        self.screen = screen
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.rank_file = rank_file
        self.background = pygame.transform.scale(pygame.image.load(BG_LEADERBOARD), (WIDTH, HEIGHT))
        self.rank_data = self.load_rank()
        self.player = player
    def load_rank(self):
        try:
            with open(self.rank_file, "r") as file:
                data = file.read().strip()
                if data:  # Nếu file không rỗng
                    return json.loads(data)
                else:
                    return []
        except json.JSONDecodeError as e:
            print("Error decoding JSON from rank file:", e)
            return []
        return []
    
    def save_rank(self):
        self.rank_data.append({"name": self.player.name, "score": self.player.score})
        self.rank_data.sort(key=lambda x: x["score"], reverse=True)
        with open(self.rank_file, "w") as file:
            json.dump(self.rank_data, file, indent=4)     
                       
    def show_rank(self):
        """Hiển thị bảng xếp hạng cho đến khi người dùng đóng cửa sổ."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Vẽ background và overlay
            self.screen.blit(self.background, (0, 0))            
            # Hiển thị tiêu đề bảng xếp hạng
            for i, entry in enumerate(self.rank_data[:4], start=0):
                text_name = self.font.render(f"{entry['name']}", True, WHITE)
                text_score = self.font.render(f"{entry['score']} pts", True, WHITE)
                self.screen.blit(text_name, (250, 220 + 75 * i))
                self.screen.blit(text_score, (WIDTH // 2 + 150, 220 + 75 * i))
            pygame.display.flip()

        pygame.quit()
        sys.exit()   
             