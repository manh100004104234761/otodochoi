import os
import random
import pygame
from math import sin, radians, degrees, copysign, sqrt, ceil, asin, degrees, floor
from pygame.math import Vector2

CAPTION = "Hello world"
SCREEN_SIZE = (1084, 720)
dest_pos = [-100, -100]
start_pos = [-100, -100]
path = []
path_current_index = 0
expected_pos_before_turn = []
expected_pos_after_turn = [0, 0]
index_before = 0
index_after = 0
repos_before = False
repos_after = False
keep_turning = False
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

def isTurning(current_point, current_dest, next_dest):
    if current_point[0] == current_dest[0] and current_dest[0] == next_dest[0]:
        return False
    elif current_point[1] == current_dest[1] and current_dest[1] == next_dest[1]:
        return False
    else:
        return True
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
        if vertex != start_point:
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
    return path
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
                if edge[0][0][0] == edge[0][1][0]:
                    if edge[0][0][1] > point_y and edge[0][1][1] < point_y or edge[0][0][1] < point_y and edge[0][1][1] > point_y:
                        min_distance = distance
                if edge[0][0][1] == edge[0][1][1]:
                    if edge[0][0][0] > point_x and edge[0][1][0] < point_x or edge[0][0][0] < point_x and edge[0][1][0] > point_x:
                        min_distance = distance
    for x in set_x:
        if point_x - min_distance == x or point_x + min_distance == x:
            return [x, point_y]
    for y in set_y:
        if point_y - min_distance == y or point_y + min_distance == y:
            return [point_x, y]

class Car(object):
    def __init__(self, CAR_IMAGE, ROAD_IMAGE, x, y, angle=-90, length=16):
        self.image = CAR_IMAGE
        self.road = ROAD_IMAGE
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(center=(0, 0))
        self.position = Vector2(x, y)
        self.velocity = Vector2(0.0, 0.0)
        self.angle = angle
        self.length = length
        self.steering = 0.0

    def update(self, dt):
        if self.steering:
            turning_radius = self.length / sin(radians(self.steering))
            angular_velocity = self.velocity.x / turning_radius
        else:
            angular_velocity = 0
        #self.rect.center = self.position
        next_position = self.position + self.velocity.rotate(-self.angle) * dt
        if self.road.get_at((int(next_position[0]), int(next_position[1]))) == (0, 0, 0, 255):
            self.position = next_position
            #print(self.position)
            self.rect.center = self.position
            self.angle += degrees(angular_velocity) * dt
        else:
            return


class Map(object):
    def __init__(self, map_image, car):
        self.image = map_image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.car = car
        self.car.rect.center = self.rect.center
        self.finished_flag = pygame.image.load("flag.png").convert_alpha()

    def update(self, dt):
        self.car.update(dt)

    def draw(self, surface):
        new_image = self.image.copy()
        surface.blit(new_image, (0, 0))
        rotated = pygame.transform.rotate(self.car.image, self.car.angle)
        rect = rotated.get_rect()
        self.car.rect = rect
        surface.blit(rotated, self.car.position -
                     (rect.width / 2, rect.height/2))
        surface.blit(self.finished_flag,
                     (dest_pos[0] - 32, dest_pos[1] - 27))
        pygame.display.flip()


class Control(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_rect()
        self.clock = pygame.time.Clock()
        self.fps = 60.0
        self.keys = pygame.key.get_pressed()
        self.done = False
        self.car = Car(CAR_IMAGE, ROAD_IMAGE, 24, 0)
        self.map = Map(MAP_IMAGE, self.car)
        self.count_clicked = 0
        self.ready = False

    def event_loop(self):
        global dest_pos, start_pos
        for event in pygame.event.get():
            if (self.ready):
                self.keys = pygame.key.get_pressed()
                if event.type == pygame.QUIT or self.keys[pygame.K_ESCAPE]:
                    self.done = True
                if self.keys[pygame.K_r]:
                    self.count_clicked = 0
                    self.ready = False
                if self.keys[pygame.K_w]:
                    self.car.velocity.x = 60
                elif self.keys[pygame.K_s]:
                    self.car.velocity.x = -60
                else:
                    self.car.velocity.x = 0

                if self.keys[pygame.K_d]:
                    self.car.steering = -4
                elif self.keys[pygame.K_a]:
                    self.car.steering = 4
                else:
                    self.car.steering = 0
            else:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.count_clicked += 1
                    if (self.count_clicked == 1):
                        if (ROAD_IMAGE.get_at((int(pos[0]), int(pos[1]))) == (0, 0, 0, 255)):
                            start_pos = adjustPointToTheCenter(int(pos[0]), int(pos[1]))
                            self.car = Car(
                                CAR_IMAGE, ROAD_IMAGE, start_pos[0], start_pos[1])
                            self.map = Map(MAP_IMAGE, self.car)
                        else:
                            print("not in road, pls click again")
                            self.count_clicked -= 1
                    if (self.count_clicked == 2):
                        if (ROAD_IMAGE.get_at((int(pos[0]), int(pos[1]))) == (0, 0, 0, 255)):
                            dest_pos = adjustPointToTheCenter(pos[0], pos[1])
                            self.ready = True
                        else:
                            print("not in road, pls click again")
                            self.count_clicked -= 1

    def auto_drive_loop(self):
        global dest_pos, start_pos, path, path_current_index, expected_pos_before_turn, expected_pos_after_turn, repos_before, repos_after, keep_turning, index_before, index_after
        if (self.ready):
            #print([expected_pos_before_turn, expected_pos_after_turn, self.car.position])
            if int(ceil(self.car.position[0])) == expected_pos_before_turn[0] and int(ceil(self.car.position[1])) == expected_pos_before_turn[1] or int(ceil(self.car.position[0])) == expected_pos_before_turn[0] and int(floor(self.car.position[1])) == expected_pos_before_turn[1] or int(floor(self.car.position[0])) == expected_pos_before_turn[0] and int(ceil(self.car.position[1])) == expected_pos_before_turn[1] or int(floor(self.car.position[0])) == expected_pos_before_turn[0] and int(floor(self.car.position[1])) == expected_pos_before_turn[1]:
                if index_before < path_current_index:
                    if path_current_index == len(path):
                        self.car.velocity.x = 0
                    else:
                        index_before += 1
                        index_after += 1
                        repos_before = True
                        if isTurning(expected_pos_before_turn, path[path_current_index], path[path_current_index + 1]):
                            keep_turning = True
                            self.car.velocity.x = 50
                            if isPositiveTurn(expected_pos_before_turn, path[path_current_index], path[path_current_index + 1]):
                                print("Positive")
                                self.car.steering = degrees(asin(self.car.length/23.0))
                                #print(degrees(asin(self.car.length/23.0)))
                            else:
                                self.car.steering = -degrees(asin(self.car.length/23.0))
                                print("Negative")
                                #print(degrees(asin(self.car.length/23.0)))
                        else:
                            self.car.velocity.x = 50
            elif keep_turning:
                if isPositiveTurn(expected_pos_before_turn, path[path_current_index], path[path_current_index + 1]):
                    self.car.velocity.x = 50
                    self.car.steering = degrees(asin(self.car.length/23.0))
                else:
                    self.car.velocity.x = 50
                    self.car.steering = -degrees(asin(self.car.length/23.0))
            else:
                self.car.velocity.x = 50
            if int(floor(self.car.position[0])) == expected_pos_after_turn[0] and int(floor(self.car.position[1])) == expected_pos_after_turn[1] or int(floor(self.car.position[0])) == expected_pos_after_turn[0] and int(ceil(self.car.position[1])) == expected_pos_after_turn[1] or int(ceil(self.car.position[0])) == expected_pos_after_turn[0] and int(floor(self.car.position[1])) == expected_pos_after_turn[1] or int(ceil(self.car.position[0])) == expected_pos_after_turn[0] and int(ceil(self.car.position[1])) == expected_pos_after_turn[1]:
                if index_after == path_current_index:
                    repos_after = True
                    keep_turning = False
                    path_current_index += 1
                    if path_current_index == len(path) - 1:
                        expected_pos_before_turn = path[path_current_index]
                    elif path[path_current_index][0] == path[path_current_index - 1][0]:
                        expected_pos_before_turn = [int(path[path_current_index][0]), int(path[path_current_index][1] - (path[path_current_index][1] - path[path_current_index - 1][1])/abs((path[path_current_index][1] - path[path_current_index - 1][1]))*23)]
                    else:
                        expected_pos_before_turn = [int(path[path_current_index][0] - (path[path_current_index][0] - path[path_current_index - 1][0])/abs((path[path_current_index][0] - path[path_current_index - 1][0]))*23), int(path[path_current_index][1])]
                    print(expected_pos_before_turn)
                    print(expected_pos_after_turn)
                    self.car.velocity.x = 50
                    self.car.steering = 0
        else:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    self.count_clicked += 1
                    if (self.count_clicked == 1):
                        if (ROAD_IMAGE.get_at((int(pos[0]), int(pos[1]))) == (0, 0, 0, 255)):
                            start_pos = adjustPointToTheCenter(int(pos[0]), int(pos[1]))
                            self.car = Car(
                                CAR_IMAGE, ROAD_IMAGE, start_pos[0], start_pos[1])
                            self.map = Map(MAP_IMAGE, self.car)
                        else:
                            print("not in road, pls click again")
                            self.count_clicked -= 1
                    if (self.count_clicked == 2):
                        if (ROAD_IMAGE.get_at((int(pos[0]), int(pos[1]))) == (0, 0, 0, 255)):
                            dest_pos = adjustPointToTheCenter(pos[0], pos[1])
                            path = findPath(start_pos[0], start_pos[1], dest_pos[0], dest_pos[1])
                            if path[path_current_index + 1][0] == path[path_current_index][0]:
                                expected_pos_before_turn = [int(path[path_current_index + 1][0]), int(path[path_current_index + 1][1] - (path[path_current_index + 1][1] - path[path_current_index][1])/abs((path[path_current_index + 1][1] - path[path_current_index][1]))*23)]
                            else:
                                expected_pos_before_turn = [int(path[path_current_index + 1][0] - (path[path_current_index + 1][0] - path[path_current_index][0])/abs((path[path_current_index + 1][0] - path[path_current_index][0]))*23), int(path[path_current_index + 1][1])]
                            path_current_index += 1
                            if path[path_current_index + 1][0] == path[path_current_index][0]:
                                expected_pos_after_turn = [int(path[path_current_index][0]), int(path[path_current_index][1] + (path[path_current_index + 1][1] - path[path_current_index][1])/abs((path[path_current_index + 1][1] - path[path_current_index][1]))*23)]
                            else:
                                expected_pos_after_turn = [int(path[path_current_index][0] + (path[path_current_index + 1][0] - path[path_current_index][0])/abs((path[path_current_index + 1][0] - path[path_current_index][0]))*23), int(path[path_current_index][1])]
                            angle = findStartingAngle(path[0], path[1])
                            self.car = Car(
                                CAR_IMAGE, ROAD_IMAGE, start_pos[0], start_pos[1], angle)
                            self.map = Map(MAP_IMAGE, self.car)
                            self.ready = True
                        else:
                            print("not in road, pls click again")
                            self.count_clicked -= 1
    def display_fps(self):
        caption = "{} - FPS: {:.2f}".format(CAPTION, self.clock.get_fps())
        pygame.display.set_caption(caption)

    def update(self, dt):
        global repos_before, repos_after, expected_pos_before_turn, expected_pos_after_turn
        """
        Update the level. In this implementation player updating is taken
        care of by the level update function.
        """
        self.screen.fill(pygame.Color("black"))
        if not repos_before and not repos_after:
            self.map.update(dt)
        if repos_before:
            self.car.position = expected_pos_before_turn
            self.map.update(dt)
            print(self.car.position)
            repos_before = False
        if repos_after:
            print("update sau")
            self.car.position = expected_pos_after_turn
            self.car.angle = adjustAngle(self.car.angle)
            self.map.update(dt)
            repos_after = False
            if path_current_index == len(path) - 1:
                expected_pos_after_turn = path[path_current_index]
            elif path[path_current_index + 1][0] == path[path_current_index][0]:
                expected_pos_after_turn = [int(path[path_current_index][0]), int(path[path_current_index][1] + (path[path_current_index + 1][1] - path[path_current_index][1])/abs((path[path_current_index + 1][1] - path[path_current_index][1]))*23)]
            else:
                expected_pos_after_turn = [int(path[path_current_index][0] + (path[path_current_index + 1][0] - path[path_current_index][0])/abs((path[path_current_index + 1][0] - path[path_current_index][0]))*23), int(path[path_current_index][1])]
        self.map.draw(self.screen)

    def main_loop(self):
        while not self.done:
            dt = self.clock.get_time() / 1000
            self.event_loop()
            self.update(dt)
            pygame.display.update()
            self.clock.tick(self.fps)
            self.display_fps()

    def auto_drive(self):
        while True:
            dt = self.clock.get_time() / 1000
            self.auto_drive_loop()
            self.update(dt)
            pygame.display.update()
            self.clock.tick(self.fps)
            self.display_fps()

def main():
    global MAP_IMAGE, CAR_IMAGE, ROAD_IMAGE
    pygame.init()
    pygame.display.set_caption("car")
    pygame.display.set_mode(SCREEN_SIZE)
    CAR_IMAGE = pygame.image.load("car32x16.png").convert_alpha()
    MAP_IMAGE = pygame.image.load("map1084x720.png").convert_alpha()
    ROAD_IMAGE = pygame.image.load("road1084x720.png").convert_alpha()
    #Control().main_loop()
    Control().auto_drive()
    pygame.quit()


if __name__ == "__main__":
    main()
