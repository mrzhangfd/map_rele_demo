from mysql_conn import MySqlConn
from pickle import dumps, loads

#mysqlConn = MySqlConn()
# contour_year=936
# contour_name="楚"
# ret=mysqlConn.select_contour_info(contour_year,contour_name)
#
# contour=ret[0]
# print(contour[1])
# print(type(contour[2]))
# point_list=loads(contour[2])
# print(point_list)
# ret = mysqlConn.select_all_contour_info()
#mysqlConn.delete_contour_point(229,"孙吴")
mysqlConn1 = MySqlConn()
ret=mysqlConn1.select_contour_info(229,"羌胡");
points=ret[0][2]
points_list=loads(points).tolist();
print(points_list)
temp_list = []
for item in points_list:
    point = item[0]
    temp_list.append(point)
print(temp_list)
for temp in temp_list:
    point_x = temp[0]
    point_y = temp[1]
    mysqlConn = MySqlConn()
    mysqlConn.insert_contour_point(229, "羌胡", point_x, point_y)
# print(len(ret))
# for contour in ret:
#     points = contour[2]
#     # print(points)
#     print(contour[0],contour[1])
#     points_list = loads(points).tolist()
#     temp_list = []
#     for item in points_list:
#         point = item[0]
#         temp_list.append(point)
#     for temp in temp_list:
#         point_x = temp[0]
#         point_y = temp[1]
#         mysqlConn = MySqlConn()
#         mysqlConn.insert_contour_point(contour[0], contour[1], point_x, point_y)
# contour=ret[0]
# points=contour[2]
# list = loads(points)
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
