import pygame
import pygame.locals
from const import *
class Menu:
    def __init__(self, screen):
        self.background = pygame.transform.scale(pygame.image.load(f'assets/menu_images/background_menu.png'),(WIDTH, HEIGHT))
        self.width, self.height = self.background.get_size()
        self.screen = screen
        pygame.display.set_caption("Background Example")
    def execute(self):
        running = True
        self.screen.blit(self.background, (0, 0)) #Display background
        pygame.display.flip()  # Cập nhật màn hình


        font_name = pygame.font.Font(None, 50)
        font_level = pygame.font.Font(None, 70)
        COLOR_INPUT_NAME = (252, 218, 111)

        # Kích thước và vị trí của ô nhập
        input_box = pygame.Rect(160, 430, 260, 60)
        active = False  # Kiểm tra xem ô nhập có đang được chọn không
        user_text = ""
        box_name = pygame.Rect(130, 500, 100, 60)
        box_name_image = pygame.transform.scale(pygame.image.load(f'assets/menu_images/name.png'), (320, 140))
        name_surface = font_level.render("Name", True, WHITE)
        self.screen.blit(box_name_image, box_name)
        self.screen.blit(name_surface, (box_name.x + 90, box_name.y + 40))


        button_left_image = pygame.transform.scale(pygame.image.load(f'assets/menu_images/left.png'),(100, 100))
        button_right_image = pygame.transform.scale(pygame.image.load(f'assets/menu_images/right.png'),(100, 100))
        button_left = pygame.Rect(40 , 300, 100, 100)
        button_right = pygame.Rect(450 , 300, 100, 100)
    

        levels = ["Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6" ]
        index_level = 0

        box_level = pygame.Rect(120, 280, 100, 100) #Button level
        box_level_image = pygame.transform.scale(pygame.image.load(f'assets/menu_images/name.png'), (355, 140))
        level_surface = font_level.render(levels[index_level], True, WHITE)
        self.screen.blit(box_level_image, box_level)
        self.screen.blit(level_surface, (box_level.x + 90, box_level.y + 40))

        box_play = pygame.Rect(150, 200,285,78) #Button play

 
        MAX_TEXT_DISPLAY = 13


        #================Start while=================================================
        while running:
            self.screen.blit(button_left_image, button_left)
            self.screen.blit(button_right_image, button_right)
            # Lấy vị trí chuột
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return["", 0, False]

                # Kiểm tra khi click chuột vào ô nhập
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if input_box.collidepoint(event.pos):
                        active = not active  # Bật/tắt trạng thái nhập
                    else:
                        active = False
                # Nhận dữ liệu từ bàn phím
                if event.type == pygame.KEYDOWN and active:
                    if event.key == pygame.K_BACKSPACE:
                        user_text = user_text[:-1]  # Xóa ký tự cuối
                    else:
                        user_text += event.unicode  # Thêm ký tự 
                #Nhan su kien click chuot
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if button_left.collidepoint(event.pos):
                        if index_level >= 1: index_level -= 1
                    if button_right.collidepoint(event.pos):
                        if index_level <= 4: index_level += 1
                    if box_play.collidepoint(event.pos):
                        running = False


            name_temp = user_text[-MAX_TEXT_DISPLAY:]
            text_surface = font_name.render(name_temp, True, WHITE)

            self.screen.blit(box_level_image, box_level)
            level_surface = font_level.render(levels[index_level], True, WHITE)
            self.screen.blit(level_surface, (box_level.x + 90, box_level.y + 40))

            pygame.draw.rect(self.screen, COLOR_INPUT_NAME, input_box)
            # Hiển thị nội dung nhập vào
            self.screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

            # Cập nhật màn hình
            pygame.display.flip()
        #================End while=================================================
       
        return [user_text, index_level, True]