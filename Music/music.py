import pygame
import threading
import time
import utils
class Music:
    def __init__(self):
        pygame.mixer.init()
        self.stop_flag = True
        self.sound = None
        self.music_thread = None
        self.isThreading = False
    def musicStartGame(self):
        if(utils.isMusic == True):
            pygame.mixer.music.load("assets/Music/pacman_beginning.wav")
            pygame.mixer.music.play()
    def musicPacmanChomp(self):
        if(utils.isMusic == True):
            pygame.mixer.music.load("assets/Music/pacman_chomp.wav")
            pygame.mixer.music.play()
        
    def musicPacmanDeath(self):
        if(utils.isMusic == True):
            pygame.mixer.music.load("assets/Music/pacman_death.wav")
            pygame.mixer.music.play()
    
    def musicPacmanEatGhost(self):
        if(utils.isMusic == True):
            pygame.mixer.Sound("assets/Music/pacman_eatghost.wav").play()
    
    def musicThreadingLoop(self, file_music):
        if(utils.isMusic == True and self.isThreading == False):
            self.isThreading = True
            self.sound = pygame.mixer.Sound(file_music).play(loops=-1)
            while not self.stop_flag:  # Kiểm tra stop_flag
                time.sleep(0.2)
            self.sound.stop()
    def musicPowerUp(self):
        if(utils.isMusic == True):
            self.stop_flag = False
            self.music_thread = threading.Thread(target=self.musicThreadingLoop, args=("assets/Music/pacman_powerUp.wav",), daemon=True)
            self.music_thread.start()
    def musicWin(self):
        if(utils.isMusic == True):
            pygame.mixer.music.load("assets/Music/win.wav")
            pygame.mixer.music.play(1)
    
    def musicLose(self):
        if(utils.isMusic == True):
            pygame.mixer.music.load("assets/Music/lose.wav")
            pygame.mixer.music.play(1)
        
    def stopMusicThread(self):
        self.stop_flag = True
        self.isThreading = False