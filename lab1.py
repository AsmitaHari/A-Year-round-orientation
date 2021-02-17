from PIL import Image
from newaStar import astar
from bfs import BFS
import sys


class pixelObject:

    def __init__(self, terrain, elevation, x, y, neighbour):
        self.terrain = terrain
        self.elevation = elevation
        self.x = x
        self.y = y
        self.neighbour = neighbour

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


def loadTextFile(filename, imageObject, terrainTypeMap):
    content = []
    pixels = imageObject.load()
    with open(filename) as f:

        count = 0

        for line in f:
            line = line.strip()
            innerCount = -1
            innerList = []

            for x in line.split("  "):
                neighbour = []
                innerCount += 1

                p = pixelObject(pixels[innerCount, count], x.strip(), innerCount, count, neighbour)
                innerList.append(p)
                if (innerCount == 394):
                    break
            count = count + 1

            content.append(innerList)

    return content


def readStartAndEnd(filename, imageObject, pixelObjectArray,outputfile):
    pixels = imageObject.load()

    readableinput = open("read.txt", 'w')

    width, height = imageObject.size
    with open(filename) as f:
        firtspoint = f.readline().split()

        start = pixelObjectArray[int(firtspoint[1])][int(firtspoint[0])]
        points = []
        for line in f:
            lineArray = line.split()
            points.append((int(lineArray[0]), int(lineArray[1])))

        data = []

        for point in points:
            end = pixelObjectArray[point[1]][point[0]]

            path, parents = astar(pixels, pixelObjectArray, start, end, width,
                                  height, "Fall")
            drawImage(point, parents, imageObject,outputfile)
            start = pixelObjectArray[point[1]][point[0]]
            data = readable(pixels, points, point, parents, data)
        readableinput.writelines(data)  # save directions to file
        readableinput.write("\nTime taken is : %.0f " % (path / 60))  # save time to


def drawImage(start, path, im,outputfile):
    pathPixel = im.load()

    while True:

        im.putpixel((start[0], start[1]), (233, 19, 19, 255))
        if path[start] is None:
            break
        start = path[start]
    im.save(outputfile)


def openImage(imageName):
    im = Image.open(imageName)

    return im


def readable(pixels, points, point, parents, data):
    if points.index(point) != 0:
        data.append("In Point " + str(points.index(point)) + " Point is " + str(point) + "\t\n")
    end = point  # start a new path
    current = parents[end]  # take a step backwards
    while True:
        endOnPath = whereAmI(pixels, end[0], end[1])
        currentOnPath = whereAmI(pixels, current[0], current[1])
        if (endOnPath and not currentOnPath) or (not endOnPath and currentOnPath) or parents[current] is None:

            if endOnPath:
                data.append("Following path at end= " + str(end[0]) + " current= " + str(current[0])
                            + "and end= " + str(end[1]) + " current= " + str(current[1]) + " \t\n")  # write to buffer
            else:
                data.append("Path to go end=: " + str(end[0]) + " current=" + str(current[0])
                            + "and end= " + str(end[1]) + "current= " + str(current[1]) + "\t\n")
            end = current  # start a new path
            if parents[current] is None:  # our step backwards landed on the other control
                break
        current = parents[current]  # take a step backwards
    return data


def whereAmI(pixelMap, x, y):
    return pixelMap[x, y] == (0, 0, 0, 255) or pixelMap[x, y] == (71, 51, 3, 255)


def findWaterBodies(imageObject, season):
    listOfWaterEdges = set()

    pixels = imageObject.load()
    width, height = imageObject.size
    for i in range(width):
        for j in range(height):

            if (pixels[i, j] == (0, 0, 255, 255)):

                if i > 0 and pixels[i - 1, j] != (0, 0, 255, 255):
                    listOfWaterEdges.add((i - 1, j))
                if i < 394 and pixels[i + 1, j] != (0, 0, 255, 255):  # left dir
                    listOfWaterEdges.add((i + 1, j))
                if j > 0 and pixels[i, j - 1] != (0, 0, 255, 255):  # right dir
                    listOfWaterEdges.add((i, j - 1))
                if j < 499 and pixels[i, j + 1] != (0, 0, 255, 255):  # up dir
                    listOfWaterEdges.add((i, j + 1))
                if i > 0 and j > 0 and pixels[i - 1, j - 1] != (0, 0, 255, 255):  # down dir
                    listOfWaterEdges.add((i - 1, j - 1))
                if i < 394 and j > 0 and pixels[i + 1, j - 1] != (0, 0, 255, 255):  # diagonal
                    listOfWaterEdges.add((i + 1, j - 1))

                if i > 0 and j < 499 and pixels[i - 1, j + 1] != (0, 0, 255, 255):  # diagonal
                    listOfWaterEdges.add((i - 1, j + 1))
                if i < 394 and j < 499 and pixels[i + 1, j + 1] != (0, 0, 255, 255):  # diagonal
                    listOfWaterEdges.add((i + 1, j + 1))
    listOfWaterEdges = sorted(listOfWaterEdges)
    print(listOfWaterEdges)
    list=[]
    for i in listOfWaterEdges:
        neighbour=[]
        for new_position in [(0, -7), (0, 7), (-7, 0), (7, 0), (-7, -7), (-7, 7), (7, -7), (7, 7)]:
            node_position = (i[0] + new_position[0], i[1] + new_position[1])
            if node_position[0] > (394) or node_position[0] < 0 or node_position[1] > (
                    499) or node_position[1] < 0:
                continue
            else:
                neighbour.append(node_position)
                BFS(i,node_position,pixels,imageObject,season)

        list.append(neighbour)



    imageObject.save("test2.png")




def main(terrainFileName, elevationFile, path, sesason, outPutFile):
    imageObject = openImage(terrainFileName)
    terrainTypeMap = {(248, 148, 18, 255): "Open Land",
                      (255, 192, 0, 255): "Rough Meadow",
                      (255, 255, 255, 255): "Easy movement forest",
                      (2, 208, 60, 255): "Slow run forest",
                      (2, 136, 40, 255): "Walk forest",
                      (5, 73, 24, 255): "Impassible vegetation",
                      (0, 0, 255, 255): "Lake/Swamp/Marsh",
                      (71, 51, 3, 255): "Paved road",
                      (0, 0, 0, 255): "Footpath",
                      (205, 0, 101, 255): "Out of bounds"}
    pixelObjectArray = loadTextFile(elevationFile, imageObject, terrainTypeMap)
    if(sesason=="Winter" or sesason=="Spring"):
        findWaterBodies(imageObject, sesason)
        im = Image.open("test2.png")

        readStartAndEnd(path, im, pixelObjectArray,outPutFile)
    else:
        readStartAndEnd(path, imageObject, pixelObjectArray,outPutFile)




if __name__ == '__main__':
    len = sys.argv
    terrainFileName = sys.argv[1]
    elevationFile = sys.argv[2]
    path = sys.argv[3]
    sesason = sys.argv[4]
    outPutFile = sys.argv[5]

    main(terrainFileName, elevationFile, path, sesason, outPutFile)
