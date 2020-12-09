from math import sqrt

def getPossibleX(points):
    set_x = set()
    for point in points:
        set_x.add(point[0])
    return set_x
def getPossibleY(points):
    set_y = set()
    for point in points:
        set_y.add(point[1])
    return set_y
def findStartingAngle(start_point, next_point):
    if start_point[0] == next_point[0]:
        if start_point[1] < next_point[1]:
            angle = -90
        else:
            angle = 90
    else:
        if start_point[0] < next_point[0]:
            angle = 0
        else:
            angle = 180
    return angle
def insertPoint(array, point_x, point_y):
    if array[0][0] > int(point_x):
        array.insert(0, [int(point_x), int(point_y)])
    else:
        done = False
        if array[len(array) - 1][0] == int(point_x):
            end_x = int(point_x)
            end_index = len(array)
        else:
            for element in array:
                if element[0] > int(point_x):
                    end_index = array.index(element) - 1
                    end_x = array[end_index - 1][0]
                    if end_x < int(point_x):
                        array.insert(end_index + 1, [int(point_x), int(point_y)])
                        done = True
                    break
        if done == False:
            for element in array:
                if element[0] == end_x:
                    if element[1] > int(point_y):
                        array.insert(array.index(element), [int(point_x), int(point_y)])
                        done = True
                        break
            if done == False:
                array.insert(end_index, [int(point_x), int(point_y)])
    return array
def readPoint():
    points = []
    f = open("middle_point.txt", "r")
    lines = f.readlines()
    #Make list of points
    for line in lines:
        x = line[:line.find(",")]
        if x == "":
            break
        y = line[line.find(",")+1:line.find("\n")]
        points.append([int(x), int(y)])
    return points

def readEdge(points):
    edges =[]
    for point1 in points:
        count_x = 0
        count_y = 0
        for point2 in points:
            if point1[0] == point2[0] and point1[1] < point2[1] and count_x == 0:
                edges.append([[point1, point2], point2[1]-point1[1]])
                edges.append([[point2, point1], point2[1]-point1[1]])
                count_x += 1
            if point1[0] < point2[0] and point1[1] == point2[1] and count_y == 0:
                edges.append([[point1, point2], point2[0]-point1[0]])
                edges.append([[point2, point1], point2[0]-point1[0]])
                count_y += 1
            if count_x == 1 and count_y == 1:
                break
    #print(edges)
    #Make the weight of non-exist edges a large number
    for point1 in points:
        for point2 in points:
            if point1 != point2:
                flag = True
                for edge in edges:
                    if edge[0] == [point1, point2]:
                        flag = False
                        break
                if flag:
                    edges.append([[point1, point2], 1000000])
            else:
                edges.append([[point1, point2], 0])
    return edges

def findPath(starting_point_x, starting_point_y, ending_point_x, ending_point_y):
    starting_point_x = int(starting_point_x)
    starting_point_y = int(starting_point_y)
    ending_point_x = int(ending_point_x)
    ending_point_y = int(ending_point_y)
    d = []
    p = []
    points = readPoint()
    points = insertPoint(points, starting_point_x, starting_point_y)
    points = insertPoint(points, ending_point_x, ending_point_y)
    edges = readEdge(points)
    start_point = [int(starting_point_x), int(starting_point_y)]
    vertice = points.copy()
    for vertex in vertice:
        for edge in edges:
            if edge[0] == [start_point, vertex]:
                d.append([vertex, edge[1]])
                break
        p.append([vertex, start_point])
    #print(p)
    vertice.remove(start_point)
    while (len(vertice) != 0):
        min_d = 1000000
        for vertex in vertice:
            for d_e in d:
                if d_e[0] == vertex:
                    if d_e[1] < min_d:
                        min_d = d_e[1]
                        u = d_e[0]
                        break
        vertice.remove(u)
        for vertex in vertice:
            for edge in edges:
                if edge[0] == [u, vertex]:
                    old_path = min_d + edge[1]
                    break
            for d_e in d:
                if d_e[0] == vertex:
                    if d_e[1] > old_path:
                        d_e[1] = old_path
                        for p_e in p:
                            if p_e[0] == vertex:
                                p_e[1] = u;
    path = []
    path.append([ending_point_x, ending_point_y])
    currentPoint = [ending_point_x, ending_point_y]
    while (currentPoint != [starting_point_x, starting_point_y]):
        for p_e in p:
            if p_e[0] == currentPoint:
                currentPoint = p_e[1]
                path.insert(0, p_e[1])
    print(path)
def adjustPointToTheCenter(point_x, point_y):
    point_x = int(point_x)
    point_y = int(point_y)
    points = readPoint()
    edges = readEdge(points)
    set_x = getPossibleX(points)
    set_y = getPossibleY(points)
    min_distance = 10000
    for point in points:
        if int(abs(point[0] - point_x)) < 23 and int(abs(point[1] - point_y)) < 23:
            return point
    for edge in edges:
        if edge[1] != 0 and edge[1] != 1000000:
            distance = int(abs((edge[0][1][1] - edge[0][0][1])*point_x - (edge[0][1][0] - edge[0][0][0])*point_y + edge[0][1][0]*edge[0][0][1] - edge[0][0][0]*edge[0][1][1])/sqrt(pow(edge[0][1][1] - edge[0][0][1], 2) + pow(edge[0][1][0] - edge[0][0][0], 2)))
            if distance < min_distance:
                min_distance = distance
    for x in set_x:
        if point_x - min_distance == x or point_x + min_distance == x:
            return [x, point_y]
    for y in set_y:
        if point_y - min_distance == y or point_y + min_distance == y:
            return [point_x, y]
def adjustAngle(angle):
    angle = int(angle)
    if angle >= 0:
        if angle % 90 > 80:
            angle = 90 * (int(angle / 90) + 1)
        else:
            angle = 90 * (int(angle / 90))
    else:
        if angle % -90 < -80:
            angle = -90 * (int(angle / -90) + 1)
        else:
            angle = -90 * (int(angle / -90))
    return angle
def isPositiveTurn(current_point, current_dest, next_dest):
    if current_point[0] < current_dest[0]:
        if current_dest[1] > next_dest[1]:
            return True
        else:
            return False
    elif current_point[0] > current_dest[0]:
        if current_dest[1] > next_dest[1]:
            return False
        else:
            return True
    elif current_point[1] > current_dest[1]:
        if current_dest[0] > next_dest[0]:
            return True
        else:
            return False
    else:
        if current_dest[0] > next_dest[0]:
            return False
        else:
            return True
#starting_point_x = input("Enter starting point x: ")
#starting_point_y = input("Enter starting point y: ")
#ending_point_x = input("Enter ending point x: ")
#ending_point_y = input("Enter ending point y: ")
#point = adjustPointToTheCenter(starting_point_x, starting_point_y)
#print(89/90)
#print(adjustAngle(-89))
print(-120 / -90)
#findPath(starting_point_x, starting_point_y, ending_point_x, ending_point_y)
