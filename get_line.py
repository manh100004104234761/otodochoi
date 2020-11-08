import cv2
import numpy as np
import json

img = cv2.imread("nguyendu.png")
tmp = np.zeros(img.shape, np.uint8)

with open('nodes.txt', 'r') as filehandle:
    nodes = json.load(filehandle)
filehandle.close()

lines = open('lines.txt', 'r')
for line in lines:
    connect_nodes = line.split(" ")
    start = (nodes[connect_nodes[0]][0], nodes[connect_nodes[0]][1])
    end = (nodes[connect_nodes[1][:-1]][0], nodes[connect_nodes[1][:-1]][1])
    cv2.line(tmp, start, end,
             (255, 255, 255), 1)

indices = np.where(tmp == [255, 255, 255])
coordinates = zip(indices[0], indices[1])
unique_coordinates = list(set(list(coordinates)))
with open("coordinate.txt", "w") as f:
    for i in unique_coordinates:
        coordinate_to_str = str(i[0]) + " " + str(i[1])
        f.write("%s\n" % coordinate_to_str)
