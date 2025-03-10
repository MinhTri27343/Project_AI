import pygame
from const import *
from board import boards 
from EndGame.EndGameScreen import EndGameScreen
from Algorithm.BFS import BFS
from Leaderboard.LeaderBoard import LeaderBoard
import utils
class Game:
    def __init__(self, setUp, moving, ghosts, algorithms):
        self.screen = setUp.screen
        self.timer = setUp.timer
       
        self.running = True
        self.player_images = []
        self.numberRowMatrix = len(boards)
        self.numberColMatrix = len(boards[0])
        self.flicker = False
        self.moving = moving
        self.ghosts = ghosts
        self.algorithms = algorithms
        self.gameOver = False
        self.gameOverScreen = EndGameScreen("GAME OVER")
        self.win = False
        self.gameWinScreen = EndGameScreen("YOU WIN")

        for i in range(1, 5):
            self.player_images.append(pygame.transform.scale(pygame.image.load(f'assets/player_images/{i}.png'), (WIDTH_PLAYER, HEIGHT_PLAYER)))
        self.player = setUp.player
        self.board = setUp.board
        self.leaderboard = LeaderBoard(self.screen, RANK_FILE, self.player)
        
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
                
            # Khoá PACMAN     
            if self.player.startup_counter < TIME_BLOCK_PLAYER * FPS:
                self.player.startup_counter += 1
                self.player.moving = False
            else: 
                self.player.moving = True
                
            
            self.screen.fill("black")
            self.board.draw(self.flicker)
            self.player.draw()
            for ghost in self.ghosts:
                ghost.draw(self.player)
            
            self.player.turns_allowed = self.player.check_position(boards)
            if self.player.moving and self.moving:  
                self.player.move_player()
            
            
            for i in range(len(self.ghosts)):
                if (self.ghosts[i].dead == False):
                    self.ghosts[i].move_towards_end_pos(utils.getCenter(self.player.x, self.player.y, boards), boards, self.algorithms[i], self.player)
                elif (self.ghosts[i].dead == True): 
                    self.ghosts[i].move_towards_end_pos(utils.getCenter(ghost.x_inBox, ghost.y_inBox, boards), boards, BFS, self.player)
                
            self.player.check_collision()
            self.player.check_collision_no_power_up(self.ghosts)
            self.player.eat_ghost(self.ghosts)
            
            self.board.draw_misc()
            if (self.player.isGameOver() == True):
                self.gameOver = True
                self.gameOverScreen.animate_text()
                self.leaderboard.save_rank()
                self.leaderboard.show_rank()
            elif (utils.isWinGame(boards) == True):
                self.win = True
                self.gameWinScreen.animate_text()
                self.leaderboard.save_rank()
                self.leaderboard.show_rank()
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
            # Nếu game over nhấn phím bất kỳ để thoát 
            if self.gameOver or self.win:
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    self.running = False  # Nhấn phím bất kỳ để thoát
