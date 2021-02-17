from queue import Queue
from collections import defaultdict


def getadjacent(n):
    x, y = n
    return [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x + 1, y - 1), (x - 1, y + 1), (x + 1, y + 1)]


def BFS(start, end, pixels,imageObject,season):
    queue = Queue()
    queue.put([start])  # Wrapping the start tuple in a list

    while not queue.empty():

        path = queue.get()
        pixel = path[-1]
         
        if pixel == end:

            return path
        listNm=getadjacent(pixel)

        for adjacent in getadjacent(pixel):

            x, y = adjacent

            if x<0 or x>394 or y<0 or y>499:
                continue
            if pixels[x, y] == (0, 0, 255, 255):
                if(season=="winter"):
                   pixels[x, y] = (0, 255, 255, 255)
                   imageObject.putpixel((x, y), (0, 255, 255, 255))
                if(season=="Spring"):
                    pixels[x, y] = (139, 69, 19, 255)
                    imageObject.putpixel((x, y), (139, 69, 19, 255))

                new_path = list(path)
                new_path.append(adjacent)
                queue.put(new_path)

