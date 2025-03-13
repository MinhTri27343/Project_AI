import pygame
from const import *
from board import boards 
from EndGame.EndGameScreen import EndGameScreen
from Algorithm.BFS import BFS
from Menu.Menu import Menu
import utils
import time
import sys

class Game:
    def __init__(self, setUp, moving, ghosts, algorithms, idLevel):
        self.screen = setUp.screen
        self.timer = setUp.timer
        self.music = setUp.music
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
        self.music = setUp.music
        self.idLevel = idLevel
        
    def run(self):
        # print("Id", self.idLevel)
        start_game = False
        
        if (0 <= self.idLevel <= 3): 
            self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            self.timer.tick(FPS)
            if self.player.counter < 19:
                self.player.counter += 1
                if self.player.counter > 5: 
                    self.flicker = False
            else:
                self.player.counter = 0
                self.flicker = True
                
            # print ("Giá tri: ", self.player.power_up and self.player.power_counter, self.player.power_up, self.player.power_counter)
            # Xử lí trạng thái power-up. Nếu ăn thì duy trì trong 10s 
            if self.player.power_up and self.player.power_counter < TIME_POWER_UP * FPS:
                self.player.power_counter += 1
            elif self.player.power_up and self.player.power_counter >= TIME_POWER_UP * FPS:
                self.player.power_up = False
                self.music.stopMusicThread()
                self.player.power_counter = 0
                
            # Khoá PACMAN     
            if self.player.startup_counter < TIME_BLOCK_PLAYER * FPS:
                self.player.startup_counter += 1
                self.player.moving = False
            else: 
                self.player.moving = True
                
            
            self.screen.fill("black")
            self.board.draw(self.flicker) # In man hinh game pacman 
            self.player.draw() # In  nguoi  pacman
            for ghost in self.ghosts:
                ghost.draw(self.player)
            
            self.player.turns_allowed = self.player.check_position(boards)
            if self.player.moving and self.moving:  
                self.player.move_player()
            for i in range(len(self.ghosts)):
                if (self.ghosts[i].dead == False):
                    if (0 <= self.idLevel <= 3): 
                        self.ghosts[i].move_towards_end_pos_search_first_time(utils.getCenter(self.player.x, self.player.y, boards), boards, self.algorithms[i], self.player)
                    else:   
                        self.ghosts[i].move_towards_end_pos(utils.getCenter(self.player.x, self.player.y, boards), boards, self.algorithms[i], self.player)
                elif (self.ghosts[i].dead == True): 
                    if (0 <= self.idLevel <= 3):
                        self.ghosts[i].move_towards_end_pos_search_first_time(utils.getCenter(ghost.x_inBox, ghost.y_inBox, boards), boards, BFS, self.player)
                    else: 
                        self.ghosts[i].move_towards_end_pos(utils.getCenter(ghost.x_inBox, ghost.y_inBox, boards), boards, BFS, self.player)
        
            isEatBigDot = self.player.check_collision()
            if (isEatBigDot == True):
                for ghost in self.ghosts:
                    ghost.revive = False
                    ghost.eaten = True
            
            setDecreaseLives = True
            setDisplayDrawMisc = True
            if (0 <= self.idLevel <= 3):
                setDecreaseLives = False
            if (0 <= self.idLevel <= 4):
                setDisplayDrawMisc = False
            if (self.idLevel == 4): 
                self.player.lives = 1
            self.player.check_collision_no_power_up(self.ghosts, setDecreaseLives)
            self.player.eat_ghost(self.ghosts, setDecreaseLives)
            self.board.draw_misc(setDisplayDrawMisc)

            if (self.player.isGameOver() == True):
                self.music.stopMusicThread()
                self.music.musicLose()
                self.gameOverScreen.animate_text()
                self.running = False
                
            elif (utils.isWinGame(boards) == True):
                self.music.stopMusicThread()
                self.music.musicWin()
                self.gameWinScreen.animate_text()
                self.running = False
                
            self.handle_events()
            
            pygame.display.flip()
            if start_game == False:
                self.music.musicStartGame()
                self.showReady()
                time.sleep(TIMER_START_GAME)
                start_game = True

    def handle_events(self):
        if (utils.info_record != None):
                if utils.info_record.isShowRecord == True:
                    running = True
                    while running: 
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                utils.info_record.isShowRecord = False
                                self.running = False
                                running = False
                            if event.type == pygame.QUIT:
                                sys.exit()
                            
                            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
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
                          
    def showReady(self):
        ready = pygame.transform.scale(pygame.image.load(f'assets/background_images/ready.png').convert_alpha(),(100, 20))
        self.screen.blit(ready, (255, 308))
        pygame.display.update()         
        
        
        
