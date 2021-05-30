# from comtypes.safearray import numpy
#
# from mysql_conn import MySqlConn
# from pickle import dumps,loads
#
# mysqlConn = MySqlConn()
# contour_year=12
# contour_name="汉"
# ret=mysqlConn.select_contour_info(contour_year, contour_name)
# contour=ret[0]
# points=contour[2]
# list = loads(points)
# print(len(list))
# point_list=[]
# for item in list:
#     point=item[0]
#     point_list.append(point)
# print(point_list)
# for point in point_list:
#     point_x=point[0]
#     point_y=point[1]
#     mysqlConn = MySqlConn()
#     mysqlConn.insert_contour_point(contour[0],contour[1],point_x,point_y)
i=0
while i<5:
    print(i)
    if i==2:
        break
        print("*")
    i+=1
print("test")