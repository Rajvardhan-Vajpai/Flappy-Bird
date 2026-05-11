import os
import pygame as pg
import sys,time
from bird import Bird
from pipe import Pipe
import pygame.mixer as mixer

# Initialize Pygame mixer
pg.mixer.pre_init(44100, 16, 1 ,512)
pg.init()
pg.mixer.quit()
pg.mixer.init()

ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")
HIGHSCORE_FILE = "highscore.txt"

class Game:
    def __init__(self):
        # Setting window configuration
        self.width = 600
        self.height = 768
        self.scale_factor = 1.5
        self.win = pg.display.set_mode((self.width, self.height))
        self.clock = pg.time.Clock()
        self.move_speed = 250
        
        # Initialize bird and game state
        self.bird = Bird(self.scale_factor)
        self.score = 0
        self.high_score = self.loadHighScore()
        self.is_enter_pressed = False
        self.pipes = []
        self.pipe_generate_counter = 71
        self.setUpBgAndGround()
        self.start_monitoring = False
        
        # Set window title
        pg.display.set_caption("Flappy Bird")
        
        # Set up fonts
        try:
            self.font = pg.font.Font("assets/font.ttf", 32)
            self.small_font = pg.font.Font("assets/font.ttf", 24)
        except Exception as e:
            print("Font load error:", e)
            self.font = pg.font.SysFont(None, 32)
            self.small_font = pg.font.SysFont(None, 24)

        # Create score and high score text
        self.score_text = self.font.render(f"Score: {self.score}", True, (255,255,255))
        self.score_text_rect = self.score_text.get_rect(center=(100, 50))
        self.high_score_text = self.small_font.render(f"Best: {self.high_score}", True, (255,255,255))
        self.high_score_text_rect = self.high_score_text.get_rect(center=(500, 50))
        
        # Restart button
        self.restart_text = self.font.render("Restart", True, (0,0,0))
        self.restart_text_rect = self.restart_text.get_rect(center=(300, 700))
        self.is_game_started = True
        
        # Game over image
        try:
            self.game_over_img = pg.transform.scale_by(pg.image.load("assets/gameover.jpg").convert_alpha(), self.scale_factor)
        except Exception as e:
            print("Game over image load error:", e)
            self.game_over_img = pg.Surface((200, 100))
            self.game_over_img.fill((255, 0, 0))
        self.game_over_rect = self.game_over_img.get_rect(center=(300, 400))
        
        # Load sounds
        self.flap_sound = mixer.Sound("assets/sfx/flap.wav")
        self.collision_sound = mixer.Sound("assets/sfx/dead.wav")
        self.score_sound = mixer.Sound("assets/sfx/score.wav")
        self.score_sound_countdown = 10
        self.bird_up_img = pg.image.load(os.path.join(ASSETS_PATH, "birdup.png")).convert_alpha()
        self.gameLoop()

    def loadHighScore(self):
        """Load high score from file. Returns 0 if file doesn't exist."""
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read())
        except FileNotFoundError:
            return 0
        except ValueError:
            return 0
    
    def saveHighScore(self):
        """Save high score to file."""
        try:
            with open(HIGHSCORE_FILE, "w") as f:
                f.write(str(self.high_score))
        except Exception as e:
            print(f"Error saving high score: {e}")
    
    def updateHighScore(self):
        """Update high score if current score is higher."""
        if self.score > self.high_score:
            self.high_score = self.score
            self.saveHighScore()
            self.high_score_text = self.small_font.render(f"Best: {self.high_score}", True, (255,255,255))

    
    def gameLoop(self):
        """Main game loop handling events, updates, and rendering."""
        last_time = time.time()
        while True:
            # Calculate delta time for frame-rate independent movement
            new_time = time.time()
            dt = new_time - last_time
            last_time = new_time

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type==pg.KEYDOWN and self.is_game_started:
                    if event.key==pg.K_RETURN:
                        self.is_enter_pressed=True
                        self.bird.update_on=True
                        
                    if event.key==pg.K_SPACE and self.is_enter_pressed:
                        self.bird.flap(dt)
                        self.flap_sound.play()
                if event.type==pg.KEYDOWN and not self.is_game_started:
                    if event.key==pg.K_r:
                        self.restartGame()
                if event.type==pg.MOUSEBUTTONDOWN:
                    if self.restart_text_rect.collidepoint(pg.mouse.get_pos()):
                        self.restartGame()

            self.updateEverything(dt)
            self.checkCollisions()
            self.checkScore()
            self.drawEverything()
            pg.display.update()
            self.clock.tick(60)
    def restartGame(self):
        # Check and save high score before restarting
        self.updateHighScore()
        
        self.score = 0
        self.is_game_started = True
        self.is_enter_pressed = False
        self.start_monitoring = False
        self.bird.resetPosition()
        self.pipes.clear()
        self.pipe_generate_counter = 71
        self.bird.update_on = False
        self.score_text = self.font.render(f"Score: {self.score}", True, (255,255,255))
        self.score_text_rect = self.score_text.get_rect(center=(100,50))

    def checkScore(self):
        """Check if bird has passed a pipe and update score."""
        if len(self.pipes)>0:
                if self.bird.rect.left>self.pipes[0].rect_down.left and self.bird.rect.right<self.pipes[0].rect_up.right and not self.start_monitoring:
                    self.start_monitoring=True
                if self.bird.rect.left>self.pipes[0].rect_down.right and self.start_monitoring:
                    self.start_monitoring=False
                    self.score+=1
                    self.score_text=self.font.render(f"Score: {self.score}",True,(255,255,255))
                self.bird.update_on=True
                self.score_sound_countdown-=1
                if self.score_sound_countdown <= 0 and self.is_game_started:
                    self.score_sound_countdown = 100
                    self.score_sound.play()
                

    def checkCollisions(self):
        """Check for collisions with pipes and ground."""
        if len(self.pipes):
            if self.bird.rect.bottom>568:
                self.bird.update_on=True
                self.is_enter_pressed=False
                self.is_game_started=False

            if (self.bird.rect.colliderect(self.pipes[0].rect_down) or
            self.bird.rect.colliderect(self.pipes[0].rect_up)):
                self.is_enter_pressed=False
                self.is_game_started=False

    def updateEverything(self,dt):
        """Update game state including bird, pipes, and ground movement."""
        if self.is_enter_pressed:
            # Move the ground to simulate scrolling
            self.ground1_rect.x-=int(self.move_speed*dt)
            self.ground2_rect.x-=int(self.move_speed*dt)

            if self.ground1_rect.right<0:
                self.ground1_rect.x=self.ground2_rect.right
            if self.ground2_rect.right<0:
                self.ground2_rect.x=self.ground1_rect.right

            # Generate new pipes
            if self.pipe_generate_counter>70:
                self.pipes.append(Pipe(self.scale_factor,self.move_speed))
                self.pipe_generate_counter=0
                
            self.pipe_generate_counter+=1

            # Update and remove off-screen pipes
            for pipe in self.pipes:
                pipe.update(dt)
            
            if len(self.pipes)!=0:
                if self.pipes[0].rect_up.right<0:
                    self.pipes.pop(0)
                  
        # Update bird position
        self.bird.update(dt)


    def drawEverything(self):
        # Draw background and game elements
        self.win.blit(self.bg_img,(0,-300))
        for pipe in self.pipes:
            pipe.drawPipe(self.win)
        self.win.blit(self.ground1_img,self.ground1_rect)
        self.win.blit(self.ground2_img,self.ground2_rect)
        self.win.blit(self.bird.image,self.bird.rect)
        
        # Draw score and high score
        self.win.blit(self.score_text,self.score_text_rect)
        self.win.blit(self.high_score_text,self.high_score_text_rect)
        
        # Draw game over screen if game is finished
        self.win.blit(self.game_over_img,self.game_over_rect) if not self.is_game_started else None
        if not self.is_game_started:
            self.win.blit(self.restart_text,self.restart_text_rect)
    
    
    def setUpBgAndGround(self):
        """Load and setup background and ground images."""
        # Load background image
        self.bg_img=pg.transform.scale_by(pg.image.load("assets/bg.png").convert(),self.scale_factor)
        
        # Load ground images for seamless scrolling
        self.ground1_img=pg.transform.scale_by(pg.image.load("assets/ground.png").convert(),self.scale_factor)
        self.ground2_img=pg.transform.scale_by(pg.image.load("assets/ground.png").convert(),self.scale_factor)
        
        # Setup ground rectangles
        self.ground1_rect=self.ground1_img.get_rect()
        self.ground2_rect=self.ground2_img.get_rect()
        
        self.ground1_rect.x=0
        self.ground2_rect.x=self.ground1_rect.right
        self.ground1_rect.y=568
        self.ground2_rect.y=568

game=Game()