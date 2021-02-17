import math
from queue import PriorityQueue


def endEqCurNode(cur,end):
    return cur==end

# determine the estimated cost f() = g() + h()
def costFunction(pixelMap, elevationArray, timeToNode, curr, next, heading, goal,season):


    currTerrain = pixelMap[curr[0], curr[1]]
    currElevation = float(elevationArray[curr[1]][curr[0]].elevation)
    nextTerrain = pixelMap[next[0], next[1]]
    nextElevation = float(elevationArray[curr[1]][next[0]].elevation)
    rise = nextElevation - currElevation


    # determine which direction we're going
    if heading == "up"or heading =="down":
        run = 7.55     # moving up
    elif heading == "left" or heading == "right":
        run = 10.29    # moving down
    else:
        run = 12.76
    grade = (rise/run)*100
    dist = run

    if currTerrain == (5, 73, 24, 255) or currTerrain == (0, 0, 255, 255) or currTerrain == (205, 0, 101, 255):
        currSpeed = 0
    elif currTerrain == (255, 192, 0, 255):
        currSpeed = 2.0
    elif currTerrain == (255, 255, 255, 255):
        currSpeed = 2.5
    elif currTerrain == (2, 208, 60):
        currSpeed = 2.0
    elif currTerrain == (2, 136, 40, 255):
        currSpeed = 1.0
    elif currTerrain == (0, 0, 0, 255):
        currSpeed = 3.0
    elif currTerrain == (71, 51, 3, 255):
        currSpeed = 4.0
    elif currTerrain == (0, 255, 255, 255):
        currSpeed = 1.5
    elif currTerrain == (139, 69, 19, 255):
        currSpeed = 0.5

    else:
        currSpeed = 3.0  # open land
    if nextTerrain == (5, 73, 24, 255) or nextTerrain == (0, 0, 255, 255) or nextTerrain == (205, 0, 101, 255):
        nextSpeed = 0
    elif nextTerrain == (255, 192, 0, 255):
        nextSpeed = 2.0
    elif nextTerrain == (255, 255, 255, 255) and season=="Fall":
        nextSpeed = 3.5
    elif nextTerrain == (255, 255, 255, 255):
        nextSpeed = 2.5
    elif nextTerrain == (2, 208, 60):
        nextSpeed = 2.0
    elif nextTerrain == (2, 136, 40, 255):
        nextSpeed = 1.0
    elif nextTerrain == (0, 0, 0, 255):
        nextSpeed = 3.0
    elif nextTerrain == (71, 51, 3, 255):
        nextSpeed = 4.0
    elif nextTerrain == (0, 255, 255, 255):
        nextSpeed = 1.5
    elif nextTerrain == (139, 69, 19, 255):
        nextSpeed = 0.5
    else:
        nextSpeed = 3.0
    if currSpeed == 0 or nextSpeed == 0:
        time = float("inf")
    else:
        time = ((dist/2)/currSpeed) + ((dist/2)/nextSpeed)
    if grade >= 0:
        time += (dist*grade*0.0080529707)
    else:
        time -= (dist*grade*0.004970964566929)
    timeToNode[next] = timeToNode[curr] + time
    return timeToNode[next] + heuristic(next, goal)



def heuristic(next, goal):
    D = 1.8875
    D2 = 3.19
    dx = abs(next[0] - goal[0])
    dy = abs(next[1] - goal[1])
    return D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)  # diagonal distance heuristic equation


def astar(pixel, elevationArray,start, end,width,height,season):
    start = (start.x, start.y)
    end = (end.x, end.y)
    NodeToTime={}
    NodeToTime[start]=0
    parents={start:None}
    child=PriorityQueue()
    child.put((0,start))

    while not child.empty():
          state=child.get()[1]

          if endEqCurNode(state,end):
            return NodeToTime[end],parents
          for nei in neighbour(state):

              if (nei[0], nei[1]) not in parents:
                  next = (int(nei[0]), int(nei[1]))
                  dir = nei[2]
                  t = (costFunction(pixel, elevationArray, NodeToTime, state, next, dir, end,season), next)  # heuristic
                  child.put(t)
                  parents[(nei[0], nei[1])] = (state[0], state[1])







def neighbour(state):
    x = int(state[0])
    y = int(state[1])
    neighbour = []                     # heading is necessary to keep as it will determine the distance traveled
    if x > 0:
        neighbour.append((x-1, y, 'left'))
    if x < 394:                         # left dir
        neighbour.append((x+1, y, 'right'))
    if y > 0:                           # right dir
        neighbour.append((x, y-1, 'up'))
    if y < 499:                         # up dir
        neighbour.append((x, y+1, 'down'))
    if x > 0 and y > 0:                 # down dir
        neighbour.append((x-1, y-1, 'diagonal'))
    if x < 394 and y > 0:               # diagonal
        neighbour.append((x+1, y-1, 'diagonal'))
    if x > 0 and y < 499:               # diagonal
        neighbour.append((x-1, y+1, 'diagonal'))
    if x < 394 and y < 499:             # diagonal
        neighbour.append((x+1, y+1, 'diagonal'))
    return neighbour
