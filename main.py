import pygame,sys
import numpy as np
from pygame.locals import *
import sounddevice as sd
from threading import Thread
pygame.init()

clock = pygame.time.Clock()

SCRSIZE = (800,800)
scr = pygame.display.set_mode(SCRSIZE)
pygame.display.set_caption('interactive avatar')

vol = 0

class avatar():
    def __init__(self,characterFolder):
        self.info = dict(eval(open(f'assets/characters/{characterFolder}/info.json').read()))

        if self.info['bodyImg'] == True:
            self.body = pygame.image.load(f'assets/characters/{characterFolder}/body.png').convert()
            self.body.set_colorkey((0,0,0))
            self.bodyPos = self.info['bodyPos']

        if self.info['headImg'] == True:
            self.head = pygame.image.load(f'assets/characters/{characterFolder}/head.png').convert()
            self.head.set_colorkey((0,0,0))
            self.headPos = self.info['headPos']

        if self.info['mouthImg'] == True:
            self.mouthBg = pygame.image.load(f'assets/characters/{characterFolder}/mouthBg.png')
            self.mouth = pygame.image.load(f'assets/characters/{characterFolder}/mouth2.png')
            self.mouth.set_colorkey((0,0,0))
            self.mouthPos = self.info['mouthPos']
            self.mouthMaxPos = self.info['mouthMaxPos']

        if self.info['eyesImg'] == True:
            self.eyes = pygame.image.load(f'assets/characters/{characterFolder}/eyes.png').convert()
            self.eyes.set_colorkey((0,0,0))
            self.eyesPos = self.info['eyesPos']
            
            self.shutEyes = pygame.image.load(f'assets/characters/{characterFolder}/shutEyes.png').convert()
            self.shutEyes.set_colorkey((0,0,0))
            self.shutEyesPos = [self.info['eyesPos'][0],self.info['eyesPos'][1]-self.shutEyes.get_height()]
            self.howShut = 0
            self.shutTimer = 1000

            self.shutDir = {'up':False,'down':False}
        self.Opened = 150

        self.mouthRect = pygame.Rect(375,425,200,200)
        
    def draw(self,surf):
        pygame.draw.rect(surf,(59,26,23),self.mouthRect)
        surf.blit(self.eyes,self.eyesPos)
        surf.blit(self.shutEyes,[self.shutEyesPos[0],self.shutEyesPos[1]+self.howShut])
        
        surf.blit(self.mouth,(self.mouthPos[0],self.mouthPos[1]+self.Opened))
        surf.blit(self.head,self.headPos)
        surf.blit(self.body,self.bodyPos)

        if self.shutTimer >= 1000:
            if self.shutDir == {'up':False,'down':False}:
                self.shutDir = {'up':False,'down':True}
            self.shutTimer = 0

        if self.shutDir == {'up':False,'down':False}:
            self.shutTimer += 1
        if self.shutDir['down'] == True:
            self.howShut += 1
            if self.howShut >= self.shutEyes.get_height():
                self.shutDir = {'up':True,'down':False}

        if self.shutDir['up'] == True:
            if self.howShut > 0:
                self.howShut -= 1
            else:
                self.shutDir = {'up':False,'down':False}
                
            self.shutTimer = 0
    
            
        
        if self.Opened > self.info['mouthPos'][1] + self.info['mouthMaxPos']:
            self.Opened = self.info['mouthPos'][1] + self.info['mouthMaxPos'] - 1
        
hershey = avatar('hershey')
def get_volume(indata, frames, time, status):
    global vol
    volume_norm = np.linalg.norm(indata) * 10
    vol = int(volume_norm)
    #print(int(volume_norm))

stream = sd.InputStream(callback=get_volume)
def get_vol():
    global stream
    
    with stream:
        sd.sleep(-1 )

get_volu = Thread(target=get_vol)
get_volu.start()


radius = SCRSIZE[0]//2

center = [SCRSIZE[0]//2,SCRSIZE[1]//2]
ellipseRect = pygame.Rect(center[0]-150,center[1]+100,300,10)



while True:
    clock.tick(0)
    scr.fill((255,255,255))

    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    '''
    pygame.draw.circle(scr,(240,240,0),(SCRSIZE[0]//2,SCRSIZE[1]//2),radius)

    pygame.draw.circle(scr,(0,0,0),(SCRSIZE[0]//2-(SCRSIZE[0]//2//2),SCRSIZE[1]//2),30)
    pygame.draw.circle(scr,(0,0,0),(SCRSIZE[0]//2+(SCRSIZE[0]//2//2),SCRSIZE[1]//2),30)

    ellipseRect.height = 10+vol
    if ellipseRect.height > SCRSIZE[1]-ellipseRect.y:
        ellipseRect.height = SCRSIZE[1]-ellipseRect.y-1

    pygame.draw.ellipse(scr,(0,0,0),ellipseRect)
    '''

    hershey.Opened = vol
    hershey.draw(scr)

    pygame.display.set_caption(str(round(clock.get_fps())))

    pygame.display.update()
    
