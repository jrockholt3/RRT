import random
import math 
import pygame

class RRTMap:
    def __init__(self, start, goal, MapDims, obsDim, obsNum):
        self.start=start
        self.goal=goal
        self.MapDims=MapDims
        self.Maph, self.Mapw = self.MapDims

        # window settings
        self.MapwindowName='RRT Path Planning'
        pygame.display.set_caption(self.MapwindowName)
        self.map=pygame.display.set_mode((self.Mapw, self.Maph))
        self.map.fill((255,255,255))
        self.nodeRad=2
        self.nodeThickness=0
        self.edgeThickness=1

        self.obs=[]
        self.obsDim=obsDim
        self.obsNum=obsNum

        # colors
        self.grey = (70,70,70)
        self.Blue = (0,0,255)
        self.Green = (0,255,0)
        self.Red = (255,0,0)
        self.white = (255,255,255)

    def drawMap(self, obstacles):
        # draws start ang goal and obstacles on map display
        pygame.draw.circle(self.map, self.Green, self.start,self.nodeRad+5,0)
        pygame.draw.circle(self.map, self.Green, self.goal,self.nodeRad+20,1)
        self.drawObs(obstacles)


    def drawPath(self):
        pass

    def drawObs(self,obstacles):
        obstacleslist=obstacles.copy()
        while (len(obstacleslist)>0):
            obs_i = obstacleslist.pop(0)
            pygame.draw.rect(self.map,self.grey, obs_i)

class RRTGraph:
    def __init__(self, start, goal, MapDims, obsDim, obsNum):
        (x,y) = start
        self.start=start
        self.goal=goal
        self.goalFlag=False
        self.maph,self.mapw=MapDims
        self.x=[]
        self.y=[]
        self.parent=[]
        # initialize tree 
        self.x.append(x)
        self.y.append(y)
        self.parent.append(0)
        # obstacles
        self.obstacles=[]
        self.obsDim=obsDim
        self.obsNum=obsNum
        # path
        self.goalstate = None
        self.path=[]

    def makeRandomRect(self):
        # generate rand xy to represent upper LH corner of square obs
        uppercornerx=int(random.uniform(0,self.mapw-self.obsDim))
        uppercornery=int(random.uniform(0,self.maph-self.obsDim))
        
        return (uppercornerx,uppercornery)

    def makeobs(self):
        obs = []
        for _ in range(0,self.obsNum):
            rectang=None
            startgoalcol=True
            while startgoalcol:
                upper = self.makeRandomRect()
                rectang=pygame.Rect(upper,(self.obsDim, self.obsDim))
                if rectang.collidepoint(self.start) or rectang.collidepoint(self.goal):
                    startgoalcol=True
                else:
                    startgoalcol=False

            obs.append(rectang)
        
        self.obstacles = obs.copy()
        return obs

    def add_node(self,n,x,y):
        self.x.insert(n,x)
        self.y.insert(n,y)

    def remove_node(self,n):
        self.x.pop(n)
        self.y.pop(n)

    def add_edge(self,parent,child):
        # child is used as an index and parent is the element
        self.parent.insert(child,parent)

    def remove_edge(self,n):
        # n = indx of the child
        self.parent.pop(n)

    def number_of_nodes(self):
        return len(self.x)

    def distance(self,n1,n2):
        (x1,y1) = (self.x[n1],self.y[n1])
        (x2,y2) = (self.x[n2],self.y[n2])

        px = (float(x1) - float(x2))**2
        py = (float(y1) - float(y2))**2

        return (px+py)**(0.5)

    def sample_envir(self):
        x = int(random.uniform(0,self.mapw))
        y = int(random.uniform(0,self.maph))

        return x,y

    def nearest(self):
        pass

    def isFree(self):
        # is the node located in the "free space" or within an obstacle?
        n = self.number_of_nodes() - 1 # id of new node to be added
        (x,y) = (self.x[n],self.y[n])
        obs = self.obstacles.copy()

        while len(obs)>0:
            obs_i = obs.pop(0)
            if obs_i.collidepoint(x,y):
                self.remove_node(n)
                return False
        return True

    def crossObstacle(self,x1,y1,x2,y2):
        # check if an edage crosses any obstacles
        obs=self.obstacles.copy()
        while (len(obs)>0):
            rectang=obs.pop(0)
            for i in range(0,101):
                u=i/100
                x=x1*u + x2*(1-u)
                y=y1*u + y2*(1-u)
                if rectang.collidepoint(x,y):
                    return True
                
        else:
            return False 
        
    def connect(self,n1,n2):
        (x1,y1) = (self.x[n1],self.y[n1])
        (x2,y2) = (self.x[n2],self.y[n2])
        if self.crossObstacle(x1,y1,x2,y2):
            self.remove_node(n2)
            return False
        else:
            self.add_edge(n1,n2)
            return True 
        
    def step(self):
        pass

    def path_to_goal(self):
        pass

    def getPathCoords(self):
        pass

    def bias(self):
        pass

    def expand(self):
        pass 

    def cost(self):
        pass

