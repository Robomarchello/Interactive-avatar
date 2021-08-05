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
    def __init__(self):
        pass

def get_volume(indata, frames, time, status):
    global vol
    volume_norm = np.linalg.norm(indata) * 10
    vol = int(volume_norm)
    #print(int(volume_norm))

stream = sd.InputStream(callback=get_volume)
def get_vol():
    global stream
    
    with stream:
        sd.sleep(-1 * 100)

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

    pygame.draw.circle(scr,(240,240,0),(SCRSIZE[0]//2,SCRSIZE[1]//2),radius)

    pygame.draw.circle(scr,(0,0,0),(SCRSIZE[0]//2-(SCRSIZE[0]//2//2),SCRSIZE[1]//2),30)
    pygame.draw.circle(scr,(0,0,0),(SCRSIZE[0]//2+(SCRSIZE[0]//2//2),SCRSIZE[1]//2),30)

    ellipseRect.height = 10+vol
    if ellipseRect.height > SCRSIZE[1]-ellipseRect.y:
        ellipseRect.height = SCRSIZE[1]-ellipseRect.y-1

    pygame.draw.ellipse(scr,(0,0,0),ellipseRect)

    pygame.display.set_caption(str(round(clock.get_fps())))

    pygame.display.update()
    
