#-----------------------------------------------------------------------------
# Name:        Zombie OutCry (assignment.py)
# Purpose:     Purpose of game is to defeat the incoming zombie horde 
#              in order to protect your village and family from 
#
# Author:      Mr. Brooks
# Created:     31-May-2021
# Updated:    
#-----------------------------------------------------------------------------
#I think this project deserves a level 4 + because i met all level 3 requirements and level 4 reqs
# + added many more features to make the game better. 
#
#Features Added:
#   music sound affects for bullet, lose, win and buttons
#   detailed self made help screen with background story for game
#   Animation of player, zombie and bullet
#-----------------------------------------------------------------------------

import pygame
import ctypes
import random
from pygame import mixer

 
ctypes.windll.user32.SetProcessDPIAware()

# a list with images of zombie walking
zombWalk =[pygame.image.load("images/Walk_1.png"),pygame.image.load("images/Walk_2.png"),
           pygame.image.load("images/Walk_3.png"),pygame.image.load("images/Walk_4.png"),
           pygame.image.load("images/Walk_5.png"),pygame.image.load("images/Walk_6.png"),
           pygame.image.load("images/Walk_7.png"),pygame.image.load("images/Walk_8.png"),
           pygame.image.load("images/Walk_9.png"),pygame.image.load("images/Walk_10.png")]


class Player(): # player class
    def __init__(self):
     # Parameters
     # ----------
     # none
     
     # Returns
     #-------
     # none 
        
        self.image = pygame.image.load("images/man.png") # loads image of player
        self.rect = [34,150, 112,62] # creates rect (points from paint)
        self.pos = [100,510] # position
        self.speed = 3 #player speed 
        self.direction = "Right" # player direction
        self.move = False # player cannot move initially
        
        # image animation variables
        self.patchNumber = 0 # intial patch number
        self.numPatches = 6 # number of patches to go through
        self.FrameRate = 10 # frame rate for player animation
    
    def walk (self):
     # Parameters
     # ----------
     # none

     # Returns
     #-------
     # none
        if (self.move): # if player can move 
            if self.direction == "Right": # if moving right
                self.pos[0] += self.speed # move right on x axis
            else: # if moving left..
                self.pos[0] -= self.speed #moves left on x axis             
   
        
    def draw(self, screen): 
     # Parameters
     # ----------
     # screen : pygame screen  

     # Returns
     #-------
     # none
        tempSurface = pygame.Surface( (self.rect[2], self.rect[3]) ) #Makes a temp Surface using the width and height of the rect
        tempSurface.fill((1,255,1))             # makes black background colour for temp surface
        tempSurface.set_colorkey((1,255,1))     #Set the color black to be transparent
        tempSurface.blit(self.image, (0,0),  self.rect) # on temp surface draws image
        
        if self.direction == "Left": # if direction is left
            tempSurface = pygame.transform.flip(tempSurface,True,False) # flips horizontally but not vertically
        screen.blit(tempSurface, self.pos) # displays player
        
class Bullet(): # bullet class
    def __init__(self):
     # Parameters
     # ----------
     # none
     
     # Returns
     #-------
     # none
        self.image = pygame.image.load("images/bullet.png") #loads image of bullet
        self.rect = [0,0,23,12] # bullet rect points from paint
        self.posx = 30 # x position
        self.posy = 529 # y position
        self.speed = 10 # speed of bullet
        self.state = "Ready" # bullet state
        
    def shoot(self,screen,x,y):
     # Parameters
     # ----------
     # screen : pygame screen 
     # x : int
     # y : int
     
     # Returns
     #-------
     # none
        if self.posx >= 799  : # if x of bullet position is bigger than screensize
            self.posx = 30 # set x back to 30 
            self.state = "Ready" # sets state back to ready
        elif self.state == "Fire": # if bullet state is fire
            self.posx  += self.speed # adds speed of bullet to x positon
            tempSurface = pygame.Surface( (self.rect[2], self.rect[3]) ) #Makes a temp Surface using the width and height of the rect
            tempSurface.fill((255,255,255))             # makes white background colour for temp surface
            tempSurface.set_colorkey((255,255,255))     #Set the color white to be transparent
            tempSurface.blit(self.image, (0,0),  self.rect) # on temp surface draws image
            screen.blit(tempSurface, (x+25,y)) # displays bullet
            

    
    
        
class Zombie():  # zombie class 
    def __init__(self,xPos,yPos,speed):
     # Parameters
     # ----------
     # speed: int
     # xPos : int
     # yPos : int
     
     # Returns
     #-------
     # none
        self.rect = [0,0,131,144] # rect of image, from paint
        self.pos = [xPos,yPos] # sets y and x coords to number inputted when creating zombie
        self.speed = speed # sets speed to inputed speed
        self.move = True # zombie is moving is true
        self.moveFrame = 0 # frame of zombie to display
        
        # image animation variables
        self.frameRate = 10 # frame rate for animation
        self.frameCount = 0 # frame count
        
    def walk(self):
     # Parameters
     # ----------
     # none
     
     # Returns
     #-------
     # none
        
        if self.move == True: # if zombie is moving 
            self.image = zombWalk[self.moveFrame] # draws certain image from list depending on number that moveframe is at the time
            self.pos[0] -= self.speed # makes zombie move left by subtracting speed
            
            
    def update(self):
     # Parameters
     # ----------
     # none
     
     # Returns
     #-------
     # none
        if self.moveFrame > 8: # if moveframe is greater than 8, sets back to 0 
            self.moveFrame = 0
        elif (self.frameCount % self.frameRate == 0): # only change animation once every 10 frames
            self.moveFrame += 1 # adds 1 to move frame
            
    def draw(self, screen): 
     # Parameters
     # ----------
     # screen : pygame screen 
     
     # Returns
     #-------
     # None 
        tempSurface = pygame.Surface( (self.rect[2], self.rect[3]) ) #Makes a temp Surface using the width and height of the rect
        tempSurface.fill((255,255,255))             # makes white background colour for temp surface
        tempSurface.set_colorkey((255,255,255))     #Set the color white to be transparent
        tempSurface.blit(self.image, (0,0),  self.rect) # on temp surface draws image
        screen.blit(tempSurface, self.pos) # displays zombie 


class Background(): # background screens class
    def __init__(self, Image, xPos, yPos): 
     # Parameters
     # ----------
     # image : pygame.image 
     # xPos : int
     # yPos : int
     
     # Returns
     #-------
     # none
        self.image = Image # self image is set to whatever image inputed when creating object
        self.pos = [xPos, yPos] # self position is set to number inputed  
        
    def draw(self,screen):
     # Parameters
     # ----------
     # screen : pygame screen  
     
     # Returns
     #-------
     # none
        screen.blit(self.image, self.pos) #displays background image on screen 
    
class Buttons(): #Button class
    def __init__(self, left, top, width, height, colour):
     # Parameters
     # ----------
     # left : int
     # top : int
     # width : int
     # height : int
     # colour : int
     
     # Returns
     #-------
     # none
        self.size = [left, top, width, height] #sets self size to number of left,top,width,height inputted
        self.colour = colour # sets self colour to colour
        self.touching = False # initial touching is false (when mouse not touching button)

        self.increaseWidth = self.size[3] + 20  #new variable of increased width, height, top, left, using self size + a number
        self.increaseHeight = self.size[2] + 20
        self.increaseTop = self.size[1] - 10
        self.increaseLeft = self.size[0] - 10
        
    def collide (self):
     # Parameters
     # ----------
     # none
     
     # Returns
     #-------
     # none
        if (pygame.mouse.get_pos()[0]>= self.size[0]) and (pygame.mouse.get_pos()[0]<= self.size[0] + self.size[2]): # if mouse x is between rectangle left and width...
            if (pygame.mouse.get_pos()[1] >= self.size[1]) and (pygame.mouse.get_pos()[1] <= self.size[1] + self.size[3]): # if mouse y is between rectangle height and top...
                
                self.size[0] = self.increaseLeft # sets button size left to increasedleft size
                self.size[1] = self.increaseTop # sets button size top to increasedtop size
                
                self.size[2] = self.increaseHeight # sets button size height to increasedheight size
                self.size[3] = self.increaseWidth #sets button size width to increasedwidth size
                self.touching = True # self touching is set to true 

                             
            else: # mouse not on button 
                self.size[0] = self.increaseLeft + 10 # sets self to size back to original size ( by using self.increased value and subtracting number previously added)
                self.size[1] = self.increaseTop +10 # sets top back to original size
                
                self.size[2] = self.increaseHeight - 20 # sets height back to original size
                self.size[3] = self.increaseWidth - 20 # sets width back to original size
                self.touching = False # self touching is set to false

    def draw(self, screen):
     # Parameters
     # ----------
     # screen : pygame screen  
     
     # Returns
     #-------
     # none
        pygame.draw.rect(screen, self.colour, self.size) # draws button
        
def main():
    #-----------------------------Setup------------------------------------------------#
    pygame.init()      # Prepare the pygame module for use
    mixer.init()        # music module
    
    pygame.mixer.music.set_volume(0.2) # volume
    surfaceSize = 800   # Desired physical surface size, in pixels.
    surfaceSize2 = 600
    clock = pygame.time.Clock()  #Force frame rate to be slower
    screen = pygame.display.set_mode((surfaceSize, surfaceSize2)) # creates screen
    pygame.display.set_caption("Zombie OutCry") # sets caption of screen
    
    font = pygame.font.SysFont("Arial", 15)  #Creates a font object
    fontMid = pygame.font.SysFont("Arial", 50)  #Creates a font object
    fontGiant = pygame.font.SysFont("Arial", 70)  #Creates a font object
    frameCount = 0 # keep track of frames
    gameState = "Start" # intial game state
    
    # game screen variables
    score = 0 # player score
    isHuman = False #is human is false
    life = 3 # number of lives player has
    zombiesLeft = 20 # number of zombies left to kill to win game
    zombie = Zombie(700,425,1) # creates zombie object  from zombie class using x, y and speed assigned
    player = Player() # creates player object from Player class
    bullet = Bullet() # creates bullet object from Bullet class
    gameScreen = Background(pygame.image.load("images/gamescreen.png"),0,0) # creates gamescreen object from background class using image and position assigned
    
    #start screen variables
    startScreen = Background(pygame.image.load("images/start.jpg"),0,0) #creates startscreen object from background class using image and position assigned
    startButton = Buttons(250,250, 300, 75 ,(14,23,28)) #creates button object from Button class using, left, top, width, height and colour assigned
    helpButton = Buttons(250,450, 300, 75 ,(14,23,28))#creates button object from Button class using, left, top, width, height and colour assigned
    
    #how to play varibles
    helpScreen = Background(pygame.image.load("images/howtoplay.png"),0,0) # creates helpscreen object from background class using image and position assigned
    backButton = Buttons(250,450, 300, 75 ,(14,23,28))# creates button object from Button class using, left, top, width, height and colour assigned

    #lose screen  + win screen variables
    loseScreen  = Background(pygame.image.load("images/losescreen.jpg"),-250,-100) # creates losescreen object from background class using image and pos assigned
    winScreen = Background(pygame.image.load("images/win.jpg"), -90, -150) # creates winscreen objectfrom background class using image and position assigned
    restartButton = Buttons(250,450, 300, 75 ,(14,23,28)) # # creates button object from Button class using, left, top, width, height and colour assigned
    
    
   
    
    #-----------------------------Main Game Loop----------------------------------------#
    while True:
        #-----------------------------Event Handling-----------------------------------#
        ev = pygame.event.poll()    # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break                   # leave game loop
        elif ev.type == pygame.KEYDOWN: # if key down..
            if ev.key == pygame.K_a or ev.key == pygame.K_LEFT: # if pressing left key/a..
                player.direction = "Left" # sets player direction to left
                player.move = True # sets player movement to true
            elif ev.key == pygame.K_d or ev.key == pygame.K_RIGHT: # if pressing right key/d
                player.direction = "Right" # sets player direction to right
                player.move = True #sets player movement to true
                
            elif ev.key == pygame.K_SPACE:# if space button pressed
                if gameState == "Game": # if on game screen
                    if player.direction == "Right": # if player is looking right
                        isHuman = False # ishuman is set to false
                        bullet.state = "Fire" # bullet state changes to fire
                        if bullet.posx + player.pos[0] == player.pos[0] + 30:#if bulletx + playerx is = to starting pos of bullet(hidden behind gun, which is player pos + 30)...
                            mixer.music.load("images/gunshot.wav") # loads gun shot sound affect
                            pygame.mixer.music.play(0) # plays gunshot sound affect
                    else:
                        isHuman = True # ishuman is set to true
                
        elif ev.type == pygame.MOUSEBUTTONUP: #if mouse buttonup
            # startscreen buttons collision
            if gameState == "Start": # if on start screen...
                if startButton.touching == True:# if mouse clicked while on rectangle...
                    gameState = "Game" # sets gamestate to game
                    mixer.music.load("images/button.wav") # loads button click
                    pygame.mixer.music.play(0) # plays button click
                 
                elif helpButton.touching == True:# if mouse clicked while on rectangle...
                    gameState = "Help" # sets gamestate to help
                    mixer.music.load("images/button.wav") # loads button click
                    pygame.mixer.music.play(0) # plays button click
                    
            #helpscreen button collision
            elif gameState == "Help": #if on help screen
                if backButton.touching == True: #if mouse clicked on rectangle
                    gameState = "Start" # sets gamestate to start
                    mixer.music.load("images/button.wav") # loads button click
                    pygame.mixer.music.play(0) # plays button click
                    
            #lose/win screen button collison
            elif gameState == "Lose" or gameState == "Win": # if on win or lose screen..
                if restartButton.touching == True:# if mouse clicked on rectangle
                    gameState = "Start" # sets gamestate to start screen
                    mixer.music.load("images/button.wav") # loads button click
                    pygame.mixer.music.play(0) # plays button click
                    
        elif ev.type == pygame.KEYUP: # if key up...
            player.move = False # sets player movement to false
                
        
        if gameState == "Start": # if gamestate is start...
            file = open("scoresaved.txt", "r") # opens saved score file 
            oldScore = file.readline() # reads line
            file.close() # closes file
            
            # resets zombies and lives, player pos, score
            score = 0 
            player.pos[0] = 100
            zombiesLeft = 20
            life = 3
        #----------------------collision----------------------------#
            startButton.collide()# runs collide method from buttonclass for startbutton
            helpButton.collide() # runs collide method from buttonclass for helpbutton
        #----------------------drawing----------------------------#
            startScreen.draw(screen) # runs draw method from background class for startscreen
            startButton.draw(screen) # runs draw method from buttonclass for startbutton
            helpButton.draw(screen)  # runs draw method from buttonclass for helpbutton
            screen.blit(fontGiant.render(('Zombie Outcry'), 1, pygame.Color(108,16,16)), (180,110)) # displays text on specific pos
            screen.blit(fontMid.render(('Start'), 1, pygame.Color(108,16,16)), (350, 260)) # displays text on specific pos
            screen.blit(fontMid.render(('Help'), 1, pygame.Color(108,16,16)), (355, 460)) # displays text on specific pos
            screen.blit(fontGiant.render((f'last score : {oldScore}'), 1, pygame.Color(108,16,16)),(200,345)) # displays text on specific pos 
        
        
        elif gameState == "Help": # if gamestate is help...
        #----------------------collision----------------------------#
            backButton.collide()# runs collide method from buttonclass for backbutton
        #----------------------drawing----------------------------#    
            helpScreen.draw(screen) # runs draw method from background class for helpscreen 
            backButton.draw(screen) # runs draw method from buttonclass for backbutton
            screen.blit(fontMid.render(('Back'), 1, pygame.Color(108,16,16)), (355, 460)) # displays text on specific coords

        
            
        elif gameState == "Game":  # if gamestate is game...  
        #----------------------Game Logic Goes After Here----------------------------#           
            if player.move == True: # if player can move           
                if (frameCount % player.FrameRate == 0):    #Only change the animation frame once every 10 frames
                    if (player.patchNumber < player.numPatches-1) :
                        player.patchNumber += 1
                        player.rect[0] += player.rect[2]  #Shifts the "display window" to the right along the man.png sheet by the width of the image
                    else:
                        player.patchNumber = 0           #Reset back to first patch
                        player.rect[0] -= player.rect[2]*(player.numPatches-1)  #Reset the rect position of the rect back too
            elif player.move == False:# if player cannot move, set to patch 4 so it looks like man is standing straight
                player.patchNumber = 4
                player.rect =[448,150, 112,62] 
                
            
            if life == 0: #if no lives left
                gameState = "Lose" # switches to lose screen
                mixer.music.load("images/lose.wav") # loads lose music
                pygame.mixer.music.play(0) # plays lose music
                
            elif zombiesLeft == 0: # if no zombies left
                gameState = "Win" # sets gamestate to win
                mixer.music.load("images/win.wav") # loads win music
                pygame.mixer.music.play(0) # plays win music 
                
        #----------------------Game collision----------------------------#
            # zombie collison 
            if player.pos[0] + bullet.posx >= zombie.pos[0]: # if bullet x is equal/greater than zombie x... (if bullet hits zombie)
                bullet.state = "Ready" #sets bullet to idle ready state
                bullet.posx = 30 # resets bullet position x
                zombiesLeft -= 1 # subtracts 1 each time player shoots a zombie
                score +=30 # adds 30 to score
                zombie.pos[0] = (random.randint(800,810)) # makes zombie have random x position
                zombie.speed = (random.randint(1,11)) # gives zombie random speed
                
            elif player.pos[0] + 40 >= zombie.pos[0]: # if player x is equal to zombie x... if zombie touches player
                life -=1 #lose one life
                score -=100 # subtracts 100 from score
                zombie.pos[0] = (random.randint(800,810)) # makes zombie have random x position
                zombie.speed = (random.randint(1,11)) # gives zombie random speed  
            
            # screen collison    
            elif player.pos[0] >= 694: # if player x pos greater than screen size
                player.pos[0] = 694 # sets positon to edge of screen so player cant move past screen
                 
            elif player.pos[0] <= 1: # if player x pos smaller than screen size
                player.pos[0] = 1 # sets positon to edge of screen so player cant move past screen
                              
        #----------------------Draw all the images----------------------------#
            gameScreen.draw(screen) # runs draw method from background class for gameScreen
            
            #For Player Object
            bullet.shoot(screen,player.pos[0] + bullet.posx,bullet.posy) # runs shoot method from bullet class
            player.draw(screen) # runs draw methond from playerclass
            player.walk() # runs walk method from player class
            
            #For Zombie Object
            zombie.walk() # runs walk method from zombieclass
            zombie.update() # runs update method from zombieclass
            zombie.draw(screen) # runs draw method from zombieclass
            
            # Text for game screen
            remaining = font.render((f'zombies left : {zombiesLeft}'), 1, pygame.Color(0,0,0)) # text & number of zombs left
            lives = font.render((f'lives left : {life}'), 1, pygame.Color(0,0,0)) # text & number of lives
            scores = font.render((f'score : {score}'), 1, pygame.Color(0,0,0)) # text & score
            screen.blit(remaining, (80,110)) # displays it on specific pos
            screen.blit(lives, (100,140)) # displays it on specific pos
            screen.blit(scores, (100, 85))# displays it on specific pos
            if isHuman == True: # if ishuman is true
                screen.blit(font.render(("Don't shoot this way! They are humans"), 1, pygame.Color(0,0,0)), (100, 450)) # displays text on specific pos

        elif gameState == "Win": # if gamestate is win...
            file = open('scoresaved.txt', 'w') # opens saved score file (and over writes it)
            file.write(f'{score}') # writes final score 
            file.close() # closes file
       #----------------------collision----------------------------#
            restartButton.collide()# runs collide method from button class for restartButton
       #----------------------Draw all the images----------------------------#     
            winScreen.draw(screen) # runs draw method from background class for winscreen
            restartButton.draw(screen) # runs draw method from button class for restartbutton
            screen.blit(fontMid.render(('Play Again'), 1, pygame.Color(108,16,16)), (290, 460)) # displays text on specific pos
       
            
        elif gameState == "Lose":# if gamestate is lose...
            
            file = open('scoresaved.txt', 'w') # opens saved score file (and over writes it)
            file.write(f'{score}') # writes final score 
            file.close() # closes file
       #----------------------collision----------------------------#     
            restartButton.collide()#runs collide method from buttonclass for restartbutton
       #----------------------Draw all the images----------------------------#                 
            loseScreen.draw(screen) # runs draw method from backgroundclass for losescreen
            restartButton.draw(screen) # runs draw method from buttonclass for restartbutton 
            screen.blit(fontMid.render(('Play Again'), 1, pygame.Color(108,16,16)), (290, 460)) # displays text on specific coords

        pygame.display.flip() 
        
        zombie.frameCount += 1 #adds one every tick 
        frameCount += 1 # adds one every tick
        clock.tick(60) #Force frame rate to be slower

    pygame.quit()     # Once we leave the loop, close the window.

main()
