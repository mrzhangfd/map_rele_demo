# -*- coding: utf-8 -*-
# @Time    :
# @Author  : zfd
# @File    : rele_window.py
# @Software: PyCharm
from pickle import dumps
from numpy import array, fromfile, uint8, zeros, square, math, int32, ones
import cv2 as cv
from re import findall
from PyQt5.QtWidgets import QPushButton, QLineEdit, QHBoxLayout, QVBoxLayout, QFileDialog, QWidget, QGraphicsView, \
    QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QImage, QPixmap
from baidu_ocr import BaiDuAPI
from photo_viewer import PhotoViewer
from mysql_conn import MySqlConn
from color_list import get_corlor_list
from matplotlib import pyplot as plt


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.init_WINDOW()

    def init_WINDOW(self):
        # 存储加载的图片和抽取的轮廓
        self.image = array([])
        self.cnt = array([])
        self.color_dict = get_corlor_list()
        self.choosePoints = []
        self.ocr_flag = False

        # 存储加载的图片和抽取的轮廓——第二个图片的信息
        self.image_1 = array([])
        self.cnt_1 = array([])
        self.color_dict_1 = get_corlor_list()
        self.choosePoints_1 = []
        self.ocr_flag_1 = False

        # 鼠标点击坐标和鼠标释放坐标
        self.x_clicked = 0
        self.y_clicked = 0
        self.x_released = 0
        self.y_released = 0

        # 鼠标点击坐标和鼠标释放坐标——第二个图
        self.x_clicked_1 = 0
        self.y_clicked_1 = 0
        self.x_released_1 = 0
        self.y_released_1 = 0

        self.fnmae = ''  # 加载的map
        self.baidu_api = BaiDuAPI()

        # 第二个图片的信息
        self.fnmae_1 = ''  # 加载的map
        self.baidu_api_1 = BaiDuAPI()

        # 图片图元
        self.viewer = PhotoViewer(self)
        self.viewer_1 = PhotoViewer(self)

        # UI初始化

        # 'Load image' button
        self.btnLoad = QPushButton(self)
        self.btnLoad.setText('图片加载')
        # self.btnLoad.setText('Img Load')
        self.btnLoad.clicked.connect(self.loadImage)

        # 'Load image' button ——第二个图片
        self.btnLoad_1 = QPushButton(self)
        self.btnLoad_1.setText('图片加载')
        # self.btnLoad.setText('Img Load')
        self.btnLoad_1.clicked.connect(self.loadImage_1)

        self.editYearInfo = QLineEdit(self)
        self.editYearInfo.setPlaceholderText('时间')

        self.editYearInfo_1 = QLineEdit(self)
        self.editYearInfo_1.setPlaceholderText('时间')

        # Button to change from drag/pan to getting pixel info
        self.btnClickDrag = QPushButton(self)
        self.btnClickDrag.setText('点击/拖拽')
        self.btnClickDrag.setIcon(QIcon("image/dragIcon.png"))
        self.btnClickDrag.clicked.connect(self.clickDrag)

        # Button to change from drag/pan to getting pixel info
        self.btnClickDrag_1 = QPushButton(self)
        self.btnClickDrag_1.setText('点击/拖拽')
        self.btnClickDrag_1.setIcon(QIcon("image/dragIcon.png"))
        self.btnClickDrag_1.clicked.connect(self.clickDrag_1)

        # 点击处的信息
        self.editClickInfo = QLineEdit(self)
        self.editClickInfo.setReadOnly(True)
        self.viewer.mouse_clicked.connect(self.photoClicked)  # 自建的鼠标点击的传递信号连接photoClicked函数

        # 点击处的信息——第二个图片
        self.editClickInfo_1 = QLineEdit(self)
        self.editClickInfo_1.setReadOnly(True)
        self.viewer_1.mouse_clicked.connect(self.photoClicked_1)  # 自建的鼠标点击的传递信号连接photoClicked函数

        # 轮廓生成按钮，连接轮廓生成函数
        self.btnContour = QPushButton(self)
        self.btnContour.setText('轮廓生成')
        self.btnContour.clicked.connect(self.getContour)

        # 轮廓生成按钮，连接轮廓生成函数——第二个图片
        self.btnContour_1 = QPushButton(self)
        self.btnContour_1.setText('轮廓生成')
        self.btnContour_1.clicked.connect(self.getContour_1)

        # 轮廓拖动按钮，连接轮廓拖动函数
        self.btnDrag = QPushButton(self)
        self.btnDrag.setText("轮廓拖拽")
        self.btnDrag.clicked.connect(self.dragOutline)
        self.viewer.mouse_released.connect(self.mouse_releasePoint)  # 自建鼠标松开信号连接了两个函数
        self.viewer.mouse_released.connect(self.contourDraged)

        # 轮廓拖动按钮，连接轮廓拖动函数——第二个图片
        self.btnDrag_1 = QPushButton(self)
        self.btnDrag_1.setText("轮廓拖拽")
        self.btnDrag_1.clicked.connect(self.dragOutline_1)
        self.viewer_1.mouse_released.connect(self.mouse_releasePoint_1)  # 自建鼠标松开信号连接了两个函数
        self.viewer_1.mouse_released.connect(self.contourDraged_1)

        # 获取轮廓信息的按钮
        self.btnContourInfo = QPushButton(self)
        self.btnContourInfo.setText("轮廓信息")
        # self.btnContourInfo.setText("Contour Info")
        self.btnContourInfo.clicked.connect(self.contour_info)

        # 获取轮廓信息的按钮——第二个图片
        self.btnContourInfo_1 = QPushButton(self)
        self.btnContourInfo_1.setText("轮廓信息")
        # self.btnContourInfo.setText("Contour Info")
        self.btnContourInfo_1.clicked.connect(self.contour_info_1)

        # 显示轮廓的信息
        self.editcontourName = QLineEdit(self)
        self.editcontourName.setPlaceholderText('轮廓名称')
        # self.editcontourName.setPlaceholderText('Contour Name')

        self.editContourArea = QLineEdit(self)
        self.editContourArea.setReadOnly(True)
        self.editContourArea.setPlaceholderText("轮廓面积")
        # self.editContourArea.setPlaceholderText("Area")
        self.editContourPerimeter = QLineEdit(self)
        self.editContourPerimeter.setReadOnly(True)
        self.editContourPerimeter.setPlaceholderText("轮廓周长")
        self.editContourCentre = QLineEdit(self)
        self.editContourCentre.setPlaceholderText("轮廓重心")
        self.editContourCentre.setReadOnly(True)

        # 显示轮廓的信息——第二个图片
        self.editcontourName_1 = QLineEdit(self)
        self.editcontourName_1.setPlaceholderText('轮廓名称')
        # self.editcontourName.setPlaceholderText('Contour Name')

        self.editContourArea_1 = QLineEdit(self)
        self.editContourArea_1.setReadOnly(True)
        self.editContourArea_1.setPlaceholderText("轮廓面积")
        # self.editContourArea.setPlaceholderText("Area")
        self.editContourPerimeter_1 = QLineEdit(self)
        self.editContourPerimeter_1.setReadOnly(True)
        self.editContourPerimeter_1.setPlaceholderText("轮廓周长")
        self.editContourCentre_1 = QLineEdit(self)
        self.editContourCentre_1.setPlaceholderText("轮廓重心")
        self.editContourCentre_1.setReadOnly(True)

        # 存储轮廓的信息
        self.btnContourSave = QPushButton(self)
        self.btnContourSave.setText("存储轮廓信息")
        # self.btnContourSave.setText("Store Profile Information")
        self.btnContourSave.clicked.connect(self.save_contour)

        # 存储轮廓的信息——第二个图片
        self.btnContourSave_1 = QPushButton(self)
        self.btnContourSave_1.setText("存储轮廓信息")
        # self.btnContourSave.setText("Store Profile Information")
        self.btnContourSave_1.clicked.connect(self.save_contour_1)

        # 地点识别
        self.btnSite = QPushButton(self)
        self.btnSite.setText("地点选择")
        # self.btnSite.setText("Site Selection")
        self.btnSite.clicked.connect(self.site_choose)
        self.viewer.mouse_moved.connect(self.draw_line)

        self.btnSiteInfo = QPushButton(self)
        self.btnSiteInfo.setText("地点信息")
        # self.btnSiteInfo.setText("Site Info")
        self.btnSiteInfo.clicked.connect(self.site_info)

        self.site_ContourName = QLineEdit(self)
        self.site_ContourName.setPlaceholderText("所属轮廓")
        # self.site_ContourName.setPlaceholderText("Contour Belong")

        self.editSiteName = QLineEdit(self)
        self.editSiteName.setPlaceholderText("地名")
        self.editSiteSlope = QLineEdit(self)
        self.editSiteSlope.setPlaceholderText('斜度')
        self.editSiteLenth = QLineEdit(self)
        self.editSiteLenth.setPlaceholderText('长度')
        self.editSitePos = QLineEdit(self)
        self.editSitePos.setPlaceholderText("位置")

        self.btnSiteSave = QPushButton(self)
        self.btnSiteSave.setText("存储地点信息")
        self.btnSiteSave.clicked.connect(self.save_site)

        # 地点识别——第二个图片
        self.btnSite_1 = QPushButton(self)
        self.btnSite_1.setText("地点选择")
        # self.btnSite.setText("Site Selection")
        self.btnSite_1.clicked.connect(self.site_choose_1)
        self.viewer_1.mouse_moved.connect(self.draw_line_1)

        self.btnSiteInfo_1 = QPushButton(self)
        self.btnSiteInfo_1.setText("地点信息")
        # self.btnSiteInfo.setText("Site Info")
        self.btnSiteInfo_1.clicked.connect(self.site_info_1)

        self.site_ContourName_1 = QLineEdit(self)
        self.site_ContourName_1.setPlaceholderText("所属轮廓")
        # self.site_ContourName.setPlaceholderText("Contour Belong")

        self.editSiteName_1 = QLineEdit(self)
        self.editSiteName_1.setPlaceholderText("地名")
        self.editSiteSlope_1 = QLineEdit(self)
        self.editSiteSlope_1.setPlaceholderText('斜度')
        self.editSiteLenth_1 = QLineEdit(self)
        self.editSiteLenth_1.setPlaceholderText('长度')
        self.editSitePos_1 = QLineEdit(self)
        self.editSitePos_1.setPlaceholderText("位置")

        self.btnSiteSave_1 = QPushButton(self)
        self.btnSiteSave_1.setText("存储地点信息")
        self.btnSiteSave_1.clicked.connect(self.save_site_1)

        # 第三列按钮
        self.btnSetRele = QPushButton(self)
        self.btnSetRele.setText("建立关联")
        self.btnSetRele.clicked.connect(self.save_rele)

        # 左图复位按钮
        self.btnReset = QPushButton(self)
        self.btnReset.setText("左图复位")
        self.btnReset.clicked.connect(self.reset)

        # 右图复位按钮
        self.btnReset_1 = QPushButton(self)
        self.btnReset_1.setText("右图复位")
        self.btnReset_1.clicked.connect(self.reset_1)

        # 消息提示框
        self.editHint = QLineEdit(self)
        self.editHint = QLineEdit(self)
        self.editHint.setPlaceholderText("消息提示")
        self.editHint.setReadOnly(True)

        self.setStyleSheet(
            "QPushButton{background-color: rgb(39, 118, 148)}"
            "QPushButton{color:white}" "QPushButton:hover{color:yellow}" "QPushButton:pressed{color:red;}"
            "QPushButton{border-radius:5px}" "QPushButton{border:2px groove gray}" "QPushButton{border-style: outset}" "QPushButton{padding:2px 4px}"
            "QLineEdit {border:2px groove gray}" "QLineEdit {border-radius:5px}" "QLineEdit{padding: 2px 4px}"
        )

        # Arrange layout
        HBlayoutAll = QHBoxLayout(self)

        # 左起，第一列布局，垂直布局。
        VBlayout = QVBoxLayout()
        VBlayout.addWidget(self.viewer)
        HBlayout = QHBoxLayout()
        HBlayout.setAlignment(Qt.AlignLeft)
        HBlayout.addWidget(self.btnLoad)
        HBlayout.addWidget(self.editYearInfo)
        HBlayout.addWidget(self.btnClickDrag)
        HBlayout.addWidget(self.editClickInfo)
        HBlayout.addWidget(self.btnContour)
        HBlayout.addWidget(self.btnDrag)

        # 第二行信息
        HBlayoutSecond = QHBoxLayout()
        HBlayoutSecond.setAlignment(Qt.AlignLeft)
        HBlayoutSecond.addWidget(self.btnContourInfo)
        HBlayoutSecond.addWidget(self.editcontourName)
        HBlayoutSecond.addWidget(self.editContourArea)
        HBlayoutSecond.addWidget(self.editContourPerimeter)
        HBlayoutSecond.addWidget(self.editContourCentre)
        HBlayoutSecond.addWidget(self.btnContourSave)

        # 第三行信息
        HBlayoutThird = QHBoxLayout()
        HBlayoutThird.setAlignment(Qt.AlignLeft)
        HBlayoutThird.addWidget(self.btnSite)
        HBlayoutThird.addWidget(self.btnSiteInfo)
        HBlayoutThird.addWidget(self.site_ContourName)
        HBlayoutThird.addWidget(self.editSiteName)
        HBlayoutThird.addWidget(self.editSiteSlope)
        HBlayoutThird.addWidget(self.editSiteLenth)
        HBlayoutThird.addWidget(self.editSitePos)
        HBlayoutThird.addWidget(self.btnSiteSave)

        VBlayout.addLayout(HBlayout)
        VBlayout.addLayout(HBlayoutSecond)
        VBlayout.addLayout(HBlayoutThird)

        ##左起，第二列布局，垂直布局。
        # 右边图片的布局
        VBlayout_1 = QVBoxLayout()
        VBlayout_1.addWidget(self.viewer_1)
        HBlayout_1 = QHBoxLayout()
        HBlayout_1.setAlignment(Qt.AlignLeft)
        HBlayout_1.addWidget(self.btnLoad_1)
        HBlayout_1.addWidget(self.editYearInfo_1)
        HBlayout_1.addWidget(self.btnClickDrag_1)
        HBlayout_1.addWidget(self.editClickInfo_1)
        HBlayout_1.addWidget(self.btnContour_1)
        HBlayout_1.addWidget(self.btnDrag_1)

        # 第二行信息
        HBlayoutSecond_1 = QHBoxLayout()
        HBlayoutSecond_1.setAlignment(Qt.AlignLeft)
        HBlayoutSecond_1.addWidget(self.btnContourInfo_1)
        HBlayoutSecond_1.addWidget(self.editcontourName_1)
        HBlayoutSecond_1.addWidget(self.editContourArea_1)
        HBlayoutSecond_1.addWidget(self.editContourPerimeter_1)
        HBlayoutSecond_1.addWidget(self.editContourCentre_1)
        HBlayoutSecond_1.addWidget(self.btnContourSave_1)

        # 第三行信息
        HBlayoutThird_1 = QHBoxLayout()
        HBlayoutThird_1.setAlignment(Qt.AlignLeft)
        HBlayoutThird_1.addWidget(self.btnSite_1)
        HBlayoutThird_1.addWidget(self.btnSiteInfo_1)
        HBlayoutThird_1.addWidget(self.site_ContourName_1)
        HBlayoutThird_1.addWidget(self.editSiteName_1)
        HBlayoutThird_1.addWidget(self.editSiteSlope_1)
        HBlayoutThird_1.addWidget(self.editSiteLenth_1)
        HBlayoutThird_1.addWidget(self.editSitePos_1)
        HBlayoutThird_1.addWidget(self.btnSiteSave_1)

        VBlayout_1.addLayout(HBlayout_1)
        VBlayout_1.addLayout(HBlayoutSecond_1)
        VBlayout_1.addLayout(HBlayoutThird_1)

        ##左起，第三列布局，垂直布局。
        VBlayout_2 = QVBoxLayout()
        VBlayout_2.addWidget(self.btnSetRele)
        VBlayout_2.addWidget(self.btnReset)
        VBlayout_2.addWidget(self.btnReset_1)
        # VBlayout_2.addWidget(self.editHint)

        HBlayoutAll.addLayout(VBlayout)
        HBlayoutAll.addLayout(VBlayout_1)
        HBlayoutAll.addLayout(VBlayout_2)

        self.setGeometry(500, 300, 800, 600)
        self.setWindowTitle('历史时空')
        self.setWindowIcon(QIcon('windowIcon.png'))
        self.show()

    # 图片加载
    def loadImage(self):
        self.fname, _ = QFileDialog.getOpenFileName(self, "选择地图", 'D:\\0Kind of File\\Map\\中国历史地图第三版',
                                                    'Image files(*.jpg *.gif *.png)')
        # fi = QtCott
        # re.QFileInfo(fname) 获取fname的信息
        if not self.fname:
            pass
        else:
            # 从新加载图片，清空变量
            # 存储加载的图片和抽取的轮廓
            self.image = array([])
            self.cnt = array([])

            # 鼠标点击坐标和鼠标释放坐标
            self.x_clicked = 0
            self.y_clicked = 0
            self.x_released = 0
            self.y_released = 0

            self.image = cv.imdecode(fromfile(self.fname, dtype=uint8), -1)
            year_img = self.image[0:100, 0:500]
            cut_bila = cv.bilateralFilter(year_img, d=0, sigmaColor=75, sigmaSpace=15)
            cv.imwrite('image/year.jpg', cut_bila)
            year_str = self.baidu_api.picture2text('image/year.jpg')
            year_int = findall(r'\d+', year_str)
            if '前' in year_str:
                map_year = -int(year_int[0])
            else:
                map_year = int(year_int[0])
            # myimage = open(self.fname, 'rb')
            # map_img = myimage.read()
            # mysqlConn = MySqlConn()
            self.editYearInfo.setText(str(map_year))
            # print(len(map_img))
            # mysqlConn.img_insert(map_year=map_year, map_img=map_img)
            image_height, image_width, image_depth = self.image.shape
            QIm = cv.cvtColor(self.image, cv.COLOR_BGR2RGB)
            QIm = QImage(QIm.data, image_width, image_height, image_width * image_depth,
                         QImage.Format_RGB888)
            self.viewer.setPhoto(QPixmap.fromImage(QIm))
            self.viewer.fitInView()

    #     图片加载——第二个图片
    def loadImage_1(self):
        self.fname_1, _ = QFileDialog.getOpenFileName(self, "选择地图", 'D:\\0Kind of File\\Map\\中国历史地图第三版',
                                                      'Image files(*.jpg *.gif *.png)')
        # fi = QtCott
        # re.QFileInfo(fname) 获取fname的信息
        if not self.fname_1:
            pass
        else:
            # 从新加载图片，清空变量
            # 存储加载的图片和抽取的轮廓
            self.image_1 = array([])
            self.cnt_1 = array([])

            # 鼠标点击坐标和鼠标释放坐标
            self.x_clicked_1 = 0
            self.y_clicked_1 = 0
            self.x_released_1 = 0
            self.y_released_1 = 0

            self.image_1 = cv.imdecode(fromfile(self.fname_1, dtype=uint8), -1)
            year_img = self.image_1[0:100, 0:500]
            cut_bila = cv.bilateralFilter(year_img, d=0, sigmaColor=75, sigmaSpace=15)
            cv.imwrite('image/year.jpg', cut_bila)
            year_str = self.baidu_api.picture2text('image/year.jpg')
            year_int = findall(r'\d+', year_str)
            if '前' in year_str:
                map_year = -int(year_int[0])
            else:
                map_year = int(year_int[0])
            # myimage = open(self.fname_1, 'rb')
            # map_img = myimage.read()
            # mysqlConn = MySqlConn()
            self.editYearInfo_1.setText(str(map_year))
            # print(len(map_img))
            # mysqlConn.img_insert(map_year=map_year, map_img=map_img)
            image_height, image_width, image_depth = self.image_1.shape
            QIm = cv.cvtColor(self.image_1, cv.COLOR_BGR2RGB)
            QIm = QImage(QIm.data, image_width, image_height, image_width * image_depth,
                         QImage.Format_RGB888)
            self.viewer_1.setPhoto(QPixmap.fromImage(QIm))
            self.viewer_1.fitInView()

    # 鼠标切换点击和拖拽模式
    def clickDrag(self):
        if self.viewer._contour or self.viewer._ocr:
            pass
        else:
            if self.viewer.dragMode():
                self.btnClickDrag.setIcon(QIcon("image/clickIcon.png"))
            else:
                self.btnClickDrag.setIcon(QIcon("image/dragIcon.png"))
            self.viewer.toggleDragMode()

    # 鼠标切换点击和拖拽模式-第二个图片
    def clickDrag_1(self):
        if self.viewer_1._contour or self.viewer_1._ocr:
            pass
        else:
            if self.viewer_1.dragMode():
                self.btnClickDrag_1.setIcon(QIcon("image/clickIcon.png"))
            else:
                self.btnClickDrag_1.setIcon(QIcon("image/dragIcon.png"))
            self.viewer_1.toggleDragMode()

    # 传递鼠标点击的坐标
    def photoClicked(self, pos):
        if self.viewer.dragMode() == QGraphicsView.NoDrag:
            self.editClickInfo.setText('%d, %d' % (pos.x(), pos.y()))
            self.x_clicked = pos.x()
            self.y_clicked = pos.y()

    # 传递鼠标点击的坐标-第二个图片
    def photoClicked_1(self, pos):
        if self.viewer_1.dragMode() == QGraphicsView.NoDrag:
            self.editClickInfo_1.setText('%d, %d' % (pos.x(), pos.y()))
            self.x_clicked_1 = pos.x()
            self.y_clicked_1 = pos.y()

    # 获取轮廓
    def getContour(self):

        # 获取鼠标点击处的hsv值
        hsv = cv.cvtColor(self.image, cv.COLOR_BGR2HSV)

        # 使用区域的hsv均值代替某一点的hsv的值
        area_hsv = [0, 0, 0]

        for i in range(-3, 6, 3):
            for j in range(-3, 6, 3):
                area_hsv = area_hsv + hsv[self.y_clicked - i, self.x_clicked - j]
        color_hsv = area_hsv // 9
        # 判断需要提取的hsv区间
        color = False
        for key, value in self.color_dict.items():
            if color_hsv[0] >= value[0][0] and color_hsv[0] <= value[1][0] and color_hsv[1] >= value[0][1] and \
                    color_hsv[1] <= value[1][1] and color_hsv[2] >= value[0][2] and color_hsv[2] <= value[1][2]:
                color = True
                lower_HSV = value[0]
                upper_HSV = value[1]
                self.color_dict.pop(key)
                self.color_dict[key] = value
                break
        if not color:
            print("请重新选区颜色")
        else:
            # 中值滤波去除椒盐噪声
            blurImg = cv.medianBlur(self.image, 21)
            img = cv.cvtColor(blurImg, cv.COLOR_BGR2HSV)
            # 提取对应的hsv区域
            mask = cv.inRange(img, lower_HSV, upper_HSV)
            choose_color = cv.bitwise_and(img, img, mask=mask)
            result = cv.cvtColor(choose_color, cv.COLOR_HSV2BGR)
            gray = cv.cvtColor(result, cv.COLOR_BGR2GRAY)  # 图象灰度化
            # 提取图象梯度(可改进）
            gradX = cv.Sobel(gray, ddepth=cv.CV_32F, dx=1, dy=0, ksize=-1)
            gradY = cv.Sobel(gray, ddepth=cv.CV_32F, dx=0, dy=1, ksize=-1)

            # gradX = cv.Scharr(gray, cv.CV_64F, 1, 0)
            # gradY = cv.Scharr(gray, cv.CV_64F, 0, 1)
            # 保留水平和竖直梯度大的
            gradient = cv.max(gradX, gradY)
            # cv.namedWindow("Img0", cv.WINDOW_KEEPRATIO)
            # cv.imshow("Img0", gradient)
            # cv.imwrite("img0.jpg", gradient)
            gradient = cv.convertScaleAbs(gradient)
            #  寻找轮廓
            # 采用三角形法进行二值化
            # hist = cv.calcHist([gradient],[0],None,[256],[0,256])
            # plt.plot(hist)
            # plt.show()
            ret, th = cv.threshold(gradient, 0, 255, cv.THRESH_BINARY | cv.THRESH_TRIANGLE)
            # cv.namedWindow("Img", cv.WINDOW_KEEPRATIO)
            # cv.imshow("Img", th)
            # cv.imwrite("img.jpg", th)
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
            # 闭运算，先腐蚀后膨胀，去除黑色小点
            closed = cv.morphologyEx(th, cv.MORPH_CLOSE, kernel, iterations=6)
            # 轮廓生成
            # cv.namedWindow("Img1", cv.WINDOW_KEEPRATIO)
            # cv.imshow("Img1", closed)
            # cv.imwrite("img1.jpg", closed)

            # OpenCV3 的findContours有三个返回值，OpenCV 4的有四个返回值
            # 应该安装opencv-python 3.*版本。
            # cnts ：返回的轮廓的列表
            myImage, cnts, hierarchy = cv.findContours(closed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
            num = 0
            con_exit = False
            for cnt in cnts:
                mesure = cv.pointPolygonTest(cnt, (self.x_clicked, self.y_clicked), measureDist=False)
                if mesure == 1:
                    con_exit = True
                    break
                num = num + 1
            if con_exit:
                self.cnt = cnts[num]  # 确定轮廓

                back = ones(self.image.shape, uint8) * 255
                img_contour = cv.drawContours(self.image.copy(), cnts, num, (255, 255, 255), 3)
                # img_contour1 = cv.drawContours(back, cnts, num, (0, 0, 255), 3)
                # 重新渲染
                image_height, image_width, image_depth = img_contour.shape
                QIm = cv.cvtColor(img_contour, cv.COLOR_BGR2RGB)
                QIm = QImage(QIm.data, image_width, image_height, image_width * image_depth,
                             QImage.Format_RGB888)
                self.viewer.setPhoto(QPixmap.fromImage(QIm))
                # 重新渲染后，图元回到拖拽模式
                self.btnClickDrag.setIcon(QIcon("image/dragIcon.png"))
            else:
                print("重新选区颜色点")

    # 获取轮廓-第二个图片
    def getContour_1(self):

        # 获取鼠标点击处的hsv值
        hsv = cv.cvtColor(self.image_1, cv.COLOR_BGR2HSV)

        # 使用区域的hsv均值代替某一点的hsv的值
        area_hsv = [0, 0, 0]

        for i in range(-3, 6, 3):
            for j in range(-3, 6, 3):
                area_hsv = area_hsv + hsv[self.y_clicked_1 - i, self.x_clicked_1 - j]
        color_hsv = area_hsv // 9
        # 判断需要提取的hsv区间
        color = False
        for key, value in self.color_dict.items():
            if color_hsv[0] >= value[0][0] and color_hsv[0] <= value[1][0] and color_hsv[1] >= value[0][1] \
                    and color_hsv[1] <= value[1][1] and color_hsv[2] >= value[0][2] and color_hsv[2] <= value[1][2]:
                color = True
                lower_HSV = value[0]
                upper_HSV = value[1]
                self.color_dict.pop(key)
                self.color_dict[key] = value

                break
        # (color)
        if not color:
            print("请重新选区颜色")
        else:
            # 中值滤波去除椒盐噪声
            blurImg = cv.medianBlur(self.image_1, 21)
            img = cv.cvtColor(blurImg, cv.COLOR_BGR2HSV)
            # 提取对应的hsv区域
            mask = cv.inRange(img, lower_HSV, upper_HSV)
            choose_color = cv.bitwise_and(img, img, mask=mask)
            result = cv.cvtColor(choose_color, cv.COLOR_HSV2BGR)
            gray = cv.cvtColor(result, cv.COLOR_BGR2GRAY)  # 图象灰度化
            # 提取图象梯度(可改进）
            gradX = cv.Sobel(gray, ddepth=cv.CV_32F, dx=1, dy=0, ksize=-1)
            gradY = cv.Sobel(gray, ddepth=cv.CV_32F, dx=0, dy=1, ksize=-1)

            # gradX = cv.Scharr(gray, cv.CV_64F, 1, 0)
            # gradY = cv.Scharr(gray, cv.CV_64F, 0, 1)
            # 保留水平和竖直梯度大的
            gradient = cv.max(gradX, gradY)
            # cv.namedWindow("Img0", cv.WINDOW_KEEPRATIO)
            # cv.imshow("Img0", gradient)
            # cv.imwrite("img0.jpg", gradient)
            gradient = cv.convertScaleAbs(gradient)
            #  寻找轮廓
            # 采用三角形法进行二值化
            # hist = cv.calcHist([gradient],[0],None,[256],[0,256])
            # plt.plot(hist)
            # plt.show()
            ret, th = cv.threshold(gradient, 0, 255, cv.THRESH_BINARY | cv.THRESH_TRIANGLE)
            # cv.namedWindow("Img", cv.WINDOW_KEEPRATIO)
            # cv.imshow("Img", th)
            # cv.imwrite("img.jpg", th)
            kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (5, 5))
            # 闭运算，先腐蚀后膨胀，去除黑色小点
            closed = cv.morphologyEx(th, cv.MORPH_CLOSE, kernel, iterations=6)

            # 轮廓生成
            # OpenCV3 的findContours有三个返回值，OpenCV 4的有四个返回值
            # 应该安装opencv-python 3.*版本。
            myImage, cnts, hierarchy = cv.findContours(closed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
            num = 0
            con_exit = False
            for cnt in cnts:
                mesure = cv.pointPolygonTest(cnt, (self.x_clicked_1, self.y_clicked_1), measureDist=False)
                if mesure == 1:
                    con_exit = True
                    break
                num = num + 1
            if con_exit:
                self.cnt_1 = cnts[num]  # 确定轮廓

                back = ones(self.image_1.shape, uint8) * 255
                img_contour = cv.drawContours(self.image_1.copy(), cnts, num, (255, 255, 255), 3)
                # img_contour1 = cv.drawContours(back, cnts, num, (0, 0, 255), 3)
                # 重新渲染
                image_height, image_width, image_depth = img_contour.shape
                QIm = cv.cvtColor(img_contour, cv.COLOR_BGR2RGB)
                QIm = QImage(QIm.data, image_width, image_height, image_width * image_depth,
                             QImage.Format_RGB888)
                self.viewer_1.setPhoto(QPixmap.fromImage(QIm))
                # 重新渲染后，图元回到拖拽模式
                self.btnClickDrag_1.setIcon(QIcon("image/dragIcon.png"))
            else:
                print("重新选区颜色点")

    # 轮廓拖动模式切换
    def dragOutline(self):
        if not self.viewer._contour:
            self.viewer._contour = True
            self.viewer.toggleDragMode()
            self.btnClickDrag.setIcon(QIcon("image/clickIcon.png"))
            self.btnDrag.setStyleSheet("QPushButton{color:red}")
        else:
            self.viewer._contour = False
            self.btnDrag.setStyleSheet("QPushButton{color:white}")

    # 轮廓拖动模式切换——第二个图片
    def dragOutline_1(self):
        if not self.viewer_1._contour:
            self.viewer_1._contour = True
            self.viewer_1.toggleDragMode()
            self.btnClickDrag_1.setIcon(QIcon("image/clickIcon.png"))
            self.btnDrag_1.setStyleSheet("QPushButton{color:red}")
        else:
            self.viewer_1._contour = False
            self.btnDrag_1.setStyleSheet("QPushButton{color:white}")

    # 获取鼠标松开的位置坐标
    def mouse_releasePoint(self, pos):
        self.x_released = pos.x()
        self.y_released = pos.y()

    # 获取鼠标松开的位置坐标——第二个图片
    def mouse_releasePoint_1(self, pos):
        self.x_released_1 = pos.x()
        self.y_released_1 = pos.y()

    # 轮廓拖动函数
    def contourDraged(self, pos):

        if self.viewer.dragMode() == QGraphicsView.NoDrag and self.viewer._contour == True:

            if self.cnt.any():
                for p in self.cnt:
                    if ((p[0][0] - self.x_clicked) ** 2 + (p[0][1] - self.y_clicked) ** 2) <= 25:
                        p[0][0] = p[0][0] + (pos.x() - self.x_clicked) * 0.9
                        p[0][1] = p[0][1] + (pos.y() - self.y_clicked) * 0.9
                    elif ((p[0][0] - self.x_clicked) ** 2 + (p[0][1] - self.y_clicked) ** 2) <= 100:
                        p[0][0] = p[0][0] + (pos.x() - self.x_clicked) * 0.7
                        p[0][1] = p[0][1] + (pos.y() - self.y_clicked) * 0.7
                    elif ((p[0][0] - self.x_clicked) ** 2 + (p[0][1] - self.y_clicked) ** 2) <= 225:
                        p[0][0] = p[0][0] + (pos.x() - self.x_clicked) * 0.5
                        p[0][1] = p[0][1] + (pos.y() - self.y_clicked) * 0.5
                    elif ((p[0][0] - self.x_clicked) ** 2 + (p[0][1] - self.y_clicked) ** 2) <= 400:
                        p[0][0] = p[0][0] + (pos.x() - self.x_clicked) * 0.3
                        p[0][1] = p[0][1] + (pos.y() - self.y_clicked) * 0.3
                    elif ((p[0][0] - self.x_clicked) ** 2 + (p[0][1] - self.y_clicked) ** 2) <= 625:
                        p[0][0] = p[0][0] + (pos.x() - self.x_clicked) * 0.1
                        p[0][1] = p[0][1] + (pos.y() - self.y_clicked) * 0.1

                # 重新渲染图元
                img_contour = cv.drawContours(self.image.copy(), self.cnt, -1, (255, 255, 255), 3)
                image_height, image_width, image_depth = img_contour.shape
                QIm = cv.cvtColor(img_contour, cv.COLOR_BGR2RGB)
                QIm = QImage(QIm.data, image_width, image_height, image_width * image_depth,
                             QImage.Format_RGB888)
                self.viewer.setPhoto(QPixmap.fromImage(QIm))
                self.viewer.curve_mode = True
                self.viewer.toggleDragMode()  # 判断是否还处于拖拽模式

    # 轮廓拖动函数——第二个图片
    def contourDraged_1(self, pos):

        if self.viewer_1.dragMode() == QGraphicsView.NoDrag and self.viewer_1._contour == True:

            if self.cnt_1.any():
                for p in self.cnt_1:
                    if ((p[0][0] - self.x_clicked_1) ** 2 + (p[0][1] - self.y_clicked_1) ** 2) <= 25:
                        p[0][0] = p[0][0] + (pos.x() - self.x_clicked_1) * 0.9
                        p[0][1] = p[0][1] + (pos.y() - self.y_clicked_1) * 0.9
                    elif ((p[0][0] - self.x_clicked_1) ** 2 + (p[0][1] - self.y_clicked_1) ** 2) <= 100:
                        p[0][0] = p[0][0] + (pos.x() - self.x_clicked_1) * 0.7
                        p[0][1] = p[0][1] + (pos.y() - self.y_clicked_1) * 0.7
                    elif ((p[0][0] - self.x_clicked_1) ** 2 + (p[0][1] - self.y_clicked_1) ** 2) <= 225:
                        p[0][0] = p[0][0] + (pos.x() - self.x_clicked_1) * 0.5
                        p[0][1] = p[0][1] + (pos.y() - self.y_clicked_1) * 0.5
                    elif ((p[0][0] - self.x_clicked_1) ** 2 + (p[0][1] - self.y_clicked_1) ** 2) <= 400:
                        p[0][0] = p[0][0] + (pos.x() - self.x_clicked_1) * 0.3
                        p[0][1] = p[0][1] + (pos.y() - self.y_clicked_1) * 0.3
                    elif ((p[0][0] - self.x_clicked_1) ** 2 + (p[0][1] - self.y_clicked_1) ** 2) <= 625:
                        p[0][0] = p[0][0] + (pos.x() - self.x_clicked_1) * 0.1
                        p[0][1] = p[0][1] + (pos.y() - self.y_clicked_1) * 0.1

                # 重新渲染图元
                img_contour = cv.drawContours(self.image_1.copy(), self.cnt_1, -1, (255, 255, 255), 3)
                image_height, image_width, image_depth = img_contour.shape
                QIm = cv.cvtColor(img_contour, cv.COLOR_BGR2RGB)
                QIm = QImage(QIm.data, image_width, image_height, image_width * image_depth,
                             QImage.Format_RGB888)
                self.viewer_1.setPhoto(QPixmap.fromImage(QIm))
                self.viewer_1.curve_mode = True
                self.viewer_1.toggleDragMode()  # 判断是否还处于拖拽模式

    # 获取轮廓的信息
    def contour_info(self):
        if self.cnt.any():
            ROI = zeros(self.image.shape[:2], uint8)
            proimage = self.image.copy()
            roi = cv.drawContours(ROI, [self.cnt], 0, (255, 255, 255), -1)
            x, y, w, h = cv.boundingRect(self.cnt)
            imgroi = cv.bitwise_and(proimage, proimage, mask=roi)
            site = imgroi[y:y + h, x:x + w]
            median_img = cv.medianBlur(site, 9)
            img_gray = cv.cvtColor(median_img, cv.COLOR_BGR2GRAY)
            th = cv.adaptiveThreshold(img_gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 65, 30)
            g = cv.getStructuringElement(cv.MORPH_RECT, (2, 1))
            # 形态学处理，开运算
            ersion = cv.erode(th, g, iterations=4)
            cv.imwrite('image/contour_name.jpg', ersion)
            contour_name = self.baidu_api.picture2text('image/contour_name.jpg')
            self.editcontourName.setText(contour_name)
            contour_area = cv.contourArea(self.cnt)
            contour_perimeter = cv.arcLength(self.cnt, True)
            M = cv.moments(self.cnt)
            self.contour_centre = str(int(M['m10'] / M['m00'])) + ',' + str(int(M['m01'] / M['m00']))
            self.editContourArea.setText("%d" % (contour_area))
            self.editContourPerimeter.setText("%d" % (contour_perimeter))
            self.editContourCentre.setText("%d,%d" % (int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])))

    # 获取轮廓的信息——第二个图片
    def contour_info_1(self):
        if self.cnt_1.any():
            ROI = zeros(self.image_1.shape[:2], uint8)
            proimage = self.image_1.copy()
            roi = cv.drawContours(ROI, [self.cnt_1], 0, (255, 255, 255), -1)
            x, y, w, h = cv.boundingRect(self.cnt_1)
            imgroi = cv.bitwise_and(proimage, proimage, mask=roi)
            site = imgroi[y:y + h, x:x + w]
            median_img = cv.medianBlur(site, 9)
            img_gray = cv.cvtColor(median_img, cv.COLOR_BGR2GRAY)
            th = cv.adaptiveThreshold(img_gray, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY_INV, 65, 30)
            g = cv.getStructuringElement(cv.MORPH_RECT, (2, 1))
            # 形态学处理，开运算
            ersion = cv.erode(th, g, iterations=4)
            cv.imwrite('image/contour_name.jpg', ersion)
            contour_name = self.baidu_api.picture2text('image/contour_name.jpg')
            self.editcontourName_1.setText(contour_name)
            contour_area = cv.contourArea(self.cnt_1)
            contour_perimeter = cv.arcLength(self.cnt_1, True)
            M = cv.moments(self.cnt_1)
            self.contour_centre_1 = str(int(M['m10'] / M['m00'])) + ',' + str(int(M['m01'] / M['m00']))
            self.editContourArea_1.setText("%d" % (contour_area))
            self.editContourPerimeter_1.setText("%d" % (contour_perimeter))
            self.editContourCentre_1.setText("%d,%d" % (int(M['m10'] / M['m00']), int(M['m01'] / M['m00'])))

    # 轮廓存储
    def save_contour(self):
        # 判断鼠标点击是否在原轮廓，
        # mesure = cv.pointPolygonTest(self.cnt, (self.x_clicked, self.y_clicked), measureDist=False)
        # # 不在，说明原轮廓处理完毕，可以将其所包含的区域填充黑色
        # if mesure != 1:

        ## 将self.image 修改了
        self.image = cv.drawContours(self.image, [self.cnt], 0, (0, 0, 0), -1)
        contour_year = int(self.editYearInfo.text())
        contour_name = self.editcontourName.text()
        contour_points_arr = self.cnt
        # (contour_points_arr)
        contour_points = dumps(contour_points_arr)  # narray 转换为二进制
        # print(contour_points)
        contour_area = float(self.editContourArea.text())
        contour_perimeter = float(self.editContourPerimeter.text())
        contour_centre = self.editContourCentre.text()

        mysqlConn = MySqlConn()
        mysqlConn.contour_insert(contour_year, contour_name, contour_points, contour_area, contour_perimeter,
                                 contour_centre)

    # 轮廓存储——第二个图片
    def save_contour_1(self):
        # 判断鼠标点击是否在原轮廓，
        # mesure = cv.pointPolygonTest(self.cnt, (self.x_clicked, self.y_clicked), measureDist=False)
        # # 不在，说明原轮廓处理完毕，可以将其所包含的区域填充黑色
        # if mesure != 1:
        #     # 将self.image 修改了
        # 获取色调范围列表
        self.image_1 = cv.drawContours(self.image_1, [self.cnt_1], 0, (0, 0, 0), -1)
        contour_year = int(self.editYearInfo_1.text())
        contour_name = self.editcontourName_1.text()
        contour_points_arr = self.cnt_1
        # print(contour_points_arr)
        contour_points = dumps(contour_points_arr)  # narray 转换为二进制
        # print(contour_points)
        contour_area = float(self.editContourArea_1.text())
        contour_perimeter = float(self.editContourPerimeter_1.text())
        contour_centre = self.editContourCentre_1.text()

        mysqlConn = MySqlConn()
        mysqlConn.contour_insert(contour_year, contour_name, contour_points, contour_area, contour_perimeter,
                                 contour_centre)

    # 存储轮廓关联
    def save_rele(self):

        # 将关联的两个轮廓区域覆盖黑色
        self.image = cv.drawContours(self.image, [self.cnt], 0, (0, 0, 0), -1)
        self.image_1 = cv.drawContours(self.image_1, [self.cnt_1], 0, (0, 0, 0), -1)

        # 基本思路：
        #     先去数据表map_rele中查询图片是否存在。
        #     如果该图片作为左侧图片时，已经存在，说明该图片已有前序。
        #     如果该图片作为右侧图片时，已经存在，说明该图片已有后序。

        # 第一个轮廓时间、名字
        contour_year = int(self.editYearInfo.text())
        print(contour_year, type(contour_year))
        contour_name = self.editcontourName.text()
        print(contour_name, type(contour_name))

        # 第二个轮廓时间、名字
        contour_year_1 = int(self.editYearInfo_1.text())
        print(contour_year_1, type(contour_year_1))
        contour_name_1 = self.editcontourName_1.text()
        print(contour_name_1, type(contour_name_1))

        # 查询左侧轮廓在数据库中是否存在，返回ret
        mysqlConn1 = MySqlConn()
        ret = mysqlConn1.select_contour(contour_year, contour_name)
        # 如果ret非空，则说明左侧轮廓已经有了前序轮廓。
        if ret:
            # 当ret[2] ret[3]都不为空时，all函数返回true
            if all([ret[2], ret[3]]):
                pre_contour_year = ret[2]
                pre_contour = ret[3]
                print(ret[2])
                print(ret[3])
                # 此时要存入数据库的后序轮廓就是右边图片中的轮廓。
                next_contour_year = contour_year_1
                next_contour = contour_name_1

                print(pre_contour_year, pre_contour, next_contour_year, next_contour)

                mysqlConn2 = MySqlConn()
                mysqlConn2.insert_rele(contour_year, contour_name, pre_contour_year, pre_contour, next_contour_year,
                                       next_contour)
            else:
                print("左侧轮廓在数据库中已有数据，但ret[2]或ret[3] 为空,说明左侧轮廓多次作为前序轮廓写入数据库")
                print("比如；左侧轮廓A关联到右侧轮廓B，但A真正对应的是C，将右侧复位后，就出现以上情况（A的ret[2]=0，ret[3]为空），"
                      "此时应该更新A的后序")
                mysqlConn3 = MySqlConn()
                mysqlConn3.insert_rele(contour_year, contour_name, ret[2], ret[3], contour_year_1, contour_name_1)
        else:
            # 数据库中没有左侧轮廓的关联信息，则直接插入，前序轮廓赋值为空。时间赋值为0.
            mysqlConn4 = MySqlConn()
            mysqlConn4.insert_rele(map_year=contour_year, contour_name=contour_name, pre_contour_year=0,
                                   pre_contour=None, next_contour_year=contour_year_1, next_contour=contour_name_1)

        # 在数据库中查询右侧轮廓是否存在
        mysqlConn5 = MySqlConn()
        ret_1 = mysqlConn5.select_contour(contour_year_1, contour_name_1)
        # 如果ret_1非空，则说明右侧轮廓已经有了后序轮廓。
        if ret_1:
            if all([ret_1[4], ret_1[5]]):
                # 此时要存入数据库的前序轮廓就是左边图片中的轮廓。
                pre_contour_year = contour_year
                pre_contour = contour_name
                next_contour_year = ret_1[4]
                next_contour = ret_1[5]
                mysqlConn6 = MySqlConn()
                mysqlConn6.insert_rele(contour_year, contour_name, pre_contour_year, pre_contour, next_contour_year,
                                       next_contour)
            else:
                print("右侧轮廓在数据库中已有数据，但ret[4]或ret[5] 为空,说明右边轮廓多次作为后序轮廓，写入数据库")
                print("比如；右侧轮廓B已经被左侧轮廓A关联，但B真正的前序是左侧的C，将左侧复位后，就出现以上情况（B的ret[4]=0，ret[5]为空），"
                      "此时应该更新B的前序")
                mysqlConn7 = MySqlConn()
                mysqlConn7.insert_rele(contour_year_1, contour_name_1, contour_year, contour_name, ret_1[4], ret_1[5])

        else:
            mysqlConn8 = MySqlConn()
            mysqlConn8.insert_rele(map_year=contour_year_1, contour_name=contour_name_1, pre_contour_year=contour_year,
                                   pre_contour=contour_name, next_contour_year=0, next_contour=None)

    # 图片复位
    def reset(self):
        print("reset 1")
        # 重新读入图片
        self.image = cv.imdecode(fromfile(self.fname, dtype=uint8), -1)
        image_height, image_width, image_depth = self.image.shape
        QIm = cv.cvtColor(self.image, cv.COLOR_BGR2RGB)
        QIm = QImage(QIm.data, image_width, image_height, image_width * image_depth,
                     QImage.Format_RGB888)
        self.viewer.setPhoto(QPixmap.fromImage(QIm))
        self.viewer.fitInView()

    def reset_1(self):
        print("reset 2")
        self.image_1 = cv.imdecode(fromfile(self.fname_1, dtype=uint8), -1)
        image_height, image_width, image_depth = self.image_1.shape
        QIm = cv.cvtColor(self.image_1, cv.COLOR_BGR2RGB)
        QIm = QImage(QIm.data, image_width, image_height, image_width * image_depth,
                     QImage.Format_RGB888)
        self.viewer_1.setPhoto(QPixmap.fromImage(QIm))
        self.viewer_1.fitInView()

    # 开启文字识别模式
    def site_choose(self):
        if not self.viewer._ocr:
            self.viewer._ocr = True
            self.viewer.toggleDragMode()
            self.x_clicked = 0
            self.y_clicked = 0
            self.x_released = 0
            self.y_released = 0
            self.btnSite.setStyleSheet("QPushButton{color:red}")
            self.ocr_flag = True
            self.btnClickDrag.setIcon(QIcon("image/clickIcon"))
        else:
            self.viewer._ocr = False
            self.btnSite.setStyleSheet("QPushButton{color:white}")
            self.ocr_flag = False

    # 开启文字识别模式——第二个图片
    def site_choose_1(self):
        if not self.viewer_1._ocr:
            self.viewer_1._ocr = True
            self.viewer_1.toggleDragMode()
            self.x_clicked_1 = 0
            self.y_clicked_1 = 0
            self.x_released_1 = 0
            self.y_released_1 = 0
            self.btnSite_1.setStyleSheet("QPushButton{color:red}")
            self.ocr_flag_1 = True
            self.btnClickDrag_1.setIcon(QIcon("image/clickIcon"))
        else:
            self.viewer._ocr_1 = False
            self.btnSite_1.setStyleSheet("QPushButton{color:white}")
            self.ocr_flag_1 = False

    # 文字区域画线
    def draw_line(self, pos):
        if self.viewer._ocr and self.x_clicked or self.y_clicked:
            img_line = cv.line(self.image.copy(), (self.x_clicked, self.y_clicked), (pos.x(), pos.y()), (0, 0, 0), 2)
            image_height, image_width, image_depth = img_line.shape
            QIm = cv.cvtColor(img_line, cv.COLOR_BGR2RGB)
            QIm = QImage(QIm.data, image_width, image_height, image_width * image_depth,
                         QImage.Format_RGB888)
            self.viewer.setPhoto(QPixmap.fromImage(QIm))
        # 终止画线
        if self.x_released or self.y_released:
            self.choosePoints = []  # 初始化存储点组
            inf = float("inf")
            if self.x_released or self.y_released:
                if (self.x_released - self.x_clicked) == 0:
                    slope = inf
                else:
                    slope = (self.y_released - self.y_clicked) / (self.x_released - self.x_clicked)

                siteLenth = 0.5 * math.sqrt(
                    square(self.y_released - self.y_clicked) + square(self.x_released - self.x_clicked))

                mySiteLenth = 2 * siteLenth
                self.siteLenth = ("%.2f" % mySiteLenth)
                self.editSiteLenth.setText(self.siteLenth)
                radian = math.atan(slope)
                self.siteSlope = ("%.2f" % radian)
                self.editSiteSlope.setText(self.siteSlope)
                x_bas = math.ceil(math.fabs(0.5 * siteLenth * math.sin(radian)))
                y_bas = math.ceil(math.fabs(0.5 * siteLenth * math.cos(radian)))

                if slope <= 0:
                    self.choosePoints.append([(self.x_clicked - x_bas), (self.y_clicked - y_bas)])
                    self.choosePoints.append([(self.x_clicked + x_bas), (self.y_clicked + y_bas)])
                    self.choosePoints.append([(self.x_released + x_bas), (self.y_released + y_bas)])
                    self.choosePoints.append([(self.x_released - x_bas), (self.y_released - y_bas)])
                elif slope > 0:
                    self.choosePoints.append([(self.x_clicked + x_bas), (self.y_clicked - y_bas)])
                    self.choosePoints.append([(self.x_clicked - x_bas), (self.y_clicked + y_bas)])
                    self.choosePoints.append([(self.x_released - x_bas), (self.y_released + y_bas)])
                    self.choosePoints.append([(self.x_released + x_bas), (self.y_released - y_bas)])
            self.viewer._ocr = False

    # 文字区域画线——第二个图片
    def draw_line_1(self, pos):
        if self.viewer_1._ocr and self.x_clicked_1 or self.y_clicked_1:
            img_line = cv.line(self.image_1.copy(), (self.x_clicked_1, self.y_clicked_1), (pos.x(), pos.y()), (0, 0, 0),
                               2)
            image_height, image_width, image_depth = img_line.shape
            QIm = cv.cvtColor(img_line, cv.COLOR_BGR2RGB)
            QIm = QImage(QIm.data, image_width, image_height, image_width * image_depth,
                         QImage.Format_RGB888)
            self.viewer_1.setPhoto(QPixmap.fromImage(QIm))
        # 终止画线
        if self.x_released_1 or self.y_released_1:
            self.choosePoints_1 = []  # 初始化存储点组
            inf = float("inf")
            if self.x_released_1 or self.y_released_1:
                if (self.x_released_1 - self.x_clicked_1) == 0:
                    slope = inf
                else:
                    slope = (self.y_released_1 - self.y_clicked_1) / (self.x_released_1 - self.x_clicked_1)

                siteLenth = 0.5 * math.sqrt(
                    square(self.y_released_1 - self.y_clicked_1) + square(self.x_released_1 - self.x_clicked_1))

                mySiteLenth = 2 * siteLenth
                self.siteLenth_1 = ("%.2f" % mySiteLenth)
                self.editSiteLenth_1.setText(self.siteLenth_1)
                radian = math.atan(slope)
                self.siteSlope_1 = ("%.2f" % radian)
                self.editSiteSlope_1.setText(self.siteSlope_1)
                x_bas = math.ceil(math.fabs(0.5 * siteLenth * math.sin(radian)))
                y_bas = math.ceil(math.fabs(0.5 * siteLenth * math.cos(radian)))

                if slope <= 0:
                    self.choosePoints_1.append([(self.x_clicked_1 - x_bas), (self.y_clicked_1 - y_bas)])
                    self.choosePoints_1.append([(self.x_clicked_1 + x_bas), (self.y_clicked_1 + y_bas)])
                    self.choosePoints_1.append([(self.x_released_1 + x_bas), (self.y_released_1 + y_bas)])
                    self.choosePoints_1.append([(self.x_released_1 - x_bas), (self.y_released_1 - y_bas)])
                elif slope > 0:
                    self.choosePoints_1.append([(self.x_clicked_1 + x_bas), (self.y_clicked_1 - y_bas)])
                    self.choosePoints_1.append([(self.x_clicked_1 - x_bas), (self.y_clicked_1 + y_bas)])
                    self.choosePoints_1.append([(self.x_released_1 - x_bas), (self.y_released_1 + y_bas)])
                    self.choosePoints_1.append([(self.x_released_1 + x_bas), (self.y_released_1 - y_bas)])
            self.viewer_1._ocr = False

    # 求地点信息
    def site_info(self):
        if self.ocr_flag:
            if self.choosePoints:
                site_contourName = self.editcontourName.text()
                self.site_ContourName.setText(site_contourName)
                points = array([self.choosePoints], int32)
                pts = points.reshape(-1, 1, 2)
                ROI = zeros(self.image.shape[:2], uint8)
                proimage = self.image.copy()
                roi = cv.drawContours(ROI, [pts], 0, (255, 255, 255), -1)
                x, y, w, h = cv.boundingRect(pts)
                imgroi = cv.bitwise_and(proimage, proimage, mask=roi)
                site = imgroi[y:y + h, x:x + w]
                cut_bila = cv.bilateralFilter(site, d=0, sigmaColor=75, sigmaSpace=15)
                self.site_centre = ((x + 0.5 * w), (y + 0.5 * h))
                cv.imwrite('image/site.jpg', cut_bila)
                siteName = self.baidu_api.picture2text('image/site.jpg')
                self.editSiteName.setText(siteName)
                self.editSitePos.setText(str(self.site_centre))

                self.viewer._ocr = True
                self.viewer.toggleDragMode()
                self.x_clicked = 0
                self.y_clicked = 0
                self.x_released = 0
                self.y_released = 0

    # 求地点信息——第二个图片
    def site_info_1(self):
        if self.ocr_flag_1:
            if self.choosePoints_1:
                site_contourName = self.editcontourName_1.text()
                self.site_ContourName_1.setText(site_contourName)
                points = array([self.choosePoints_1], int32)
                pts = points.reshape(-1, 1, 2)
                ROI = zeros(self.image_1.shape[:2], uint8)
                proimage = self.image_1.copy()
                roi = cv.drawContours(ROI, [pts], 0, (255, 255, 255), -1)
                x, y, w, h = cv.boundingRect(pts)
                imgroi = cv.bitwise_and(proimage, proimage, mask=roi)
                site = imgroi[y:y + h, x:x + w]
                cut_bila = cv.bilateralFilter(site, d=0, sigmaColor=75, sigmaSpace=15)
                self.site_centre_1 = ((x + 0.5 * w), (y + 0.5 * h))
                cv.imwrite('image/site.jpg', cut_bila)
                siteName = self.baidu_api_1.picture2text('image/site.jpg')
                self.editSiteName_1.setText(siteName)
                self.editSitePos_1.setText(str(self.site_centre_1))

                self.viewer_1._ocr = True
                self.viewer_1.toggleDragMode()
                self.x_clicked_1 = 0
                self.y_clicked_1 = 0
                self.x_released_1 = 0
                self.y_released_1 = 0

    # 存储地点信息
    def save_site(self):
        site_year = int(self.editYearInfo.text())
        site_name = self.editSiteName.text()
        site_contour = self.site_ContourName.text()
        site_slpoe = float(self.siteSlope)
        site_lenth = float(self.siteLenth)
        site_centre = str(self.site_centre)
        mysqlConn = MySqlConn()
        mysqlConn.site_insert(site_year, site_name, site_contour, site_slpoe, site_lenth, site_centre)

    # 存储地点信息——第二个图片
    def save_site_1(self):
        site_year = int(self.editYearInfo_1.text())
        site_name = self.editSiteName_1.text()
        site_contour = self.site_ContourName_1.text()
        site_slpoe = float(self.siteSlope_1)
        site_lenth = float(self.siteLenth_1)
        site_centre = str(self.site_centre_1)
        mysqlConn = MySqlConn()
        mysqlConn.site_insert(site_year, site_name, site_contour, site_slpoe, site_lenth, site_centre)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
