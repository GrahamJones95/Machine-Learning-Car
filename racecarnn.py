import pygame
from pygame import *
from random import *
import random
import time
import os
import sys
import math
from pygame.locals import *
import Network as Net

black = (0,0,0)
white =(255,255,255)
blue = (0,0,255)
grasscolor = (147, 196, 125, 255)
roadcolor = (102, 102, 102, 255)
surfaceWidth = 972
surfaceHeight = 683
roadspeed = 8
grassspeed = 2
carlength = 50
numberrays = 3
pygame.init()
clock = pygame.time.Clock()
myfont = pygame.font.SysFont(pygame.font.get_default_font(),20)
net = Net.Network([7,5,4,2])
surface = pygame.display.set_mode((surfaceWidth,surfaceHeight))

def placeTextAt(text,loc):
    textsurface = myfont.render(text,False,(0,0,0))
    surface.blit(textsurface , loc)

def main():
    background = pygame.image.load("RacetrackTest.png")
    carimage = pygame.image.load("car2.png")
    surface.blit(background,(0,0))
    game_over = False
    y_val = 130
    x_val = 200
    speed = 0
    speedmult = 0
    steering_angle = 0
    theta = -0.25
    L = 10
    while not game_over:
        # for event in pygame.event.get():
            # if event.type == pygame.QUIT:
                # game_over = True
            # if event.type == pygame.KEYDOWN:
                # if(event.key == pygame.K_RIGHT):
                    # if steering_angle > math.pi/2:
                        # steering_angle = math.pi/2
                    # else:
                        # steering_angle = steering_angle+math.pi/12
                # elif(event.key == pygame.K_LEFT):
                    # if steering_angle < -math.pi/2:
                        # steering_angle = -math.pi/2
                    # else:
                        # steering_angle = steering_angle-math.pi/12
                # elif(event.key == pygame.K_UP):
                    # speedmult = 1
                # elif(event.key == pygame.K_DOWN):
                    # speedmult = -1
        
            # if event.type == pygame.KEYUP:
                # if(event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                    # steering_angle = 0
                # if(event.key == pygame.K_UP or event.key == pygame.K_DOWN):
                    # speedmult = 0
        theta = theta+(speed/L)*math.tan(steering_angle)
        x_val = x_val+round(speed*math.cos(theta))
        y_val = y_val+round(speed*math.sin(theta))
        
        surface.blit(background,(0,0))
        thetatodeg = -round(theta*180/3.1415)
        
        imagesurface = surface.blit(pygame.transform.rotate(carimage,thetatodeg),(x_val,y_val))
        carfrontcenter = (imagesurface.center[0]+round(carlength/2*math.cos(theta)),imagesurface.center[1]+round(carlength/2*math.sin(theta)))
        
        pygame.draw.circle(surface, white, carfrontcenter,1)
        distance = []

        for raynum in range(-numberrays,numberrays+1):
            nextgrasspoint = (carfrontcenter[0]+round(math.cos(theta)),carfrontcenter[1]+round(math.sin(theta)))
            i=0
            while(nextgrasspoint[0]<surfaceWidth and nextgrasspoint[1]<surfaceHeight and background.get_at(nextgrasspoint) != grasscolor):
                i = i+0.1
                nextgrasspoint = (round(carfrontcenter[0]+i*math.cos(theta+(raynum/numberrays)*(3.1415/2))),round(carfrontcenter[1]+i*math.sin((theta+(raynum/numberrays)*(3.1415/2)))))
            pygame.draw.circle(surface, white, nextgrasspoint,2)
            print(numberrays+raynum)
            pygame.draw.line(surface,white,carfrontcenter,nextgrasspoint,1)
            distance.append(((carfrontcenter[0]-nextgrasspoint[0])**2+(carfrontcenter[1]-nextgrasspoint[1])**2)**0.5)
            
        if(background.get_at(imagesurface.center) == grasscolor):
            speed = speedmult*1
        else:
            speed = speedmult*3
            
        
        inputs = [theta,speed,distance[0],distance[1],distance[2],distance[3],distance[4]]
        outputs = net.feedforward(inputs)    
        print(inputs)
        print(outputs)
        speedmult = outputs[0]
        steering_angle = outputs[1]
        
        
        
        #Now draw a ray to find the closest grass
        
        placeTextAt('X: {} Y: {}'.format(x_val,y_val),(40,600))
        placeTextAt('Theta: {:2.2f}'.format(theta),(40,640))
        #pygame.draw.rect(surface , white ,[x_val,y_val,20,20])
        
        #outerlines = [(40,40),(600,40),(600,300),(40,300)]
        #innerlines = [(120,120),(520,120),(520,220),(120,220)]
        #pygame.draw.lines(surface, blue,True,outerlines,5)
        #pygame.draw.lines(surface, blue,True,innerlines,5)
        pygame.display.update()
        clock.tick(50)

main()
pygame.quit()
quit()