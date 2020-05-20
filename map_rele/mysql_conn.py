# -*- coding: utf-8 -*-
# @Time    : 2019/1/10 16:08
# @Author  : Bo
# @Email   : mat_wu@163.com
# @File    : mysql_conn_time.py
# @Software: PyCharm

from configparser import ConfigParser
from pymysql import connect, Error

db_config = 'password.txt'


class MySqlConn(object):
    """数据库连接"""

    # 数据库初始化连接
    def __init__(self):
        try:
            target = ConfigParser()
            target.read(db_config, encoding='utf-8')  # 注意编码方式,可以修改位utf-8-sig

            host = target.get('mysqlConfigure', 'host')
            db = target.get('mysqlConfigure', 'db')
            user = target.get('mysqlConfigure', 'user')
            password = target.get('mysqlConfigure', 'password')
            port = int(target.get('mysqlConfigure', 'port'))
            charset = target.get('mysqlConfigure', 'charset')
            self._conn = connect(host=host, user=user, passwd=password, db=db, port=port, charset=charset)
            if (self._conn):
                self._cur = self._conn.cursor()
        except IOError:
            print("Error: 无法连接数据库")

    # 图片入库
    def img_insert(self, map_year, map_img):
        insertString = 'insert into primal_map(map_year,map_image) values (%s,%s) ON DUPLICATE KEY UPDATE map_image = values(map_image)'
        args = (map_year, map_img)
        try:
            self._cur.execute(insertString, args)
            self._conn.commit()
        except Error as e:
            self._conn.rollback()
            print("插入失败")
        # 无论如何，连接记得关闭游标和数据库链接
        finally:
            self._cur.close()  # 关闭游标
            self._conn.close()  # 释放数据库资源

    # 轮廓入库
    def contour_insert(self, contour_year, contour_name, contour_points, contour_area, contour_perimeter,
                       contour_centre):
        print(contour_year, contour_name, contour_points, contour_area, contour_perimeter, contour_centre)
        insertString = 'insert into contour_info(contour_year,contour_name,contour_points,contour_area,contour_perimeter,contour_centre) values (%s,%s,%s,%s,%s,%s)' \
                       'ON DUPLICATE KEY UPDATE contour_points = values(contour_points),contour_area = values(contour_area),contour_perimeter = values(contour_perimeter),' \
                       'contour_centre = values(contour_centre)'
        args = (contour_year, contour_name, contour_points, contour_area, contour_perimeter, contour_centre)
        try:
            self._cur.execute(insertString, args)
            self._conn.commit()
        except Error as e:
            self._conn.rollback()
            print("插入失败")
        finally:
            # 无论如何，连接记得关闭游标和数据库链接
            self._cur.close()  # 关闭游标
            self._conn.close()  # 释放数据库资源

    # 地点入库
    def site_insert(self, site_year, site_name, site_contour, site_slope, site_lenth, site_centre):
        insertString = 'insert into site_info(site_year, site_name, site_contour,site_slope, site_lenth, site_centre) values (%s,%s,%s,%s,%s,%s)' \
                       'ON DUPLICATE KEY UPDATE site_contour = values(site_contour),site_slope = values(site_slope),site_lenth = values (site_lenth),site_centre = values (site_centre)'

        args = (site_year, site_name, site_contour, site_slope, site_lenth, site_centre)
        try:
            self._cur.execute(insertString, args)
            self._conn.commit()
        # 无论如何，连接记得关闭游标和数据库链接
        except Error as e:
            self._conn.rollback()
            print("插入失败")
        finally:
            self._cur.close()  # 关闭游标
            self._conn.close()  # 释放数据库资源

    # 根据map_year和contour_name 查询轮廓
    def select_contour(self, map_year, contour_name):
        print("this is select_contour")
        select_string = 'select * from map_rele where map_year=%s and contour_name=%s'

        args = (map_year, contour_name)
        try:
            self._cur.execute(select_string, args)
            ret = self._cur.fetchone()
            self._conn.commit()
            return ret
        # 无论如何，连接记得关闭游标和数据库链接
        except Error as e:
            self._conn.rollback()
            print("插入失败")
        finally:
            self._cur.close()  # 关闭游标
            self._conn.close()  # 释放数据库资源

    # 根据map_year和contour_name 查询轮廓
    def select_all(self, map_year,next_contour_year):
        print("this is select_contour")
        select_string = 'select * from map_rele where (map_year=%s ) or (map_year=%s )'

        args = (map_year,next_contour_year)
        try:
            self._cur.execute(select_string, args)
            ret = self._cur.fetchall()
            self._conn.commit()
            return ret
        # 无论如何，连接记得关闭游标和数据库链接
        except Error as e:
            self._conn.rollback()
            print("插入失败")
        finally:
            self._cur.close()  # 关闭游标
            self._conn.close()  # 释放数据库资源

    def insert_rele(self, map_year, contour_name, pre_contour_year, pre_contour,
                    next_contour_year, next_contour):
        insertString = 'insert into map_rele(map_year, contour_name, pre_contour_year,pre_contour, next_contour_year,next_contour) ' \
                       'values (%s,%s,%s,%s,%s,%s)' \
                       'ON DUPLICATE KEY UPDATE pre_contour_year = values(pre_contour_year),' \
                       'pre_contour = values(pre_contour),next_contour_year = values (next_contour_year),next_contour = values (next_contour)'

        args = (map_year, contour_name, pre_contour_year, pre_contour, next_contour_year, next_contour)
        try:
            self._cur.execute(insertString, args)
            self._conn.commit()
        except Error as e:
            self._conn.rollback()
            print("插入失败")
        # 无论如何，连接记得关闭游标和数据库链接
        finally:
            self._cur.close()  # 关闭游标
            self._conn.close()  # 释放数据库资源

    # 根据当前轮廓、后序轮廓删除记录
    def delete_rele_bynext(self, map_year, contour_name, next_contour_year, next_contour):
        deleteString = 'delete from map_rele where map_year=%s and contour_name=%s and next_contour_year=%s and next_contour=%s'

        args = (map_year, contour_name, next_contour_year, next_contour)

        try:
            print(deleteString)
            self._cur.execute(deleteString, args)
            self._conn.commit()
        except Error as e:
            self._conn.rollback()
            print("删除失败")
        # 无论如何，连接记得关闭游标和数据库链接
        finally:
            self._cur.close()  # 关闭游标
            self._conn.close()  # 释放数据库资源

    # 根据当前轮廓、前序轮廓删除记录
    def delete_rele_bypre(self, map_year, contour_name, pre_contour_year, pre_contour):
        deleteString = 'delete from map_rele where map_year=%s and contour_name=%s and pre_contour_year=%s and pre_contour=%s'

        args = (map_year, contour_name, pre_contour_year, pre_contour)

        try:
            print(deleteString)
            self._cur.execute(deleteString, args)
            self._conn.commit()
        except Error as e:
            self._conn.rollback()
            print("删除失败")
        # 无论如何，连接记得关闭游标和数据库链接
        finally:
            self._cur.close()  # 关闭游标
            self._conn.close()  # 释放数据库资源


    def delete_rele_byKey(self,map_year,contour_name):
        deleteString = 'delete from map_rele where map_year=%s and contour_name=%s'

        args = (map_year, contour_name)

        try:
            print(deleteString)
            self._cur.execute(deleteString, args)
            self._conn.commit()
        except Error as e:
            self._conn.rollback()
            print("删除失败")
        # 无论如何，连接记得关闭游标和数据库链接
        finally:
            self._cur.close()  # 关闭游标
            self._conn.close()  # 释放数据库资源
