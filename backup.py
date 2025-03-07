import pygame
import queue
from collections import deque
import math
from const import *
from board import boards
import os


def bfs(matrix, row_start, col_start, row_end, col_end):
    
    rows, cols = len(matrix), len(matrix[0])
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Lên, xuống, trái, phải
    
    # Kiểm tra nếu điểm bắt đầu hoặc kết thúc không thể đi được
    if matrix[row_start][col_start] in range(2, 9) or matrix[row_end][col_end] in range(2, 9):
        return None
    
    queue = deque([(row_start, col_start, [])])
    visited = set()
    visited.add((row_start, col_start))
    while queue:
        x, y, path = queue.popleft()
        
        # Nếu đến đích, trả về đường đi
        if (x, y) == (row_end, col_end):
            return path + [(x, y)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and (nx, ny) not in visited:
                if matrix[nx][ny] in (0, 1, 9):  # Chỉ đi được nếu là 0, 1 hoặc 9
                    visited.add((nx, ny))
                    queue.append((nx, ny, path + [(x, y)]))
    
    return None  # Không tìm thấy đường đi

def convert_coordinates(center_x, center_y):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    x_coordinate = center_x // num2
    y_coordinate = center_y // num1
    return x_coordinate, y_coordinate
class Board:
    def __init__(self, level, screen, numberRowMatrix, numberColMatrix, player, font):
        self.level = level
        self.screen = screen
        self.colorLine = "blue"
        self.colorCircle = "white"
        self.PI = math.pi
        self.WIDTH_LINE_BOARD = 2
        self.WIDTH_SMALL_CIRCLE_BOARD = 3
        self.WIDTH_BIG_CIRCLE_BOARD = 8
        self.num1 = (HEIGHT - 50) // numberRowMatrix
        self.num2 = WIDTH // numberColMatrix
        self.player = player
        self.font = font

    
    def draw(self, flicker):
        for i in range(len(self.level)):
            for j in range(len(self.level[i])):
                x, y = j * self.num2, i * self.num1
                cx, cy = x + 0.5 * self.num2, y + 0.5 * self.num1
                if self.level[i][j] == 1:
                        pygame.draw.circle(self.screen, self.colorCircle, (cx, cy), self.WIDTH_SMALL_CIRCLE_BOARD)
                elif self.level[i][j] == 2 and not flicker:
                        pygame.draw.circle(self.screen, self.colorCircle, (cx, cy), self.WIDTH_BIG_CIRCLE_BOARD)
                elif self.level[i][j] == 3:
                        pygame.draw.line(self.screen, self.colorLine, (cx, y), (cx, y + self.num1), self.WIDTH_LINE_BOARD)
                elif self.level[i][j] == 4:
                        pygame.draw.line(self.screen, self.colorLine, (x, cy), (x + self.num2, cy), self.WIDTH_LINE_BOARD)
                elif self.level[i][j] == 5:
                        pygame.draw.arc(self.screen, self.colorLine, [(x - 0.4 * self.num2) - 2, y + 0.5 * self.num1, self.num2, self.num1], 0, self.PI / 2, self.WIDTH_LINE_BOARD)
                elif self.level[i][j] == 6:
                        pygame.draw.arc(self.screen, self.colorLine, [(x + 0.5 * self.num2), y + 0.5 * self.num1, self.num2, self.num1], self.PI / 2, self.PI, self.WIDTH_LINE_BOARD)
                elif self.level[i][j] == 7:
                        pygame.draw.arc(self.screen, self.colorLine, [(x + 0.5 * self.num2), y - 0.4 * self.num1, self.num2, self.num1], self.PI, 3 * self.PI / 2, self.WIDTH_LINE_BOARD)
                elif self.level[i][j] == 8:
                        pygame.draw.arc(self.screen, self.colorLine, [(x - 0.4 * self.num2) - 2, y - 0.4 * self.num1, self.num2, self.num1], 3 * self.PI / 2, 2 * self.PI, self.WIDTH_LINE_BOARD)
                elif self.level[i][j] == 9:
                        pygame.draw.line(self.screen, self.colorCircle, (x, cy), (x + self.num2, cy), self.WIDTH_LINE_BOARD)
    
    def draw_misc(self):
        score_text = self.font.render(f'Score: {self.player.score}', True, 'white')
        self.screen.blit(score_text, (10, HEIGHT - 30))
        
        # Hiển thị trạng thái power-up nếu có trạng thái power-up thì hiển thị một hình tròn màu xanh
        if self.player.power_up:
            pygame.draw.circle(self.screen, 'blue', (200, HEIGHT - 20), 10)

        
        # Hiển thị mạng còn sống của player
        for i in range(self.player.lives):
            self.screen.blit(pygame.transform.scale(self.player.images[0], (25, 25)), (400 + (i * 40), HEIGHT - 40))
        

class Player: 
    def __init__(self, x, y, screen, images, numberRowMatrix, numberColMatrix):
        self.x = x
        self.y = y
        self.direction = 0
        self.direction_command = 0
        self.counter = 0
        self.speed = 2
        self.score = 0
        self.screen = screen
        self.images = images
        self.width = WIDTH_PLAYER
        self.height = HEIGHT_PLAYER
        self.numberRowMatrix = numberRowMatrix 
        self.numberColMatrix = numberColMatrix
        self.turns_allowed = [False, False, False, False]
        self.level = boards
        self.power_up = False
        self.power_counter = 0
        self.eaten_ghost = [False, False, False, False]
        self.lives = NUMBER_LIVES
        self.moving = False
        self.startup_counter = 0
        

    def setPosition(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self):
    # 0-RIGHT, 1-LEFT, 2-UP, 3-DOWN
        if self.direction == RIGHT:
           self.screen.blit(self.images[self.counter // 5], (self.x, self.y))
        elif self.direction == LEFT:
           self.screen.blit(pygame.transform.flip(self.images[self.counter // 5], True, False), (self.x, self.y))
        elif self.direction == UP:
           self.screen.blit(pygame.transform.rotate(self.images[self.counter // 5], 90), (self.x, self.y))
        elif self.direction == DOWN:
            self.screen.blit(pygame.transform.rotate(self.images[self.counter // 5], 270), (self.x, self.y))
    
    def get_center(self):
        return self.x + self.width // 2, self.y + self.height // 2
    
    def check_collision(self):
        num1 = (HEIGHT - 50) // 32
        num2 = WIDTH // 30
        center_x, center_y = self.get_center()
        if 0 < self.x < WIDTH - 30:
            # Nếu ăn thức ăn thường thì score + 10
            if self.level[center_y // num1][center_x // num2] == 1:
                self.level[center_y // num1][center_x // num2] = 0
                self.score += 10
            
            # Nếu ăn power-up score + 50 và bật trạng thái power_up
            if self.level[center_y // num1][center_x // num2] == 2:
                self.level[center_y // num1][center_x // num2] = 0
                self.score += 50
                self.power_up = True
                self.power_counter = 0
                self.eaten_ghost = [False, False, False, False]
                

    def check_position(self, level):
        center_x, center_y = self.get_center()
        pygame.draw.circle(self.screen, "red", (center_x, center_y), 3)
        turns = [False, False, False, False]
        num1 = (HEIGHT - 50) // self.numberRowMatrix
        num2 = WIDTH // self.numberColMatrix
        num3 = min(num1, num2) // 2
        if center_x // self.numberColMatrix < self.numberColMatrix - 1:
            if self.direction == RIGHT and level[center_y // num1][(center_x - num3) // num2] < 3:
                turns[LEFT] = True
            if self.direction == LEFT and level[center_y // num1][(center_x + num3) // num2] < 3:
                turns[RIGHT] = True
            if self.direction == UP and level[(center_y + num3) // num1][center_x // num2] < 3:
                turns[DOWN] = True
            if self.direction == DOWN and level[(center_y - num3) // num1][center_x // num2] < 3:
                turns[UP] = True
            
            if self.direction in [UP, DOWN]:
                if level[(center_y + num3) // num1][center_x // num2] < 3:
                    turns[DOWN] = True
                if level[(center_y - num3) // num1][center_x // num2] < 3:
                    turns[UP] = True
                if level[center_y // num1][(center_x - num2) // num2] < 3:
                    turns[LEFT] = True
                if level[center_y // num1][(center_x + num2) // num2] < 3:
                    turns[RIGHT] = True
            if self.direction in [RIGHT, LEFT]:
                if level[(center_y + num1) // num1][center_x // num2] < 3:
                    turns[DOWN] = True
                if level[(center_y - num1) // num1][center_x // num2] < 3:
                    turns[UP] = True
                if level[center_y // num1][(center_x - num3) // num2] < 3:
                    turns[LEFT] = True
                if level[center_y // num1][(center_x + num3) // num2] < 3:
                    turns[RIGHT] = True
        else:
            turns[RIGHT] = True
            turns[LEFT] = True

        return turns
    
    def move_player(self):
        # r, l, u, d
        if self.direction == RIGHT and self.turns_allowed[RIGHT]:
            self.x += self.speed
        elif self.direction == LEFT and self.turns_allowed[LEFT]:
            self.x -= self.speed
        elif self.direction == UP and self.turns_allowed[UP]:
            self.y -= self.speed
        elif self.direction == DOWN and self.turns_allowed[DOWN]:
            self.y += self.speed
            
class Blinky: 
    def __init__(self): 
        self.x = 320 
        self.y = 250
      
        self.direction = 0
        self.image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/red.png'), (WIDTH_GHOST, HEIGHT_GHOST)) 
        self.id = ID_BLINKY
        
        
class Inky: 
    def __init__(self): 
        self.x = 260
        self.y = 250 
        self.direction = 2
        self.image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/blue.png'), (WIDTH_GHOST, HEIGHT_GHOST)) 
        self.id = ID_INKY
        
class Pinky: 
    def __init__(self): 
        self.x = 250 
        self.y = 285
        
        self.direction = 1
        self.image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/pink.png'), (WIDTH_GHOST, HEIGHT_GHOST)) 
        self.id = ID_PINKY

class Clyde: 
    def __init__(self): 
        self.x = 200 
        self.y = 220
        self.direction = 3
        self.image = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/orange.png'), (WIDTH_GHOST, HEIGHT_GHOST))
        self.id = ID_CLYDE

class Ghost:
    def __init__(self, x_coord, y_coord, img, direct, id,  screen, player):
        self.x_pos = x_coord
        self.y_pos = y_coord
        self.center_x = self.x_pos + WIDTH_GHOST // 2
        self.center_y = self.y_pos + HEIGHT_GHOST // 2
        self.speed = SPEED_GHOST
        self.img = img
        self.direction = direct
        self.dead = False
        self.in_box = False
        self.id = id
        self.screen = screen 
        self.eaten = False
        self.dead_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/dead.png'), (WIDTH_GHOST, HEIGHT_GHOST))
        self.spooked_img = pygame.transform.scale(pygame.image.load(f'assets/ghost_images/powerup.png'), (WIDTH_GHOST, HEIGHT_GHOST))
        self.turns, self.in_box = self.check_collisions()
        self.rect = self.draw(player)
        
    def draw(self, player):
        if (not player.power_up and not self.dead) or (self.eaten and player.power_up and not self.dead):
            self.screen.blit(self.img, (self.x_pos, self.y_pos))
        elif player.power_up and not self.dead and not self.eaten:
            self.screen.blit(self.spooked_img, (self.x_pos, self.y_pos))
        else:
            self.screen.blit(self.dead_img, (self.x_pos, self.y_pos))
        ghost_rect = pygame.rect.Rect((self.center_x - 18, self.center_y - 18), (36, 36))
        return ghost_rect
    def check_collisions(self): 
        self.turns = [False, False, False, False]
        self.in_box = True
        return self.turns, self.in_box
    
    def convert_coordinates(self, center_x, center_y):
        num1 = (HEIGHT - 50) // 32
        num2 = WIDTH // 30
        x_coordinate = center_x // num2
        y_coordinate = center_y // num1
        return x_coordinate, y_coordinate
    def BFS_Algorithm(self, player, level):
        center_player_x, center_player_y = player.get_center()
        player_x_coord, player_y_coord = convert_coordinates(center_player_x, center_player_y)
        ghost_x_coord, ghost_y_coord = convert_coordinates(self.center_x, self.center_y)
        
        path = bfs(level,  ghost_y_coord, ghost_x_coord, player_y_coord, player_x_coord)
        print("Player:", player_x_coord, player_y_coord)
        print("Ghost:", ghost_x_coord, ghost_y_coord)
        return path; 
    
    def move_towards_player(self, player, level):
        print("START", self.center_x, self.center_y)
        path = self.BFS_Algorithm(player, level)
        print("Path: ", path)
        ghost_x_coord, ghost_y_coord = self.convert_coordinates(self.center_x, self.center_y)
        if (path and len(path) >= 2):
            next_i, next_j = path[1]
            print("Next: ", next_j, next_i, " Ghost: ", ghost_x_coord, ghost_y_coord)
            if next_j > ghost_x_coord:
                self.center_x += self.speed
                self.direction = RIGHT
            elif next_j < ghost_x_coord:
                self.center_x -= self.speed
                self.direction = LEFT
            elif next_i > ghost_y_coord:
                self.center_y += self.speed
                self.direction = DOWN
                print("MOve", next_i, ghost_y_coord, self.center_y)
            elif next_i < ghost_y_coord:
                self.center_y -= self.speed
                self.direction = UP
        elif (path and len(path) == 1 and not (player.x - 2 < self.center_x < player.x + 2) and (player.y - 2 < self.center_y < player.y + 2)):
            if (self.direction == RIGHT):
                self.center_x += self.speed
            elif (self.direction == LEFT):
                self.center_y -= self.speed
            elif (self.direction == UP):
                self.center_y -= self.speed
            else: 
                self.center_y += self.speed
        self.x_pos = self.center_x - WIDTH_GHOST // 2
        self.y_pos = self.center_y - HEIGHT_GHOST // 2
        x_coord, y_coord = self.convert_coordinates(self.center_x, self.center_y)
        print("Ghost toa do: ", self.center_x, self.center_y)
        

                    

class Game:
    def __init__(self, numberRowMatrix, numberColMatrix, player_x, player_y):
        pygame.init()
        self.screen = pygame.display.set_mode([WIDTH, HEIGHT])
        self.clock = pygame.time.Clock()
        self.timer = pygame.time.Clock()
        self.font = pygame.font.Font('freesansbold.ttf', 20)
        self.running = True
        self.player_images = []
        self.numberRowMatrix = numberRowMatrix
        self.numberColMatrix = numberColMatrix
        self.flicker = False

        for i in range(1, 5):
            self.player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (WIDTH_PLAYER, HEIGHT_PLAYER)))

        self.player = Player(player_x, player_y, self.screen, self.player_images, self.numberRowMatrix, self.numberColMatrix)
        self.board = Board(boards, self.screen, self.numberRowMatrix, self.numberColMatrix, self.player, self.font)
        self.blinkyInformation = Blinky()
        self.inkyInformation = Inky()
        self.pinkyInformation = Pinky()
        self.clydeInformation = Clyde()
        self.blinky = Ghost(self.blinkyInformation.x, self.blinkyInformation.y, self.blinkyInformation.image, self.blinkyInformation.direction, self.blinkyInformation.id, self.screen, self.player)
        self.inky = Ghost(self.inkyInformation.x, self.inkyInformation.y, self.inkyInformation.image, self.inkyInformation.direction, self.inkyInformation.id, self.screen, self.player)
        self.pinky = Ghost(self.pinkyInformation.x, self.pinkyInformation.y, self.pinkyInformation.image, self.pinkyInformation.direction, self.pinkyInformation.id, self.screen, self.player)
        self.clyde = Ghost(self.clydeInformation.x, self.clydeInformation.y, self.clydeInformation.image, self.clydeInformation.direction, self.clydeInformation.id, self.screen, self.player)

       
        # def __init__(self, x_coord, y_coord, target, speed, img, direct, dead, box, id,  screen, player):
        
    def run(self):
        while self.running:
            self.timer.tick(FPS)
            if self.player.counter < 19:
                self.player.counter += 1
                if self.player.counter > 5: 
                    self.flicker = False
            else:
                self.player.counter = 0
                self.flicker = True
                
            
            # Xử lí trạng thái power-up. Nếu ăn thì duy trì trong 10s 
            if self.player.power_up and self.player.power_counter < TIME_POWER_UP * FPS:
                self.player.power_counter += 1
            elif self.player.power_up and self.player.power_counter >= TIME_POWER_UP * FPS:
                self.player.power_up = False
                self.player.power_counter = 0
                self.player.eaten_ghost = [False, False, False, False]
                
            # Khóa trong 3s đầu không cho di chuyển 
            if self.player.startup_counter < 3 * FPS:
                self.player.startup_counter += 1
                self.player.moving = False
            else: 
                self.player.moving = True
                
            
            self.screen.fill("black")
            self.board.draw(self.flicker)
            self.player.draw()
            self.blinky.draw(self.player)
            self.inky.draw(self.player)
            self.pinky.draw(self.player)
            self.clyde.draw(self.player)
            
            self.player.turns_allowed = self.player.check_position(boards)
            if self.player.moving:  
                self.player.move_player()
            self.clyde.move_towards_player(self.player, boards)
            self.player.check_collision()
            self.board.draw_misc()
            self.handle_events()
            pygame.display.flip()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    self.player.direction_command = RIGHT
                if event.key == pygame.K_LEFT:
                    self.player.direction_command = LEFT
                if event.key == pygame.K_UP:
                    self.player.direction_command = UP
                if event.key == pygame.K_DOWN:
                    self.player.direction_command = DOWN
                # Chỉ cập nhật hướng di chuyển nếu hướng đó được phép

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and self.player.direction_command == RIGHT:
                    self.player.direction_command = self.player.direction
                if event.key == pygame.K_LEFT and self.player.direction_command == LEFT:
                    self.player.direction_command = self.player.direction
                if event.key == pygame.K_UP and self.player.direction_command == UP:
                    self.player.direction_command = self.player.direction
                if event.key == pygame.K_DOWN and self.player.direction_command == DOWN:
                    self.player.direction_command = self.player.direction

            if self.player.direction_command == RIGHT and self.player.turns_allowed[RIGHT]:
                self.player.direction = RIGHT
            if self.player.direction_command == LEFT and self.player.turns_allowed[LEFT]:
                self.player.direction = LEFT
            if self.player.direction_command == UP and self.player.turns_allowed[UP]:
                self.player.direction = UP
            if self.player.direction_command == DOWN and self.player.turns_allowed[DOWN]:
                 self.player.direction = DOWN

    

if __name__ == "__main__":
    player_x = 245
    player_y = 410
    numberRowMatrix = 32
    numberColMatrix = 30
    game = Game(numberRowMatrix, numberColMatrix, player_x, player_y)
    game.run()


# def DFS(arr2D, start, end):
#     if start == end:
#         return
#     if( arr2D[end[0]][end[1]] == 1):
#         return
#     path = []
#     stack =[]
#     visited = []
#     stack.append(start)
#     parent = {}
    
#     while len(stack) != 0:
#         now = stack.pop()
#         visited.append(now)
#         if now == end:
#             break
#         dir = [(-1, 0), (1, 0), (0, -1), (0, 1)]
#         for d in dir:
#              node = [now[0] + d[0], now[1] + d[1]]
#              if node[0] >= 0 and node[0] < len(arr2D) and node[1] >= 0 and node[1] < len(arr2D[0]):
#                 if node not in visited and arr2D[now[0] + d[0]][now[1] + d[1]] != 1:
#                     stack.append(node)
#                     parent[tuple(node)] = tuple(now)
    
#     path.append(end)

#     node = end
#     while node != None:
#         path.append(parent.get(tuple(node)))
#         node = parent.get(tuple(node))

#     path.pop()
#     path.reverse()
#     return path