import pygame
from random import randint as rand
from math import *
import time
import colorsys

pygame.init()

clock = pygame.time.Clock()
fps_limit = 30

white = (255,255,255)
background_colour = (0,0,0)
#info = pygame.display.Info()
#width,height = info.current_w,info.current_h
#screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
width,height = 800,800
screen = pygame.display.set_mode((width,height))
screen.fill(background_colour)

dx,dy = 10,10
balls_no = 6
squares = False

balls = [[(rand(-width/4,width/4),rand(-height/4,height/4)),  #position
          rand(20,45),  #radius
          (rand(10,35)/10*(rand(0,1)*2-1),rand(10,35)/10*(rand(0,1)*2-1)),  #velocity
          rand(0,3),  #rotation
          rand(0,10)/100 * (rand(0,1)*2-1)  #rotation speed
          ] for i in range(balls_no)]
#balls = [[(0,0),99,(5,3)] for i in range(balls_no)]
#balls = [[(60,95),50,(2,1)],[(-50,-50),50,(4,3)]]
#balls = [[(0,300),40,(3,0)],[(0,100),20,(3,0)],[(0,0),15,(3,0)],[(150,0),15,(3,0)],[(200,-75),15,(3,0)],[(200,-200),20,(3,0)],[(150,-275),20,(3,0)],[(50,-265),5,(3,0)],[(0,-275),15,(3,0)],[(-50,-250),15,(3,0)]]

def move():
    for index,ball in enumerate(balls):
        if ball[0][0] - ball[1] - 20 < -width/2:
            balls[index][2] = (ball[2][0]*-1,ball[2][1])
        elif ball[0][0] + ball[1] + 20 > width/2:
            balls[index][2] = (ball[2][0]*-1,ball[2][1])
        if ball[0][1] - ball[1] - 20 < -height/2:
            balls[index][2] = (ball[2][0],ball[2][1]*-1)
        elif ball[0][1] + ball[1] + 20 > height/2:
            balls[index][2] = (ball[2][0],ball[2][1]*-1)
            
        if squares:
            balls[index][3] += ball[4]
            
        balls[index][0] = (ball[0][0] + ball[2][0] , ball[0][1] + ball[2][1])


def draw():
    values = [[0  for i in range(floor(height/dy))] for i in range(floor(height/dy))]
    """
    max_x = round(max(ball[0][0] + ball[1] for ball in balls) +100)
    min_x = round(min(ball[0][0] - ball[1] for ball in balls) -100)
    max_y = round(max(ball[0][1] + ball[1] for ball in balls) +100)
    min_y = round(min(ball[0][1] - ball[1] for ball in balls) -100)
    pygame.draw.rect(screen,white,(min_x+width/2,min_y+width/2,max_x-min_x,max_y-min_y),1)
    print(min_x,max_x,min_y,max_y)
    #for x in range(min_x,min_x,dx):
        #for y in range(max_y,min_y,dy):
"""
    for x in range(round(-width/2),round(width/2),dx):
        for y in range(round(-width/2),round(width/2),dy):
            try:
                if not squares:
                    values[round(y/dy)][round(x/dx)] =  sum([(ball[1])/sqrt((x-ball[0][0])**2+(y-ball[0][1])**2) for ball in balls])
                else:
                    values[round(y/dy)][round(x/dx)] =  sum([(ball[1])**2/sqrt(((x-ball[0][0])*cos(ball[3])+(y-ball[0][1])*sin(ball[3]))**4 + ((x-ball[0][0])*-sin(ball[3])+(y-ball[0][1])*cos(ball[3]))**4) for ball in balls])         
            except:
                pass
    #print(len(values))
    for x in range(round(-width/2),round(width/2),dx):
        for y in range(round(-height/2),round(height/2),dy):
            #print(values)
            box = [[values[round(y/dy)][round(x/dx)],values[round(y/dy)][round(x/dx)+1]],
                   [values[round(y/dy)+1][round(x/dx)],values[round(y/dy)+1][round(x/dx)+1]]]
            #print(box)
            #print(round(y/dy),round(x/dx))
            points = []
            above = False
            below = False
            for row in box:
                for value in row:
                    if value >= 1:
                        above = True
                    if value < 1:
                        below = True
            if below and above:
                for iy,row in enumerate(box):
                    for ix,value in enumerate(row):
                        if value >= 1:
                            #examines adjacent vertexes
                            for adjacent in range(2):
                                if adjacent == 0:
                                    compare_ix , compare_iy = (ix+1)%2 , iy

                                elif adjacent == 1:
                                    compare_ix , compare_iy = ix , (iy+1)%2
                                    
                                if box[compare_iy][compare_ix] < 1:
                                    #same x, same row
                                    if ix == compare_ix:
                                        if iy > compare_iy:
                                            new_ix,new_iy,new_compare_ix,new_compare_iy = compare_ix,compare_iy,ix,iy
                                        else:
                                            new_ix,new_iy,new_compare_ix,new_compare_iy = ix,iy,compare_ix,compare_iy
                                        #print("y diff")
                                        #print(box[compare_iy][compare_ix],box[iy][ix])
                                        
                                        points.append((x + new_compare_ix*dx , y + ((1-box[new_iy][new_ix])/(box[new_compare_iy][new_compare_ix]-box[new_iy][new_ix])) * dx))
                                        #points.append((x + compare_ix*dx , y + ((1-box[compare_iy][compare_ix])/(box[iy][ix]-box[compare_iy][compare_ix])) * dy + adjacent*iy))
                                    
                                    #same y, same column
                                    if iy == compare_iy:
                                        if ix > compare_ix:
                                            new_ix,new_iy,new_compare_ix,new_compare_iy = compare_ix,compare_iy,ix,iy
                                        else:
                                            new_ix,new_iy,new_compare_ix,new_compare_iy = ix,iy,compare_ix,compare_iy
                                        #print("x diff")
                                        #print(f"offset = {adjacent+dx}")
                                        
                                        points.append((x + ((1-box[new_iy][new_ix])/(box[new_compare_iy][new_compare_ix]-box[new_iy][new_ix])) * dy, y + new_compare_iy*dy))
                                        #points.append((x + ((1-box[compare_iy][compare_ix])/(box[iy][ix]-box[compare_iy][compare_ix])) * dy + adjacent*ix , y + compare_iy*dy))

                                    #print(iy,ix,compare_iy,compare_ix)
                                    #l = [["TL","TR"],["BL","BR"]]
                                    #print(l[iy][ix],l[compare_iy][compare_ix])
                                    #print(box)
                                    #print(((1-box[iy][ix])/(box[compare_iy][compare_ix]-box[iy][ix])) * dy)
                #print(box)
                #pygame.draw.rect(screen,(20,20,20),(x+width/2,y+height/2,dx,dy),1)
                
                (r, g, b) = colorsys.hsv_to_rgb((points[0][0]+width/2 + points[0][1]+height/2)/(width+height), 1, 1)
                colour = (r*255,g*255,b*255)
                pygame.draw.line(screen, colour, (points[0][0]+width/2,points[0][1]+height/2), (points[1][0]+width/2,points[1][1]+height/2))
                
#def rotate():
    
    
    
                
print(balls)
play = False
running = True
while running:
    clock.tick(fps_limit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                play = True
                print("Play")
    while play:
        #print(balls)
        screen.fill(background_colour)
        draw()
        move()
        #for ball in balls:
        #pygame.draw.circle(screen,white,(ball[0][0]+width/2,ball[0][1]+height/2),ball[1]*2,1)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                play = False
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                play = False
                print("Pause")
            if event.type == pygame.KEYDOWN and event.key == pygame.K_s:
                pygame.image.save(screen, "meatballs.jpeg")

pygame.quit()
