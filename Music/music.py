import pygame
import threading
import time
class Music:
    def __init__(self):
        pygame.mixer.init()
        self.stop_flag = True
        self.sound = None
        self.music_thread = None
    def musicStartGame(self):
        pygame.mixer.music.load("assets/Music/pacman_beginning.wav")
        pygame.mixer.music.play()
    def musicPacmanChomp(self):
        pygame.mixer.music.load("assets/Music/pacman_chomp.wav")
        pygame.mixer.music.play()
        
    def musicPacmanDeath(self):
        pygame.mixer.music.load("assets/Music/pacman_death.wav")
        pygame.mixer.music.play()
    
    def musicPacmanEatGhost(self):
        pygame.mixer.Sound("assets/Music/pacman_eatghost.wav").play()
    
    def musicPacmanMove(self):
        pygame.mixer.music.load("assets/Music/pacman_move.wav")
        pygame.mixer.music.play()
    def musicThreadingLoop(self, file_music):
        self.sound = pygame.mixer.Sound(file_music).play(loops=-1)
        while not self.stop_flag:  # Kiểm tra stop_flag
            time.sleep(0.1)
        self.sound.stop()
    def musicPowerUp(self):
        self.stop_flag = False
        self.music_thread = threading.Thread(target=self.musicThreadingLoop, args=("assets/Music/pacman_powerUp.wav",), daemon=True)
        self.music_thread.start()
    def musicWin(self):
        pygame.mixer.music.load("assets/Music/win.wav")
        pygame.mixer.music.play(1)
    
    def musicLose(self):
        pygame.mixer.music.load("assets/Music/lose.wav")
        pygame.mixer.music.play(1)
    
    def stopMusicThread(self):
        self.stop_flag = True