import json
import pickle
from pickle import dumps,loads
import numpy as np
import cv2 as cv
from mysql_conn import MySqlConn

img = cv.imread('C:\\Users\\icatzfd\\Desktop\\test.jpg')
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
ret, binary = cv.threshold(gray, 127, 255, cv.THRESH_BINARY)

#contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
myImage, cnts, hierarchy = cv.findContours(binary, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
img_contour=cv.drawContours(img, cnts, 1, (0, 0, 255), 3)
cnt=cnts[0]
print(cnt.shape)
list=cnt.tolist()
point_list=[]
for item in list:
    point=item[0]
    point_list.append(point)
print(str(point_list))
contour_year=18
contour_name="羊"
point_list_blob=str(point_list).encode(encoding="utf-8")
# mysqlConn = MySqlConn()
# mysqlConn.contour_insert_2_contour_point(contour_year,contour_name,point_list_blob)
# test_str="".join(str(point_list))
# print(test_str)
# print(type(test_str))

#cv.imshow("img", img)

cv.waitKey(0)

class Solution:

    def minInteger(self, num: str, k: int) -> str:
        if k <= 0 or not num:
            return num

        for i in range(0, 10):
            index = num.find(str(i))
            if index < 0:
                continue
            if index <= k:
                if k == index:
                    return str(i) + num[0:index] + num[index+1:]
                return str(i) + self.minInteger(num[0:index] + num[index+1:], k - index)
        return num