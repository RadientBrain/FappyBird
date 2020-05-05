import random # for generating random int
import pygame
import sys # sys.exit to exit game
from pygame.locals import * # basic pygame imports

#Global variables 
FPS = 32
SCREEN_WIDTH = 289
SCREEN_HEIGHT = 511

SCREEN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
GROUND_Y = SCREEN_HEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = 'gallery/sprites/bird.png'
BACKGROUND = 'gallery/sprites/background.png'
PIPE = 'gallery/sprites/pipe.png'



def welcomeScreen():
    """
    Shows welcome screen on startup
    """
    player_x= int(SCREEN_WIDTH / 5)
    player_y= int((SCREEN_HEIGHT- GAME_SPRITES['player'].get_height()) / 2)
    message_x= int((SCREEN_WIDTH- GAME_SPRITES['message'].get_width()) / 2)
    message_y= int(SCREEN_HEIGHT * 0.13)
    base_x=0
    
    while True:
        for event in pygame.event.get():
            #if user clicks cross exit game
            if event.type == QUIT or (event.type == KEYDOWN and event.key== K_ESCAPE):
                pygame.quit()
                sys.exit()
            
            # if user presses space or up key , start game
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return
            
            else:
                SCREEN.blit(GAME_SPRITES['background'] , (0,0))
                SCREEN.blit(GAME_SPRITES['player'] , (player_x,player_y))
                SCREEN.blit(GAME_SPRITES['message'] , (message_x,message_y))
                SCREEN.blit(GAME_SPRITES['base'] , (base_x,GROUND_Y))
                pygame.display.update()

                FPSCLOCK.tick(FPS)
                

def mainGame():
    score = 0
    player_x = int(SCREEN_WIDTH/5)
    player_y = int(SCREEN_WIDTH/2)
    base_x = 0
    
    # creating random pipes to blit
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    #list of upper pipes
    upperPipes = [
        {'x': SCREEN_WIDTH + 200, 'y':newPipe1[0]['y']},
        {'x': SCREEN_WIDTH + 200 + (SCREEN_WIDTH/2), 'y':newPipe2[0]['y']},
    ]

    #list of lower pipes
    lowerPipes = [
        {'x': SCREEN_WIDTH + 200, 'y':newPipe1[1]['y']},
        {'x': SCREEN_WIDTH + 200 + (SCREEN_WIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVel_X = -4

    player_Vel_Y = -9
    player_MaxVel_Y = 10
    player_MinVel_Y = -8
    player_Acc_Y = 1

    player_Flap_Accv = -8 #velocity while flapping
    playerFlapped = False #true when bird is flapping

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or( event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if player_y > 0:
                    player_Vel_Y = player_Flap_Accv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()

        #if player crashed return true
        crashTest = isCollide(player_x,player_y,upperPipes,lowerPipes)
        if crashTest :
            return
        
        #check score
        playerMidPos = player_x + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos +4 :
                score=score+1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        if player_Vel_Y < player_MaxVel_Y and not playerFlapped:
            player_Vel_Y += player_Acc_Y
        
        if playerFlapped:
            playerFlapped = False

        player_Height = GAME_SPRITES['player'].get_height()
        player_y = player_y + min(player_Vel_Y , GROUND_Y - player_y - player_Height)
        

        #moving pipes to left
        for upperPipe , lowerPipe in zip(upperPipes,lowerPipes):
            upperPipe['x'] += pipeVel_X
            lowerPipe['x'] += pipeVel_X


        #adding new pipe when first pipe is popped
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])


        #remove pipe if it is out of screen
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)

        #blitting our sprites
        SCREEN.blit(GAME_SPRITES['background'], (0,0))
        for upperPipe , lowerPipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'],upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'],lowerPipe['y']))



        SCREEN.blit(GAME_SPRITES['base'], (base_x,GROUND_Y))
        SCREEN.blit(GAME_SPRITES['player'], (player_x,player_y))
        myDigits = [int(x) for x in list(str(score))]
        width =0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        
        Xoffset = (SCREEN_WIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREEN_HEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def isCollide(player_x,player_y,upperPipes,lowerPipes):
    if player_y >GROUND_Y - 25 or player_y <0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(player_y < pipeHeight + pipe['y'] and abs(player_x - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (player_y + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(player_x - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True      

    return False


def getRandomPipe():
    """
    generating position of the pipes(reverse and straight)
    """
    pipeHeight =  GAME_SPRITES['pipe'][0].get_height()
    offset = SCREEN_HEIGHT / 3
    y2= offset + random.randrange(0, int(SCREEN_HEIGHT - GAME_SPRITES['base'].get_height()- 1.2*offset))
    pipeX = SCREEN_WIDTH+10
    y1= pipeHeight - y2 + offset
    pipe= [
        {'x':pipeX, 'y':-y1},   #upper pipe
        {'x':pipeX, 'y':y2} #lower pipe
    ]
    return pipe




if __name__ == "__main__":
    #main function to start game
    pygame.init() # initialize all pygame modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird by Chetan Maheshwari')
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha()
    )

    GAME_SPRITES['message'] = pygame.image.load('gallery/sprites/message.png').convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load('gallery/sprites/base.png').convert_alpha()
    GAME_SPRITES['pipe'] = (
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
    pygame.image.load(PIPE).convert_alpha()
    )

    # Game sounds
    GAME_SOUNDS['die'] = pygame.mixer.Sound('gallery/audio/die.wav')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('gallery/audio/hit.wav')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('gallery/audio/point.wav')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('gallery/audio/swoosh.wav')
    GAME_SOUNDS['wing'] = pygame.mixer.Sound('gallery/audio/wing.wav')
    
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    

    while True:
        welcomeScreen() #welcome screen until button is pressed
        mainGame() #main game function


















