import cv2

img = cv2.imread("img.png")
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

height, witdh = img.shape

for i in range(0, height):
    for j in range(0, witdh):
        if(img[i][j] == 0):
            continue
        else:
            img[i][j] = 255

cv2.imwrite("test.png", img)
