import random

#Directions :

UP = ( 0 , 1 )
DOWN = ( 0 , -1 )
RIGHT = ( 1 , 0 )
LEFT = ( -1 , 0 )

ALL_DIR = ( UP , DOWN , RIGHT , LEFT )

HORZ = [RIGHT , LEFT] # Horizontal Directions
VER = [UP , DOWN] # Vertical Directions

class Node :
    BlockingDirections = [] # the Directions we can't reach

    Visited : bool = False

    def __init__(self) -> None:
        self.Visited = False
        self.BlockingDirections = []

def CalculateSimpleDistance(P1 : tuple[int , int] , P2 : tuple[int,int]) : 
    return abs(P1[0] - P2[0]) + abs(P1[1] - P2[1])

def MovePoint(Point : tuple[int,int] , Dir : tuple[int, int]) : 
    return (Point[0] + Dir[0] , Point[1] - Dir[1])

def Compare(l) : 
    return l[1]

def AStarPathFinding(Map : list , Start : int, Target : int , limit : int = None) : 
    Vertices = [[None , None , None , None]] * len(Map) 
    #[Distance From the beginning , Distance to the Target , the Direction we came from , the index of the vertex we came from]
    
    l = 0
    
    path = []

    v = [(Map[Start],0)]

    Vertices[Start] = [0 , 0 , None , None]

    Trg = Map[Target] # the target coordinates
    while len(v) > 0 :
        if limit != None :
            l += 1
            if l >= limit :
                raise Exception("Limit Overflow")
        cv = v.pop(0) # Current vertex
        cindex = Map.index(cv[0])
        if cindex != Target : 
            for dir in ALL_DIR :
                NP = MovePoint(cv[0] , dir)
                if NP in Map :
                    index = Map.index(NP)
                    Dis1 = Vertices[cindex][0] + CalculateSimpleDistance(NP,cv[0])
                    Dis2 = CalculateSimpleDistance(NP,Trg) - ( 1 if dir == Vertices[cindex][3] else 0)
                    CNeighbor = Vertices[index]
                    if (CNeighbor [0] == None or Dis2 < CNeighbor[1]) and (Vertices[Target][0] == None or Vertices[Target][0] > Dis2) : 
                        v.append((NP,Dis2))
                        Vertices[index] = [Dis1 , Dis2, dir , cindex]
            v.sort(key=Compare)
        else :
            break
    if Vertices[Target][0] == None : # we didn't find a solution
        raise Exception("No such path found to the Target")
    else : 
        cv = Vertices[Target] # Current vertex
        while cv != Vertices[Start] : 
            path.append(cv[2])
            cv = Vertices[cv[3]]
        
        path.reverse()
        return path
 
def GenerateEmptiesMap(snk , apl , Gx : int , Gy : int , ExceptHead = False , Exceptapl = False) :
    """Returns all the empty points coordinates in a snake game : Points that doesn't include the Snake's body (Optionaly the apple) \n
    :parameter : \n
    SNK : The Snake's Body \n
    APPLE : The APPLE or its position \n
    Remove : Positions to Remove from the Map \n\n

    ExceptHead : set it to True if you want to consider the head's position as Empty\n\n

    GX : the Map's Width \n
    GY : The Map's Height
    """

    SPOS = snk.Pos if not ExceptHead else snk.Pos[1:len(snk)]#Snake body Positions

    APOS = apl.Pos#Apple Position

    toreturn = []
    for y in range(Gy) :
        for x in range(Gx) :
            if (x, y) not in SPOS:
                if apl == None or (x,y) != APOS or Exceptapl :
                    toreturn.append( (x,y) )

    return toreturn

def GenerateMap(Gx : int, Gy : int , reverse : bool = False) :

    """Generates a List of all the Map's Positions
        Gx : the Width of the Map
        Gy : the Height of the Map
        reverse : usually the Map will be generated starting from the left up corner going down
                    reversing means we will start at the same position going to the right
    """

    toreturn = []
    
    for y in range(Gy) :
        for x in range(Gx) :
            if reverse :
                toreturn.append((y,x))
            else :
                toreturn.append((x,y))
    
    return toreturn

def GenerateMapGraph(Mp : list) :

    Graph = [None] * len(Mp)

    for i in range(len(Mp)) :
        Point = Mp[i] # the point of the index i on the map
        
        for dir in ALL_DIR :
            NP = (Point[0] + dir[0] , Point[1] - dir[1]) # the new point if we follow that direction
            
            if NP in Mp :
                if Graph[i] == None :
                    Graph[i] = []
                
                Graph[i].append([Mp.index(NP) , 1])
            
    return Graph

def PrimsAlgorithm(G : list , Start : int) :
    
    visited = [Start]

    sol = [None] * len(G) # the Solution

    while len(visited) < len(G) :
        SmallestDis = None # the smallest distance (the smallest edge length / weight)
        ver = None
        ver2 = None

        rv = [] #vertices list to choose from randomly when finding two edges with the same length 
        re = [] #edges list to choose from randomly when finding two edges with the same length

        for v in visited : 
            for edge in G[v] :
                if edge[0] not in visited and (SmallestDis == None or edge[1] < SmallestDis) : 
                    rv = []
                    re = []
                    SmallestDis = edge[1]
                    ver = v
                    ver2 = edge[0]
                elif edge[0] not in visited and SmallestDis == edge[1] :
                    rv.append(v)
                    re.append(edge)
                elif edge[0] in visited : 
                    G[v].remove(edge) # removing the edge so we dont search it again (for improving the efficiency)

        if len(rv) > 0 :
            i = random.randint(0,len(rv)-1)
            ver = rv[i]
            ver2 = re[i][0]
            SmallestDis = re[i][1]
 
        G[ver].remove([ver2 , SmallestDis])
        G[ver2].remove([ver , SmallestDis])
        # removing the edges so we dont search them again (for improving the efficiency)
        
        if sol[ver] == None :
            sol[ver] = []

        sol[ver].append([ver2 , SmallestDis])

        visited.append(ver2)
        
    return sol

def GenerateHamiltonianMaze(Graph : list , Map : list , Gx : int, Gy : int) -> list[Node]:
    l = Gx * Gy 
    
    Maze = [None] * l 

    for i in range(l) : 
        Maze[i] = Node()

    for i in range(len(Graph)):
        if Graph[i] != None :
            vx , vy = Map[i] # the vertex's x and y coordinates

            for edge in Graph[i] :

                nvx = vx * 2 + 1 # the projected x coordinate
                nvy = vy * 2 + 1 # the projected y coordinate

                vx2 , vy2 = Map[edge[0]] # the vertex's coordinates which is adjacent to Graph[i] vertex

                Dir = (vx2 - vx , vy - vy2) #the Direction From the Vertex1 to it's adjacent (Vertex2)
                
                nvx2 = vx2 * 2 + 1
                nvy2 = vy2 * 2 + 1

                if nvx2 < nvx or nvy2 < nvy :
                    nvx = nvx2
                    nvy = nvy2
                    Dir = (-Dir[0] , -Dir[1])

                for j in range(2) :
                    if Dir in HORZ :
                        Maze[Gx * nvy + nvx].BlockingDirections.append(UP)
                        Maze[Gx * (nvy-1) + nvx].BlockingDirections.append(DOWN)
                        #Blocking the way in both sides

                        nvx += Dir[0]
                    else :
                        Maze[Gx * nvy + nvx].BlockingDirections.append(LEFT)
                        Maze[Gx * nvy + nvx - 1].BlockingDirections.append(RIGHT)
                        #Blocking the way in both sides

                        nvy -= Dir[1]
        
                pass

    return Maze

def InsideBorders(x : int , y : int , Gx : int, Gy : int) : 
    return x < Gx and x >= 0 and y < Gy and y >= 0 

def Maze2Cycle(Maze : list[Node] , Gx : int, Gy : int) : 
    P = (0,0) # Current Position
    dir = (1,0) # the direction we're going
    right = (0,-1) # our right direction relative to our facing direction
    # think about it like your Right Hand
    # if you are facing the north your right hand direction is the east
    # but if you are facing the south your right hand direction is the west 

    l = Gx * Gy

    sol = [P]# the solution we've found

    path = []#the path of the hamiltonian cycle to follow

    for N in range(l) :
        x , y = P
        if dir not in  Maze[y * Gx  + x].BlockingDirections and InsideBorders(x + dir[0] , y - dir[1] , Gx , Gy)  : # our direction is not blocked
            Maze[y * Gx  + x].Visited = True

            x += dir[0]
            y -= dir[1]

            P = (x,y)
            sol.append(P)
            path.append(dir)
        else :
            # we will search a Non Blocked Direction that doesn't lead to a Visited Node
            for d in ALL_DIR :
                nx = x + d[0]
                ny = y - d[1]
                NP = (nx,ny)
                
                if d not in Maze[y * Gx + x].BlockingDirections and InsideBorders(nx , ny , Gx , Gy) and not Maze[ny * Gx  + nx].Visited :
                    Maze[y * Gx + x].Visited = True
                    P = NP
                    dir = d

                    if dir in HORZ : # our direction is Horizontal
                        right = (0,-dir[0])
                    else : # our direction is Vertical 
                        right = (dir[1],0)
                    
                    sol.append(P)
                    path.append(dir)
                    break
        if right not in Maze[y * Gx  + x].BlockingDirections and InsideBorders(x + right[0] , y - right[1] , Gx , Gy) : # we can go right 
            dir = right 
            
            if dir in HORZ : # our direction is Horizontal
                right = (0,-dir[0])
            else : # our direction is Vertical
                right = (dir[1],0)
            # rotating our direction to the right         

    return sol , path