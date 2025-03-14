import json
import pygame
from const import *
import sys
class LeaderBoard:
    def __init__(self, screen, rank_file, player):
        self.screen = screen
        self.font_leaderboard = pygame.font.Font(None, FONT_SIZE)
        self.font_back = pygame.font.Font(None, 40)
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
        self.screen.blit(self.background, (0, 0))
        box_back_menu_image = pygame.transform.scale(pygame.image.load(f'assets/background_images/back_menu.png'),(200, 50))
        box_back_menu = pygame.Rect(20, 560, 200, 50)  
        text_back_menu = "Back menu"
        surface_back_menu = self.font_back.render(text_back_menu, True, WHITE) 
        self.screen.blit(box_back_menu_image, box_back_menu)
        self.screen.blit(surface_back_menu, (box_back_menu.x + 20, box_back_menu.y + 10)) 
        running = True
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

           
            # Hiển thị tiêu đề bảng xếp hạng
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if box_back_menu.collidepoint(event.pos):
                        return True
            for i, entry in enumerate(self.rank_data[:4], start=0):
                text_name = self.font_leaderboard.render(f"{entry['name']}", True, WHITE)
                text_score = self.font_leaderboard.render(f"{entry['score']} pts", True, WHITE)
                self.screen.blit(text_name, (250, 220 + 75 * i))
                self.screen.blit(text_score, (WIDTH // 2 + 150, 220 + 75 * i))
            pygame.display.flip()
        return False


             