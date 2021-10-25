# Filename: hello.py

"""Simple Hello World example with PyQt5."""
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage,QPixmap
import sys
import os
import cv2
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)



class Ui(QtWidgets.QMainWindow):
    
    img = []
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('Comvis I Design.ui', self)

        self.tabWidget.currentChanged.connect(self.tabChanged)
        self.btnOpenFile = self.findChild(QtWidgets.QPushButton, 'openFilebtn_2')
        self.btnOpenFile.clicked.connect(self.loadImage) 

        self.btnNegasi = self.findChild(QtWidgets.QPushButton, 'btnNegasi')
        self.btnNegasi.clicked.connect(self.Negatemeh) 

        self.btnPengembangan = self.findChild(QtWidgets.QPushButton, 'btnPengembangan')
        self.btnPengembangan.clicked.connect(self.Kembanginmeh) 

        self.btnFlipHorizontal = self.findChild(QtWidgets.QPushButton, 'btnMirrorHorizontal')
        self.btnFlipHorizontal.clicked.connect(self.MirrormehHorizontally) 

        self.btnFlipVertikal = self.findChild(QtWidgets.QPushButton, 'btnMirrorVertikal')
        self.btnFlipVertikal.clicked.connect(self.MirrormehVertically) 

        self.btnFlipCampuran = self.findChild(QtWidgets.QPushButton, 'btnMirrorCampuran')
        self.btnFlipCampuran.clicked.connect(self.MirrormehEmmYea)

        self.btnConvolusi = self.findChild(QtWidgets.QPushButton, 'btnConvolve')
        self.btnConvolusi.clicked.connect(self.Convolusi)

        self.btnDilasi = self.findChild(QtWidgets.QPushButton, 'btnDilasi')
        self.btnDilasi.clicked.connect(self.Dilate)

        self.btnErosi = self.findChild(QtWidgets.QPushButton, 'btnErosi')
        self.btnErosi.clicked.connect(self.Erode)

        self.addToolBar(NavigationToolbar(self.Histogram.canvas, self))

        self.show()
        

    def tabChanged(self):
        print("Tab Changed to : ",self.tabWidget.currentIndex())


    def loadImage(self):
        # This is executed when the button is pressed
        print('btn Open File Pressed')
        openFileDialog = QFileDialog.getOpenFileName(self,"select Image File",os.getcwd(),"Image Files (*.jpg *.gif *.bmp *.png *.tiff *.jfif)")
        fileimg = openFileDialog[0]

        # fileimg = os.getcwd() + "/Dots.png"
        #use full ABSOLUTE path to the image, not relative
        self.imageMain = self.findChild(QtWidgets.QLabel, 'image_Loaded')
        self.img = cv2.imread(fileimg,cv2.IMREAD_UNCHANGED)

        self.imageMain.setPixmap(self.rezizeandShow(self.img))
        self.drawHistogram_tab1(self.img)
        #img Asli tab 2
        self.asli2 = self.findChild(QtWidgets.QLabel, 'image_Asli')
        self.asli2.setPixmap(self.rezizeandShow(self.img))
        #img Asli tab 3
        self.asli_3_togrey = self.findChild(QtWidgets.QLabel, 'image_Asli_2')
        self.asli_3_togrey.setPixmap(self.rezizeandShow(self.getGreyVersion(self.img)))

        #img props
        self.imgProperties = self.findChild(QtWidgets.QTextEdit, 'txt_ImgProperties_2')
        self.imgProperties.setPlainText(f"filepath = {fileimg}\n"+ self.getImageProperties(self.img))

        #img val
        self.imgValues = self.findChild(QtWidgets.QTextEdit, 'txt_PixelValue_2')
        self.imgValues.setPlainText(self.getPixelValue(self.img))

    #### TAB 1 Func
    def getImageProperties(self,img):
        try:
            ax,yx,color_depth = img.shape
        except:
            ax,yx = img.shape
            color_depth = 1

        textout = f"shape = {img.shape}\n"
        textout += f"ax = {ax}\n"
        textout += f"yx = {yx}\n"
        textout += f"color depth = {color_depth}\n"
        # print(f"{img[0][0]} image type = {img[0][0].dtype}")
        textout += f"pixel depth = {self.getPixelDepth(img[0][0].dtype)}\n"
        # print(textout)
        return textout

    def getPixelDepth(self,type):
        if(type == np.uint8):
            return "8-bit/pixel"
        elif(type == np.uint16):
            return "16-bit/pixel"
        else:
            return "more than 16-bit/pixel"


    def getPixelValue(self,img):
        try:
            ax,yx,color_depth = img.shape
        except:
            ax,yx = img.shape
            color_depth = 1

        textout = ""
        if(ax>50 or yx>50):
            for i in range(50):
                for j in range(50):
                    pixel_value = img[i][j]
                    textout += f"{i}, {j} : {pixel_value} \n"
                    # print(pixel_value)
        else:
            for i in range(ax):
                for j in range(yx):
                    pixel_value = img[i][j]
                    textout += f"{i}, {j} : {pixel_value} \n"
                    # print(pixel_value)

        return textout

    #### TAB 2 Func
    def Negatemeh(self):
        piximg = self.img.copy()
        piximg = self.getNegasi(piximg)
        #img Hasil tab 2
        self.hasil = self.findChild(QtWidgets.QLabel, 'image_Hasil')
        self.hasil.setPixmap(self.rezizeandShow(piximg))
        self.drawHistogram_tab2(piximg)

    def Kembanginmeh(self):
        piximg = self.img.copy()
        piximg = self.getPengembangan(piximg,thershold = 200)
        #img Hasil tab 2
        self.hasil = self.findChild(QtWidgets.QLabel, 'image_Hasil')
        self.hasil.setPixmap(self.rezizeandShow(piximg))
        self.drawHistogram_tab2(piximg)

    def MirrormehHorizontally(self):
        piximg = self.img.copy()
        piximg = self.getMirrorHorizontal(piximg)
        #img Hasil tab 2
        self.hasil = self.findChild(QtWidgets.QLabel, 'image_Hasil')
        self.hasil.setPixmap(self.rezizeandShow(piximg))
        self.drawHistogram_tab2(piximg)

    def MirrormehVertically(self):
        piximg = self.img.copy()
        piximg = self.getMirrorVertikal(piximg)
        #img Hasil tab 2
        self.hasil = self.findChild(QtWidgets.QLabel, 'image_Hasil')
        self.hasil.setPixmap(self.rezizeandShow(piximg))
        self.drawHistogram_tab2(piximg)

    def MirrormehEmmYea(self):
        piximg = self.img.copy()
        piximg = self.getMirrorCampuran(piximg)
        #img Hasil tab 2
        self.hasil = self.findChild(QtWidgets.QLabel, 'image_Hasil')
        self.hasil.setPixmap(self.rezizeandShow(piximg))
        self.drawHistogram_tab2(piximg)

    #### TAB 3 Func
    def Convolusi(self):
        piximg = self.img.copy()
        piximg = self.getGreyVersion(piximg)
        w=np.asarray([[-1,-1,-1],
                      [-1,8,-1],
                      [-1,-1,-1]])
        piximg = cv2.filter2D(piximg, -1, w, borderType=cv2.BORDER_CONSTANT)
        #img Hasil tab 2
        self.hasil = self.findChild(QtWidgets.QLabel, 'image_Convolution')
        self.hasil.setPixmap(self.rezizeandShow(piximg))
        self.drawHistogram_tab3(piximg)
    
    def Dilate(self):
        self.txt_iterasi = self.findChild(QtWidgets.QTextEdit, 'txt_tab3_iterasi')

        try:
            self.txt_iterasi = self.findChild(QtWidgets.QTextEdit, 'txt_tab3_iterasi')
            print(self.txt_iterasi.text())
            # iterations = self.txt_iterasi.text()
            iterations = 5
        except:
            iterations = 5

        piximg = self.img.copy()
        invert = True

        if(invert == True):
            piximg = ~piximg
        piximg = self.getGreyVersion(piximg)
        w=np.array([[0,1,0],
                    [1,1,1],
                    [0,1,0]], dtype=np.uint8)
        piximg =  cv2.dilate(piximg, w,iterations = 5)
        if(invert == True):
            piximg = ~piximg
        #img Hasil tab 2
        self.hasil = self.findChild(QtWidgets.QLabel, 'image_Convolution')
        self.hasil.setPixmap(self.rezizeandShow(piximg))
        self.drawHistogram_tab3(piximg)
        
    def Erode(self):
        #todo buat radio button invert
        invert = True

        piximg = self.img.copy()
        if(invert == True):
            piximg = ~piximg
        piximg = self.getGreyVersion(piximg)
        w=np.array([[0,1,0],
                    [1,1,1],
                    [0,1,0]], dtype=np.uint8)
        piximg =  cv2.erode(piximg,w,iterations = 5)
        if(invert == True):
            piximg = ~piximg
        #img Hasil tab 2
        self.hasil = self.findChild(QtWidgets.QLabel, 'image_Convolution')
        self.hasil.setPixmap(self.rezizeandShow(piximg))
        self.drawHistogram_tab3(piximg)


    #################################################### helper func
    # resize main
    def rezizeandShow(self,img):
        img_temp = img.copy()
        try:
            y,x,color = img_temp.shape
        except:
            y,x = img.shape
            color = 1
        
        bytesPerLine = 3 * x
        if(color== 1):
            _pmap = QImage(img_temp, x, y, x, QImage.Format_Grayscale8)
        else:
            _pmap = QImage(img_temp, x, y, bytesPerLine, QImage.Format_RGB888)
        
        
        _pmap = QPixmap(_pmap)
        
       
        if(x==360 and y==240):
            imgresized = _pmap.scaled(360, 240, QtCore.Qt.KeepAspectRatio)
        else:
            imgresized = _pmap.scaled(360, 240, QtCore.Qt.KeepAspectRatio)

        # test = _pmap.toImage()
        # test.pixel(0,0)
        # for i in range(y):
        #     for j in range(x):
        #         print(f"{i,j} : {QtGui.qRed(test.pixel(i,j))},{QtGui.qGreen(test.pixel(i,j))},{QtGui.qBlue(test.pixel(i,j))}")

        
        
        return imgresized

    def getGreyVersion(self,img):
        grey = img.copy()
        try:
            ax,yx,color_depth = grey.shape
        except:
            ax,yx = grey.shape
            color_depth = 1
        if(color_depth >1):
            grey = cv2.cvtColor(grey, cv2.COLOR_BGR2GRAY)
        return grey


    def getNegasi(self,img):
        negasi = img.copy()
        try:
            ax,yx,color_depth = negasi.shape
        except:
            ax,yx = negasi.shape
            color_depth = 1

        if(color_depth==1):
            for x in range(ax):
                for y in range(yx):
                    for color in range(color_depth):
                        negasi[x][y] = 255-negasi[x][y]
        elif(color_depth!=1):
            for x in range(ax):
                for y in range(yx):
                    for color in range(color_depth):
                        negasi[x][y][color] = 255-negasi[x][y][color]
        return negasi
    
    def getPengembangan(self,img,thershold):
        pengembangan = img.copy()
        try:
            ax,yx,color_depth = pengembangan.shape
        except:
            ax,yx = pengembangan.shape
            color_depth = 1

        if(color_depth==1):
            for x in range(ax):
                for y in range(yx):
                    for color in range(color_depth):
                        if(pengembangan[x][y]<thershold):
                            pengembangan[x][y] = 0
                        else:
                            pengembangan[x][y] = 255
        else:
            for x in range(ax):
                for y in range(yx):
                    for color in range(color_depth):
                        if(pengembangan[x][y][color]<thershold):
                            pengembangan[x][y][color] = 0
                        else:
                            pengembangan[x][y][color] = 255

        # pengembangan[x][y][color]
        return pengembangan

    def getMirrorHorizontal(self,img):
        flip = img.copy()
        try:
            ax,yx,color_depth = flip.shape
        except:
            ax,yx = flip.shape
            color_depth = 1
        
        if(color_depth==1):
            for x in range(ax):
                for y in range(yx):
                    for color in range(color_depth):
                        flip[x][y]= img[x][yx-1-y]
        else:
            for x in range(ax):
                for y in range(yx):
                    for color in range(color_depth):
                        flip[x][y][color] = img[x][yx-1-y][color]

        return flip
    

    def getMirrorVertikal(self,img):
        flip = img.copy()
        try:
            ax,yx,color_depth = flip.shape
        except:
            ax,yx = flip.shape
            color_depth = 1
        
        if(color_depth==1):
            for x in range(ax):
                for y in range(yx):
                    for color in range(color_depth):
                        _temp = flip[x][y]
                        flip[x][y]= img[ax-1-x][y]
        else:
            for x in range(ax):
                for y in range(yx):
                    for color in range(color_depth):
                        _temp = flip[x][y][color]
                        flip[x][y][color] = img[ax-1-x][y][color]

        return flip

    def getMirrorCampuran(self,img):
        mirror = self.getMirrorHorizontal(img)
        mirror = self.getMirrorVertikal(mirror)
        return mirror


    def drawHistogram_tab3(self,img):
        read_img = img.copy()

        try:
            ax,yx,color_depth = read_img.shape
        except:
            ax,yx = read_img.shape
            color_depth = 1


        if(color_depth==1):
            # clean other Histogram
            self.Red_Histogram_3.canvas.axes.clear()
            self.Red_Histogram_3.canvas.draw()
            self.Blue_Histogram_3.canvas.axes.clear()
            self.Blue_Histogram_3.canvas.draw()

            self.Green_Histogram_3.canvas.axes.clear()
            histr = cv2.calcHist(read_img,[0],None,[256],[0,256])
            self.Green_Histogram_3.canvas.axes.plot(histr,color = 'k',linewidth=3.0)
            self.Green_Histogram_3.canvas.axes.set_ylabel('Y', color='black')
            self.Green_Histogram_3.canvas.axes.set_xlabel('X', color='black')
            self.Green_Histogram_3.canvas.axes.set_title('Greyscale Histogram')
            self.Green_Histogram_3.canvas.axes.set_facecolor('xkcd:wheat')
            self.Green_Histogram_3.canvas.axes.grid()
            self.Green_Histogram_3.canvas.draw()
        else:
            self.Red_Histogram_3.canvas.axes.clear()
            histr = cv2.calcHist(read_img,[0],None,[256],[0,256])
            self.Red_Histogram_3.canvas.axes.plot(histr,color = 'r',linewidth=3.0)
            self.Red_Histogram_3.canvas.axes.set_ylabel('Y', color='red')
            self.Red_Histogram_3.canvas.axes.set_xlabel('X', color='red')
            self.Red_Histogram_3.canvas.axes.set_title('Red_Histogram')
            self.Red_Histogram_3.canvas.axes.set_facecolor('xkcd:wheat')
            self.Red_Histogram_3.canvas.axes.grid()
            self.Red_Histogram_3.canvas.draw()

            self.Green_Histogram_3.canvas.axes.clear()
            histr = cv2.calcHist(read_img,[1],None,[256],[0,256])
            self.Green_Histogram_3.canvas.axes.plot(histr,color = 'g',linewidth=3.0)
            self.Green_Histogram_3.canvas.axes.set_ylabel('Y', color='green')
            self.Green_Histogram_3.canvas.axes.set_xlabel('X', color='green')
            self.Green_Histogram_3.canvas.axes.set_title('Green_Histogram')
            self.Green_Histogram_3.canvas.axes.set_facecolor('xkcd:wheat')
            self.Green_Histogram_3.canvas.axes.grid()
            self.Green_Histogram_3.canvas.draw()

            self.Blue_Histogram_3.canvas.axes.clear()
            histr = cv2.calcHist(read_img,[2],None,[256],[0,256])
            self.Blue_Histogram_3.canvas.axes.plot(histr,color = "b",linewidth=3.0)
            self.Blue_Histogram_3.canvas.axes.set_ylabel('Y', color='blue')
            self.Blue_Histogram_3.canvas.axes.set_xlabel('X', color='blue')
            self.Blue_Histogram_3.canvas.axes.set_title('Blue_Histogram')
            self.Blue_Histogram_3.canvas.axes.set_facecolor('xkcd:wheat')
            self.Blue_Histogram_3.canvas.axes.grid()
            self.Blue_Histogram_3.canvas.draw()

    def drawHistogram_tab2(self,img):
        read_img = img.copy()

        try:
            ax,yx,color_depth = read_img.shape
        except:
            ax,yx = read_img.shape
            color_depth = 1

        if(color_depth==1):
            # clean other Histogram
            self.Red_Histogram_2.canvas.axes.clear()
            self.Red_Histogram_2.canvas.draw()
            self.Blue_Histogram_2.canvas.axes.clear()
            self.Blue_Histogram_2.canvas.draw()

            self.Green_Histogram_2.canvas.axes.clear()
            histr = cv2.calcHist(read_img,[0],None,[256],[0,256])
            self.Green_Histogram_2.canvas.axes.plot(histr,color = 'k',linewidth=3.0)
            self.Green_Histogram_2.canvas.axes.set_ylabel('Y', color='black')
            self.Green_Histogram_2.canvas.axes.set_xlabel('X', color='black')
            self.Green_Histogram_2.canvas.axes.set_title('Greyscale Histogram')
            self.Green_Histogram_2.canvas.axes.set_facecolor('xkcd:wheat')
            self.Green_Histogram_2.canvas.axes.grid()
            self.Green_Histogram_2.canvas.draw()
        else:
            self.Red_Histogram_2.canvas.axes.clear()
            histr = cv2.calcHist(read_img,[0],None,[256],[0,256])
            self.Red_Histogram_2.canvas.axes.plot(histr,color = 'r',linewidth=3.0)
            self.Red_Histogram_2.canvas.axes.set_ylabel('Y', color='red')
            self.Red_Histogram_2.canvas.axes.set_xlabel('X', color='red')
            self.Red_Histogram_2.canvas.axes.set_title('Red_Histogram')
            self.Red_Histogram_2.canvas.axes.set_facecolor('xkcd:wheat')
            self.Red_Histogram_2.canvas.axes.grid()
            self.Red_Histogram_2.canvas.draw()

            self.Green_Histogram_2.canvas.axes.clear()
            histr = cv2.calcHist(read_img,[1],None,[256],[0,256])
            self.Green_Histogram_2.canvas.axes.plot(histr,color = 'g',linewidth=3.0)
            self.Green_Histogram_2.canvas.axes.set_ylabel('Y', color='green')
            self.Green_Histogram_2.canvas.axes.set_xlabel('X', color='green')
            self.Green_Histogram_2.canvas.axes.set_title('Green_Histogram')
            self.Green_Histogram_2.canvas.axes.set_facecolor('xkcd:wheat')
            self.Green_Histogram_2.canvas.axes.grid()
            self.Green_Histogram_2.canvas.draw()

            self.Blue_Histogram_2.canvas.axes.clear()
            histr = cv2.calcHist(read_img,[2],None,[256],[0,256])
            self.Blue_Histogram_2.canvas.axes.plot(histr,color = "b",linewidth=3.0)
            self.Blue_Histogram_2.canvas.axes.set_ylabel('Y', color='blue')
            self.Blue_Histogram_2.canvas.axes.set_xlabel('X', color='blue')
            self.Blue_Histogram_2.canvas.axes.set_title('Blue_Histogram')
            self.Blue_Histogram_2.canvas.axes.set_facecolor('xkcd:wheat')
            self.Blue_Histogram_2.canvas.axes.grid()
            self.Blue_Histogram_2.canvas.draw()

        print("histogram")
        print(read_img)
        print(f"histogram size : {read_img[0][0]}")
    
    def drawHistogram_tab1(self,img):
        read_img = img.copy()

        try:
            ax,yx,color_depth = read_img.shape
        except:
            ax,yx = read_img.shape
            color_depth = 1

        if(color_depth==1):
            # clean other Histogram
            self.Red_Histogram.canvas.axes.clear()
            self.Red_Histogram.canvas.draw()
            self.Blue_Histogram.canvas.axes.clear()
            self.Blue_Histogram.canvas.draw()

            self.Histogram.canvas.axes.clear()
            histr = cv2.calcHist(read_img,[0],None,[256],[0,256])
            self.Histogram.canvas.axes.plot(histr,color = 'k',linewidth=3.0)
            self.Histogram.canvas.axes.set_ylabel('Y', color='black')
            self.Histogram.canvas.axes.set_xlabel('X', color='black')
            self.Histogram.canvas.axes.set_title('Greyscale Histogram')
            self.Histogram.canvas.axes.set_facecolor('xkcd:wheat')
            self.Histogram.canvas.axes.grid()
            self.Histogram.canvas.draw()
        else:
            self.Red_Histogram.canvas.axes.clear()
            histr = cv2.calcHist(read_img,[0],None,[256],[0,256])
            self.Red_Histogram.canvas.axes.plot(histr,color = 'r',linewidth=3.0)
            self.Red_Histogram.canvas.axes.set_ylabel('Y', color='red')
            self.Red_Histogram.canvas.axes.set_xlabel('X', color='red')
            self.Red_Histogram.canvas.axes.set_title('Red_Histogram')
            self.Red_Histogram.canvas.axes.set_facecolor('xkcd:wheat')
            self.Red_Histogram.canvas.axes.grid()
            self.Red_Histogram.canvas.draw()

            self.Histogram.canvas.axes.clear()
            histr = cv2.calcHist(read_img,[1],None,[256],[0,256])
            self.Histogram.canvas.axes.plot(histr,color = 'g',linewidth=3.0)
            self.Histogram.canvas.axes.set_ylabel('Y', color='green')
            self.Histogram.canvas.axes.set_xlabel('X', color='green')
            self.Histogram.canvas.axes.set_title('Green_Histogram')
            self.Histogram.canvas.axes.set_facecolor('xkcd:wheat')
            self.Histogram.canvas.axes.grid()
            self.Histogram.canvas.draw()

            self.Blue_Histogram.canvas.axes.clear()
            histr = cv2.calcHist(read_img,[2],None,[256],[0,256])
            self.Blue_Histogram.canvas.axes.plot(histr,color = "b",linewidth=3.0)
            self.Blue_Histogram.canvas.axes.set_ylabel('Y', color='blue')
            self.Blue_Histogram.canvas.axes.set_xlabel('X', color='blue')
            self.Blue_Histogram.canvas.axes.set_title('Blue_Histogram')
            self.Blue_Histogram.canvas.axes.set_facecolor('xkcd:wheat')
            self.Blue_Histogram.canvas.axes.grid()
            self.Blue_Histogram.canvas.draw()




    
        

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
# 5. Run your application's event loop (or main loop)
sys.exit(app.exec_())