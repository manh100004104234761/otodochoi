import cv2
import numpy as np
import json

img = cv2.imread("nguyendu.png")
h, w, c = img.shape
count_press = 0
Coordinates = []
tmp = np.zeros(img.shape, np.uint8)
nodes = {}


def onMouseHandle(event, x, y, flags, param):
    global count_press
    if event == cv2.EVENT_LBUTTONDOWN:
        Coordinates.append((x, y))
        nodes[count_press] = (x, y)
        img[y, x] = (0, 255, 0)
        cv2.putText(img, str(count_press), (x, y),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 1, cv2.LINE_AA)
        count_press += 1
        # if (count_press % 2 == 0 and len(Coordinates) > 0):
        #     cv2.line(tmp, Coordinates[-2], Coordinates[-1],
        #              (255, 255, 255), 3, -1)
        #     cv2.line(img, Coordinates[-2], Coordinates[-1],
        #              (0, 255, 0), 3, -1)
        #     print(Coordinates[-1], Coordinates[-2])


def draw_line():
    cv2.namedWindow("test")
    cv2.setMouseCallback("test", onMouseHandle)
    while True:
        cv2.imshow("test", img)
        # cv2.imshow("result", tmp)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            cv2.imwrite("nodes.png", img)
            with open('nodes.txt', 'w') as filehandle:
                json.dump(nodes, filehandle)
            break


draw_line()

# def write_coordinate():
#     img_google_map = cv2.imread("nguyendu_processed.png")
#     indices = np.where(img_google_map == [255, 255, 255])
#     coordinates = zip(indices[0], indices[1])
#     unique_coordinates = list(set(list(coordinates)))
#     with open("coordinate.txt", "w") as f:
#         for i in unique_coordinates:
#             coordinate_to_str = str(i[0]) + " " + str(i[1])
#             f.write("%s\n" % coordinate_to_str)
