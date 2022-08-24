import pygame as pgm
import sys
import random

import Map

import pygame.time

#   Screen and Grid Size :
size = w , h = 400,400

Grid_Size = 40

GX = w // Grid_Size
GY = h // Grid_Size
### GX and GY must be two even numbers

LEN = GX * GY # the length of the map (number of possible positions)

#    Main Colors :

BCKG_Color = (69, 76, 87)

Apple_CLR = (255,0,0)
SNK_CLR = (190,190,190)

TXT_CLR = (4, 196, 39)

#    Snake Directions :

UP = ( 0 , 1 )
DOWN = ( 0 , -1 )
RIGHT = ( 1 , 0 )
LEFT = ( -1 , 0 )

ALL_DIR = ( UP , DOWN , RIGHT , LEFT )

HORZ = [RIGHT , LEFT] # Horizontal Directions
VER = [UP , DOWN] # Vertical Directions

class Snake :
    Length = 1
    Pos = []
    Direction = UP #Direction
    Dead = False
    LastTailPos = None # the Last Tail Position before movement
    # Used to expand the snake in the right direction
    
    LastTailDir = None # the last direction that the tail took

    Body_Padding = 2 # represents the padding we do when we draw the snake's body

    def __init__(self , Pos =  [ (GX // 2 , GY // 2)], Direction = random.choice(ALL_DIR) , Body_Padding = 2):
        self.Length = 1
        self.Pos = Pos
        self.Length = len(Pos)
        self.Direction = Direction 
        self.Body_Padding = Body_Padding

    def __len__(self):
        return self.Length

    @staticmethod
    def Draw_Piece(Pos1 : tuple | list, Pos2 : tuple | list , Pos3 : tuple | list, Body_Padding = 2 , Color : tuple = SNK_CLR) :

        DirX = Pos1[0] - Pos2[0]
        DirY = Pos1[1] - Pos2[1]
        Dir = (DirX , DirY) # the Piece's Direction
        
        if Dir == (1 , 0) : # Right
            left = Pos1[0] * Grid_Size - Body_Padding
            top = Pos1[1] * Grid_Size + Body_Padding

            pgm.draw.rect(scr,Color,pgm.Rect(left , top , Grid_Size , Grid_Size - 2 * Body_Padding))
        elif Dir == (-1 , 0) : # Left 
            left = Pos1[0] * Grid_Size + Body_Padding
            top = Pos1[1] * Grid_Size + Body_Padding

            pgm.draw.rect(scr,Color,pgm.Rect(left , top , Grid_Size , Grid_Size - 2 * Body_Padding))
        elif Dir == (0 , -1) : # Up
            left = Pos1[0] * Grid_Size + Body_Padding
            top = Pos1[1] * Grid_Size + Body_Padding

            pgm.draw.rect(scr,Color,pgm.Rect(left , top , Grid_Size - 2 * Body_Padding , Grid_Size))
        elif Dir == (0 , 1) : # Down 
            left = Pos1[0] * Grid_Size + Body_Padding
            top = Pos1[1] * Grid_Size - Body_Padding

            pgm.draw.rect(scr,Color,pgm.Rect(left , top , Grid_Size - 2 * Body_Padding , Grid_Size)) 

        if Pos3 != None : 
            DrawPos3 = True

            NDirX = Pos3[0] - Pos1[0]
            NDirY = Pos3[1] - Pos1[1]
            NDir = (NDirX , NDirY)

            if NDir == Dir : # if the Pieces have the same direction
                DrawPos3 = False

            if DrawPos3 :
                Snake.Draw_Piece(Pos3 , Pos1 , None , Body_Padding , Color) 

    def Draw(self , scr , Color : tuple = SNK_CLR):
        if len(self.Pos) == 1 :
            for i in self.Pos :
                left = i[0] * Grid_Size + self.Body_Padding
                top = i[1] * Grid_Size + self.Body_Padding

                pgm.draw.rect(scr,Color,pgm.Rect(left , top , Grid_Size - 2 * self.Body_Padding , Grid_Size - 2 * self.Body_Padding))
        else :
            for i in range(len(self.Pos) - 1) : # Drawing every piece but the tail
                Snake.Draw_Piece(self.Pos[i] , self.Pos[i + 1] , None if i == 0 else self.Pos[i - 1] ,  self.Body_Padding , Color)

            Snake.Draw_Piece(self.Pos[self.Length - 1] , self.Pos[self.Length - 2] , None , self.Body_Padding , Color) # drawing the tail

    def Move(self ,reverse = False , DontEditLT : bool = False):
        head = self.Pos[0]
        if reverse :
            p = (head[0] - self.Direction[0] , head[1] + self.Direction[1])
        else :
            p = (head[0] + self.Direction[0] , head[1] - self.Direction[1])
        self.Pos.insert(0, p )
        if not DontEditLT :
            self.LastTailPos = self.Pos.pop(len(self.Pos) - 1)
            tail = self.Pos[len(self) - 1]
            self.LastTailDir = (tail[0] - self.LastTailPos[0] , self.LastTailPos[1] - tail[1])
        else : 
            self.Pos.pop()
    def Change_Direction(self , Dir):
        Dir = tuple(Dir)
        self.Direction = Dir

    def Append(self):
        self.Pos.append(self.LastTailPos)
        self.Length += 1

    def see_if_dead(self):

        """Returns true if the Snake is in a death position """

        head = self.Pos[0]

        HX = head[0] # Head X's coordinate

        HY = head[1] # Head Y's coordinate

        if HX < 0 or HX >= GX or HY < 0 or HY >= GY or head in self.Pos[1:] :
            return True

class Apple :

    Pos = (0,0)

    scr = None # screen || surface to draw the apple on

    def __init__(self , scr , SNK : Snake , Pos : tuple = None):
        self.scr = scr

        self.Pos = Pos
        if Pos == None :
            self.Respawn(SNK)

    def Can_Eat(self , snk : Snake , Respawn = True):
        if snk.Pos[0] == self.Pos :
            snk.Append()
            if Respawn :
                self.Respawn(snk)
    def Respawn(self , snk : Snake | tuple[int]) :

        """Respawns the apple (used if the apple has been eaten)"""
        
        emp = Map.GenerateEmptiesMap(snk , self , GX , GY ) # getting all the empty spaces
        #just to make sure the apple doesn't spawn in the same place or in teh Snake's body

        if len(emp) > 0 :
            self.Pos = random.choice(emp) #Randomizing the postion of teh apple

    def Draw(self):

        """Draws the Apple on the Screen"""

        left = self.Pos[0] * Grid_Size
        top = self.Pos[1] * Grid_Size

        pygame.draw.rect(self.scr , Apple_CLR , pygame.Rect( left , top , Grid_Size , Grid_Size ) ,border_radius=8)

def MovePoint(Point : tuple[int,int] , Dir : tuple[int, int] , reverse = False) : 
    return ((Point[0] - Dir[0] , Point[1] + Dir[1]) if reverse else (Point[0] + Dir[0] , Point[1] - Dir[1]))

def IsAPossibleDir (snk : Snake,Dir : tuple , reverse = False) : 
    
    # Tests if a Direction is Safe to Follow
    
    head = snk.Pos[0]
    
    head = MovePoint(head,Dir,reverse)
    
    return (not head in snk.Pos) and Map.InsideBorders(head[0],head[1],GX,GY)

def CanContinueHamiltonianCycle(snk : Snake , HamiltonianCycle : list, Gx : int = GX , Gy : int = GY) : 
    test1 = True
    test2 = True
    
    reversehc = False
    
    l = len(snk)
    
    Len = Gx * Gy
    
    Mp = [None] * Len
    
    for i in range(l) : 
        piece = snk.Pos[l - i - 1] # a piece of the snake body at a specific index
        index = piece[1] * Gx + piece[0] # the index of the piece
        Mp[index] = i + 1   
    
    s = (HamiltonianCycle.index(snk.Pos[0]) + 1) % (len(HamiltonianCycle) - 1) # the tail index when the snake follows the HamiltonianCycle
    saveds = s
    e = (s + l - 1) % (len(HamiltonianCycle) - 1) # the head index when the snake follows the HamiltonianCycle
    
    i = 1
    
    while s != e :# tests the HamiltonianCycle in it's Normal Direction
        piece = HamiltonianCycle[s]
        index = piece[1] * Gx + piece[0]
        if Mp[index] != None and i <= Mp[index] : 
            test1 = False
            break
        s = (s+1) % (len(HamiltonianCycle) - 1)
        i += 1

    if not test1 :
        reversehc = True
        
        s = (saveds - 1) % (len(HamiltonianCycle) - 1)
        s = s if s > 0 else len(HamiltonianCycle) - 1 + s
        e = (s - l + 1) % (len(HamiltonianCycle) - 1)
        e = e if e > 0 else len(HamiltonianCycle) - 1 + e
        
        i = 0
        
        while e != s :# tests the HamiltonianCycle in it's Reversed Direction
            piece = HamiltonianCycle[e]
            index = piece[1] * Gx + piece[0]
            if Mp[index] != None and l - i <= Mp[index] : 
                test2 = False
                break
            e = (e+1) % (len(HamiltonianCycle) - 1)
            i += 1
    
    return test1 or test2 , reversehc

def IsAPossiblePath(path : list , snk : Snake , apl : Apple , HamiltonianCycle : list):
    
    RPOS = snk.Pos.copy() # The Snake's old Positions before movement

    RDir = snk.Direction # The Snake's old direction before movement
    
    for j in range(len(path)) :
        snk.Change_Direction(path[j])
        snk.Move()

    apl.Can_Eat(snk,False)
    
    test , reversehc = CanContinueHamiltonianCycle(snk,HamiltonianCycle)
    
    snk.Pos = RPOS
    snk.Direction = RDir
    snk.Length = len(RPOS)
    return test , reversehc

def ChooseBestSkip(snk : Snake , HamiltonianCycle : list) :
    head = snk.Pos[0]
    
    hi = HamiltonianCycle.index(head)
    
    l = len(HamiltonianCycle)
    
    BestDir = None
    
    less = False
    
    for dir in ALL_DIR :
        if IsAPossibleDir(snk , dir) :
            Nhead = MovePoint(head,dir)# new head position following that direction
            if  HamiltonianCycle.index(Nhead) + (l if dir == snk.Direction else 0) > hi: 
                less = False
                BestDir = dir
                hi = HamiltonianCycle.index(Nhead) + (l if dir == snk.Direction else 0)
            elif (BestDir == None or less == True) and dir == snk.Direction :
                less = False
                BestDir = dir
                hi = HamiltonianCycle.index(Nhead)
            elif BestDir == None :
                less = True
                BestDir = dir
                hi = HamiltonianCycle.index(Nhead)
    
    return BestDir

def MapTour (snk : Snake, apl : Apple, HamiltonianCycle : list , HamiltonianPath : list , limit : int , ForbiddenPos : list) : 
    
    l = 0
    path = []
    TailPath = []
    
    RPos = snk.Pos.copy()
    RDir = snk.Direction
    
    reversehc = False
    
    AteTheApple = False # represents if the snake ate an apple while Taking the tour or not
    StepsAfterLunch = 0 # the number of steps the snake took after eating an apple
    
    while l < limit :
        dir = ChooseBestSkip(snk,HamiltonianCycle)
        if snk.Pos[0] in ForbiddenPos :# used to remove loops
            snk.Pos = RPos
            snk.Direction = RDir
            snk.Length = len(RPos)
            return [] , reversehc
        if dir != None :
            path.append(dir) 
            snk.Change_Direction(dir)
            snk.Move()
            TailPath.append(snk.LastTailDir)
            if AteTheApple :
                StepsAfterLunch += 1
            if snk.Pos[0] == apl.Pos and not AteTheApple : 
                snk.Append()
                AteTheApple = True
        else :
            break
        l += 1
    while len(path) > 0 :
        if AteTheApple and StepsAfterLunch > 0 :
            StepsAfterLunch -= 1
        elif AteTheApple :
            snk.Pos.pop()
            snk.Length = len(snk.Pos)
            AteTheApple = False
        c , reversehc = CanContinueHamiltonianCycle(snk,HamiltonianCycle)
        if c :      
            break
        dir = TailPath.pop()
        snk.Pos.reverse()
        snk.Change_Direction(dir)
        snk.Move(True,True)
        path.pop()
        snk.Pos.reverse()
    snk.Pos = RPos
    snk.Direction = RDir
    snk.Length = len(RPos)
    
    return path , reversehc

def ShowScore(scr , Color = TXT_CLR) :
    global score
    
    font = pgm.font.SysFont("Verdana", 15, True)# font for displaying score
    scoretxt = font.render(str(score),False,Color)
    scr.blit(scoretxt,(0,0)) # showing the score

Win = False

def Start () :
    global score
    score = 1

    pgm.init()

    global scr
    scr = pgm.display.set_mode(size) # the main game surface

    global Win
    Win = False # represents if the snake won the Game or Not

    C = pygame.time.Clock()
    
    global snk
    snk = Snake(Body_Padding=1)

    global apl
    apl = Apple(scr , snk)

    FollowPath = False # specifies that the Snake will follow another path rather than following the hamiltonian cycle
    
    path = [] # a path that breaks the hamiltonian cycle and skips some steps

    Mp = Map.GenerateMap(GX // 2 , GY // 2) #Generating a Map of half the length and the width

    G = Map.GenerateMapGraph(Mp)# Converting that Map into a Graph

    G = Map.PrimsAlgorithm(G,0)

    Maze = Map.GenerateHamiltonianMaze(G , Mp , GX , GY)

    HPos , HPath = Map.Maze2Cycle(Maze , GX , GY)
    
    global ReverseCycle
    ReverseCycle = False # represents that we will reverse the hamiltonian cycle direction
    
    r = False 
    
    MoveIndex = HPos.index(snk.Pos[0]) # the step index in the Hamiltonian Cycle path
    
    LoopDetector = [] # used to detect looping points
    ForbiddenPos = [] # used to break the loops
    
    SkippingPath = [] # the path used to skip the hamiltonian Cycle 
    skip = True # the snake will only follow the HamiltonianCycle if skip is False
    
    while True :
        scr.fill(BCKG_Color) # filling the whole screen so we reset it
        
        C.tick(70) # fixes the frame rate of the Game
        
        try :
            if not FollowPath : # trys to find a path to the apple
                Mp = Map.GenerateEmptiesMap(snk,apl,GX,GY , ExceptHead = True , Exceptapl = True)
                path = Map.AStarPathFinding(Mp,Mp.index(snk.Pos[0]),Mp.index(apl.Pos),LEN//6)
        except : # no such path exists
            path = None

        if path != None and not FollowPath and skip :
            c , r = IsAPossiblePath(path,snk,apl,HPos) # tests if the path is safe
            if c : # the path is safe
                FollowPath = True
                SkippingPath = []
                ReverseCycle = r
                LoopDetector = []
                ForbiddenPos = []
            else : # the path is not safe
                r = None
        if not FollowPath :
            skipdir = None # the current direction in the tour
            
            if len(SkippingPath) == 0 and skip :
                if snk.Pos[0] in LoopDetector :
                    ForbiddenPos.append(snk.Pos[0])
                SkippingPath , r= MapTour(snk,apl,HPos,HPath,(GX+GY) * 2 , ForbiddenPos) # trys to find a tour path around the map
                if len(SkippingPath) > 0:
                    LoopDetector.append(snk.Pos[0])
            if len(SkippingPath) > 0 :
                if r != None :
                    ReverseCycle = r
                skipdir = SkippingPath.pop(0)
            
            if skipdir != None :
                snk.Change_Direction(skipdir)
                snk.Move()
                if snk.Pos[0] in LoopDetector :
                    ForbiddenPos.append(snk.Pos[0])
            else :
                if ReverseCycle :
                    snk.Change_Direction(HPath[MoveIndex-1])
                else :
                    snk.Change_Direction(HPath[MoveIndex])
                snk.Move(ReverseCycle)        
            MoveIndex = HPos.index(snk.Pos[0])# going to the next step in the path
            
        if FollowPath : # the snake is following a path to the apple
            snk.Change_Direction(path.pop(0))
            snk.Move()
        if FollowPath and len(path) == 0 : # got to the end of the path
            FollowPath = False
            MoveIndex = HPos.index(snk.Pos[0])
        
        snk.Draw(scr) # drawing the Snake on the screen
        
        apl.Can_Eat(snk)# Appends the Snake if he ate the apple and respawn it
        
        if len(snk) >= (LEN /100) * 65 and skip :
            skip = False
        
        score = len(snk)
        ShowScore(scr) # shows the score
        
        if len(snk) == LEN : # he won the Game
            Win = True 
            break
        else :
            apl.Draw() # Drawing the apple on the screen

        if snk.see_if_dead() : # sees if snake is in a death position
            break
        
        pgm.display.flip()

        for ev in pygame.event.get() :
            if  ev.type == pgm.QUIT :
                pgm.quit()
                sys.exit()

def Game_Over() :
    clock = pgm.time.Clock()

    font = pgm.font.SysFont("Verdana" , 30 , True)
    text = font.render("GameOver . . ." , False , TXT_CLR)
    
    TW = text.get_width() #text width

    global scr

    global snk
    snk.Draw(scr)
    
    scr.blit(text , ( (w - TW) // 2 ,0))

    ShowScore(scr) # shows the score

    pgm.display.flip()

    loop = True

    while loop :

        clock.tick(10)

        for ev in pgm.event.get() :
            if ev.type == pgm.QUIT :
                pgm.quit()
                sys.exit()
            if ev.type == pgm.KEYDOWN and ev.key == pgm.K_r :
                pgm.quit()
                loop = False # breaks to repeat the games loop ( see the last 3 lines )
                break

def Game_Win() :
    clock = pgm.time.Clock()

    font = pgm.font.SysFont("Verdana" , 30 , True)
    text = font.render("You Win ! . ." , False , TXT_CLR)

    TW = text.get_width() #text width
    TH = text.get_height()

    global scr

    global snk
    snk.Draw(scr)
    
    scr.blit(text , ( (w - TW) // 2 , (h -  TH) // 2)) #draws the winning text
    
    ShowScore(scr) # shows the score
    
    pgm.display.flip()

    loop = True

    while loop :
        clock.tick(10)

        for ev in pgm.event.get() :
            if ev.type == pgm.QUIT :
                pgm.quit()
                sys.exit()
            if ev.type == pgm.KEYDOWN and ev.key == pgm.K_r :
                pgm.quit()
                loop = False # breaks to repeat the games loop ( see the last 3 lines )
                break

while True :
    Start() # Starts the Game
    if not Win :
        Game_Over() # if we get here that means A GameOver has happened
    else :
        Game_Win() # if we get here that means the Ai has Won the Game
