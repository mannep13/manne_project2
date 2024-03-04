
import sys
#increase the capacity of the stack for recursion
sys.setrecursionlimit(10000)
from collections import deque


def processMove(move,row,col,direction):
    for c in direction:
        row=row+move[c][0]
        col=col+move[c][1]
    return row,col

def getValidNeighbours(nodeState,move,n,m,row,col):
    if row==(n-1) and col==(m-1):
        return []
    node=nodeState[row][col]
    color=node[0]
    direction=node[1]
    validNeighbours=[]
    step=0
    while True:
        step=step+1
        row,col=processMove(move,row,col,direction)
        if not(row>=0 and row<n and col>=0 and col<m):
            break
        if nodeState[row][col][0]!=color or nodeState[row][col][0]=='O':
            validNeighbours.append((row,col,step))
    return validNeighbours


def isReachable(graph,nodeState, src, dest, discovered, path):

    if src == dest:
        return True
    # mark the current node as discovered
    row_src=src[0]
    col_src=src[1]
    moves=nodeState[row_src][col_src][1]
    discovered[row_src][col_src] = True
    # if destination vertex is found
    # do for every edge (src, i)
    for childNode in graph[row_src][col_src]:
        child_row=childNode[0]
        child_col=childNode[1]
        steps=childNode[2]
        # if `u` is not yet discovered
        if not discovered[child_row][child_col]:
            # return true if the destination is found
                # include the current node in the path
            path.append(str(steps)+str(moves))
            if isReachable(graph,nodeState,(child_row,child_col), dest, discovered, path):
                return True
            # backtrack: remove the current node from the path
            path.pop()
        
    # return false if destination vertex is not reachable from src
    return False

def main():
    GRAPH_FILE_NAME = sys.argv[1]
    OUTPUT_FILE_NAME = sys.argv[2]
    # Get matrix/graph
    lines=[]
    with open(GRAPH_FILE_NAME) as file:
        lines = [line.split() for line in file]
    n,m=lines[0]
    n=int(n)
    m=int(m)
    nodeState=[[{} for j in range(m)] for i in range(n)]#graph[i][j]=[color,direction]
    graph=[[{} for j in range(m)] for i in range(n)]#graph[i][j]=[color,direction]

    for i in range(1,n+1):
        #print(lines[i])
        for j in range(m):
            if lines[i][j]=='O':
                nodeState[i-1][j]=lines[i][j]
            else:
                nodeState[i-1][j]=lines[i][j].split('-')
    
    

    
    move={}
    move['S']=[1,0]
    move['N']=[-1,0]
    move['E']=[0,1]
    move['W']=[0,-1]
    for i in range(n):
        for j in range(m):
            graph[i][j]=getValidNeighbours(nodeState,move,n,m,i,j)

    # to keep track of whether a vertex is discovered or not
    discovered = [[False for j in range(m)] for i in range(n)]
 
    # source and destination vertex
    (src, dest) = ((0,0),(n-1,m-1))
 
    # List to store the complete path between source and destination
    path = deque()
    
    # perform DFS traversal from the source vertex to check the connectivity
    # and store path from the source vertex to the destination vertex
    if isReachable(graph,nodeState,src, dest, discovered, path):
        print(f'Path exists from vertex {src} to vertex {dest}')
        #print(f'The complete path is', list(path))
        output=""
        for cell in list(path):
            output=output+str(cell)+" "
        print(output)
        with open(OUTPUT_FILE_NAME,"w") as outputFile:
            outputFile.write(output)

    else :
        print(f'Path doesnt exists from vertex {src} to vertex {dest}')

if __name__ == "__main__":
    main()

