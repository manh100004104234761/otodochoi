import cv2
import imutils
import numpy as np
import json

img = cv2.imread("nguyendu.png")
car = cv2.imread("car.png")
h, w, c = img.shape
count_press = 0
map_with_car = img
move = {
    0: [1, 0],
    45: [1, 1],
    90: [0, 1],
    135: [-1, 1],
    180: [-1, 0],
    225: [-1, -1],
    270: [0, -1],
    315: [1, -1],
}
nodes = {}
valid_coordinate = []
f = open("coordinate.txt", "r")
lines = f.readlines()
for line in lines:
    xy = line.split(" ")
    x = int(xy[0])
    y = int(xy[1][:-1])
    map_with_car[x, y] = (0, 255, 0)
    valid_coordinate.append([x, y])

car_coordinate = (0, 0)


def draw_car(x, y, angle=0):
    tmp = img.copy()
    car_tmp = imutils.rotate_bound(car, angle)
    y1, y2 = y - int(car_tmp.shape[0]/2) - 1, y - \
        int(car_tmp.shape[0]/2) - 1 + car_tmp.shape[0]
    x1, x2 = x - int(car_tmp.shape[1]/2) - 1, x - \
        int(car_tmp.shape[1]/2) - 1 + car_tmp.shape[1]
    alpha_s = car_tmp[:, :, 2] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        tmp[y1:y2, x1:x2, c] = (alpha_s * car_tmp[:, :, c] +
                                alpha_l * tmp[y1:y2, x1:x2, c])
    return tmp


def moving(x, y, last_angle, angle):
    new_angle = (last_angle + angle) % 360
    move_xy = move[new_angle]
    x += move_xy[0]
    y += move_xy[1]
    return (x, y, new_angle)


def onMouseHandle(event, x, y, flags, param):
    global count_press, car_coordinate
    if event == cv2.EVENT_LBUTTONDOWN:
        if [y, x] in valid_coordinate:
            car_coordinate = (x, y)
            map_with_car = draw_car(x, y)
            print("ready")


cv2.namedWindow("test")
cv2.setMouseCallback("test", onMouseHandle)

start = False
last_angle = 0

while True:
    cv2.imshow("test", map_with_car)
    key = cv2.waitKey(33) & 0xFF
    if key == ord("g"):
        start = True
    if key == ord("q"):
        break
    if start:
        # print(last_angle)
        for angle in np.arange(0, 360, 45):
            if angle < 270 and angle > 90:
                continue
            x, y, new_angle = moving(
                car_coordinate[0], car_coordinate[1], last_angle, angle)
            if [y, x] in valid_coordinate:
                map_with_car = draw_car(
                    car_coordinate[0], car_coordinate[1], last_angle)
                last_angle = new_angle
                car_coordinate = (x, y)
                continue
