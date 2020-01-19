import pygame
import math
import sys


# BRUH JUST GOTTA CHANGE UP PARENT ALGORITHM AND WE GUCCI!!!


pygame.init()
win = pygame.display.set_mode((802,802))
pygame.display.set_caption("Grid")
win.fill((0,0,0))

clock = pygame.time.Clock()

class square():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.px = 2 + 16*self.x
        self.py = 2 + 16*self.y
        self.avail = True
        self.colour = (255,255,255)
        self.parent = False
        self.child = False

    def drawSquare(self,erase,start,end):
        global startpos, endpos
        if erase:
            self.colour = (255,255,255)
            self.avail = True
        elif start:
            self.colour = (255,0,0)
            self.avail = True
            startpos = (self.x,self.y)
        elif end:
            self.colour = (0,255,0)
            self.avail = True
            endpos = (self.x,self.y)
        else: 
            self.colour = (0,0,0)
            self.avail = False

        pygame.draw.rect(win,self.colour,(self.px,self.py,14,14))

    def clear(self):
        self.avail = True
        self.colour = (255,255,255)
        pygame.draw.rect(win,self.colour,(self.px,self.py,14,14))


    def drawVisit(self):
        self.colour = (58, 87, 232)
        pygame.draw.rect(win,self.colour,(self.px,self.py,14,14))
        

    def drawReach(self):
        self.colour = (173, 216, 230)
        pygame.draw.rect(win,self.colour,(self.px,self.py,14,14))
        self.setCost()

    def drawPath(self):
        self.colour = (255, 244, 25)
        pygame.draw.rect(win,self.colour,(self.px,self.py,14,14))

    def setParent(self,obj):
        self.parent = obj


    def cost(self):
        return (self.g,self.h,self.f)

    def setCost(self):
        self.g = self.parent.g + distanceCost((self.x,self.y),(self.parent.x,self.parent.y))
        self.h = distanceCost((self.x,self.y),(endpos[0],endpos[1]))
        self.f = self.g + self.h

def initialize():
    global grid, start, end, erase, startpos, endpos, visit, visit_cost, reach, reach_cost
    
    grid = []
    start = False
    end = False
    erase = False
    startpos = (0,0)
    endpos = (0,0)
    visit_cost = []
    visit = []
    reach_cost = []
    reach = []

    for j in range(50):
        grid.append([])
        for i in range(50):
            spot = square(j,i)
            grid[j].append(spot)
            grid[j][i].clear()


    pygame.display.update()

def distanceCost(start,end):
    deltax = abs(start[0]-end[0])
    deltay = abs(start[1]-end[1])
    return min(deltax,deltay)*14 + 10*abs(deltax-deltay)

def minPos(x):
    
    index = []
    f = []
    for i in x:
        f.append(i[2])
    #print(f)
    minF = min(f)
    for j in range(len(f)):
        if minF == f[j]:
            index.append(j)
    minI = index[0]
    h = [x[j][1] for j in index]
    return index[h.index(min(h))]

def minParentPos(x):
    index = []
    f = []
    for i in x:
        f.append(i[2])
    #print(f)
    minF = min(f)
    for j in range(len(f)):
        if minF == f[j]:
            index.append(j)
    minI = index[0]
    h = [x[j][1] for j in index]
    return index[h.index(max(h))]

def aStar():
    c = 0
    found = False
    while True:
        clock.tick(120)
        
        x = minPos(reach_cost)
        
        visit.append(reach.pop(x))
        visit_cost.append(reach_cost.pop(x))
        current = visit[-1] 
        grid[current[0]][current[1]].drawVisit()

        if c!= 0:
            changeParent(current[0],current[1])
        c+=1

        if current == endpos:
            grid[endpos[0]][endpos[1]] = grid[current[0]][current[1]]
            found = True
            break


        for i in range(-1,2):
            for j in range(-1,2):
                if (i== 0 and j == 0):
                    continue

                elif current[0]+i>49 or current[0]+i<0 or current[1]+j>49 or current[1]+j<0:
                    continue
                
                elif not(grid[current[0]+i][current[1]+j].avail):
                    continue
                
                try:
                    if (current[0]+i,current[1]+j) in visit or (current[0]+i,current[1]+j) in reach :
                        continue
                    
                    else:
                        
                        """
                        if (current[0]+i,current[1]+j) in reach:
                            if (current[0],current[1]).g + distanceCost((current[0].x,current[1].y),(current[0].parent.x,current[1].parent.y)) <(current[0]+i,current[1]+j).g: 
                                b = reach.index((current[0].x,current[1].y))
                                reach.pop(b)
                                reach_cost.pop(b)

                            else:
                                continue
                        """
                    

                        reach.append((current[0]+i,current[1]+j))
                        grid[current[0]+i][current[1]+j].setParent(grid[current[0]][current[1]])
                        grid[current[0]+i][current[1]+j].drawReach()
                        reach_cost.append(grid[current[0]+i][current[1]+j].cost())
                         
                            
                            
                except:
                    pass
             
        pygame.display.update()

    if found:

        drawPath()

def changeParent(x,y):
    lst = []
    clst = []
    for i in range(-1,2):
        for j in range(-1,2):
            
            if (i == 0 and j == 0):
                    continue
            if (x+i,y+j) in visit:

                lst.append((x+i,y+j))
                clst.append(grid[x+i][y+j].cost())




                    

    a = minParentPos(clst)
    grid[x][y].setParent(grid[lst[a][0]][lst[a][1]])
    grid[x][y].setCost()
                    
    
    
    #pygame.draw.rect(win,(0,0,0),(grid[x][y].parent.px,grid[x][y].parent.py,14,14))  # BUG DETECTION
    
    # CHECK MY SKETCH FOR REASON FOR BUG 
 
    #pygame.draw.rect(win,(0,0,0),(grid[x][y].px,grid[x][y].py,14,14))  # BUG DETECTION
    pygame.draw.rect(win,(255,0,0),(grid[x][y].parent.px,grid[x][y].parent.py,14,14))  # BUG DECTECTION

def drawPath():
    print(grid[endpos[0]][endpos[1]].parent.x,grid[endpos[0]][endpos[1]].parent.y)
    path = []
    current = (endpos[0],endpos[1])
    while True:
        
        path.append(current)
        #pygame.draw.rect(win,(255,0,0),(grid[current[0]][current[1]].px,grid[current[0]][current[1]].parent.py,14,14))
        current = (grid[current[0]][current[1]].parent.x,grid[current[0]][current[1]].parent.y)
        #print(current)
        if (grid[current[0]][current[1]].parent.x,grid[current[0]][current[1]].parent.y) == startpos:
            break

    path.append(current) 
    for i in path[::-1]:
        clock.tick(30)
        grid[i[0]][i[1]].drawPath()


        pygame.display.update()







    
initialize()     

#MAIN LOOP
while True:

    clock.tick(120)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
             pygame.quit()
             sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_c]:
        initialize()
        pygame.time.delay(200)
        
    elif keys[pygame.K_s]:
        grid[startpos[0]][startpos[1]].clear()
        start = True
        end = False
        pygame.time.delay(200)
        
    elif keys[pygame.K_e]:
        grid[endpos[0]][endpos[1]].clear()
        start = False
        end = True
        pygame.time.delay(200)
        
    elif keys[pygame.K_SPACE]:
        erase = True if (not(erase)) else False
        pygame.time.delay(200)
        
    elif pygame.mouse.get_pressed()[0]: 
        x_pos,y_pos = pygame.mouse.get_pos()
        x_pos,y_pos = x_pos//16,y_pos//16   
        if x_pos<=49 or x_pos>=0 or y_pos<=49 or y_pos>=0:
            grid[x_pos][y_pos].drawSquare(erase,start,end)
        if start or end:
            start, end = False, False
            pygame.time.delay(400)

    elif keys[pygame.K_l]:
        reach.append(startpos)
        grid[startpos[0]][startpos[1]].g = 0
        grid[startpos[0]][startpos[1]].h = distanceCost(startpos,(grid[startpos[0]][startpos[1]].x,grid[startpos[0]][startpos[1]].y))
        grid[startpos[0]][startpos[1]].f = grid[startpos[0]][startpos[1]].g + grid[startpos[0]][startpos[1]].h
        
        reach_cost.append(grid[startpos[0]][startpos[1]].cost())
        aStar()
        

    
        
            
    pygame.display.update()   

