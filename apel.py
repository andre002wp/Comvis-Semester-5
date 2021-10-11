import sys
import os
import cv2

img = cv2.imread("1.jpg",cv2.IMREAD_UNCHANGED)
img2 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite("Sample2.jpg", img2)