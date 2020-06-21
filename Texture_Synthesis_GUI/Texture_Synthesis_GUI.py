
from PIL import Image
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt, QFile, QTextStream
import threading
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import QtWidgets
import ctypes
import numpy as np
# import tensorflow as tf
import tensorflow.contrib.eager as tf
import time
import numpy as np
import math
from skimage import io, util
import heapq
import css
import os
import sys
global count
count=0

class main_window_gui(QWidget):
    def __init__(self, parent=None):
        super(main_window_gui, self).__init__(parent)
        # init the initial parameters of this GUI
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        self.title = 'Texture Synethsis'
        self.width = w
        self.height = h
        self.initUI()

    #Exit all the program
    def closeEvent(self, QCloseEvent):
            os._exit(0)

    def initUI(self):
        file = QFile(':css/StyleSheet.css')
        file.open(QFile.ReadOnly)
        stream = QTextStream(file)
        text = stream.readAll()
        self.setStyleSheet(text)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(":css/Icons/logo.png"))
        self.setGeometry(0, 0, self.width, self.height-60)

        #Creating main frame,it is a container for the all framers. parent it to QWindow
        self.main_frame = QtWidgets.QFrame(self)
        self.main_frame.setObjectName("MainFrame")
        self.main_frame.setFixedWidth(self.width)
        self.main_frame.setFixedHeight(self.height)
        self.main_layout = QtWidgets.QVBoxLayout(self.main_frame)

        # the Icons sub frame
        self.iconsub_frame = QtWidgets.QFrame(self.main_frame)
        self.iconsub_frame.setFixedHeight(80)
        self.main_layout.addWidget(self.iconsub_frame)
        self.iconsub_layout = QtWidgets.QHBoxLayout(self.iconsub_frame)
        self.iconsub_layout.setAlignment(Qt.AlignLeft)


        # the Icon sub frame
        self.logo_sub_frame = QtWidgets.QFrame(self.main_frame)
        self.logo_sub_frame.setFixedWidth(self.width)
        self.main_layout.addWidget(self.logo_sub_frame)
        self.logosub_layout = QtWidgets.QHBoxLayout(self.logo_sub_frame)
        self.logosub_layout.setAlignment(Qt.AlignCenter)

        # Setting up the logo
        logo = QtWidgets.QLabel('', self)
        pixmap = QPixmap(":css/Icons/logo.png")
        pixmap = pixmap.scaled(260, 260)
        logo.setPixmap(pixmap)
        self.logosub_layout.addWidget(logo)
        logo.setAlignment(Qt.AlignCenter)

        # The Button sub frame
        self.button_sub_frame = QtWidgets.QFrame(self.main_frame)
        self.main_layout.addWidget(self.button_sub_frame)
        self.button_sub_layout = QtWidgets.QHBoxLayout(self.button_sub_frame)
        self.button_sub_frame.setFixedWidth(self.width)
        self.button_sub_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        StartCreateNewBtn = QtWidgets.QPushButton("Click here : Texture Synthesis", self)
        StartCreateNewBtn.setObjectName("MainGuiButtons")
        StartCreateNewBtn.setToolTip('Start image style process.')
        StartCreateNewBtn.clicked.connect(self.openTextureImageGui)
        self.button_sub_layout.addWidget(StartCreateNewBtn)
        self.showMaximized()

    def openTextureImageGui(self):
        textureImage = TextureImageGui(self)
        textureImage.show()
        self.main_frame.setVisible(False)

class TextureImageGui(QWidget):
    def __init__(self, parent=None):
        super(TextureImageGui, self).__init__(parent)

        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        self.title = 'Texture Synethsis'
        self.width = w
        self.height = h
        self.initUI2()
        self.t = None  
    
    def initUI2(self):
        global flag_content_image
        flag_content_image = 0
        global flag_style_image
        flag_style_image = 0
        global flag_finish_generate
        flag_finish_generate = 0

        file = QFile(':css/StyleSheet.css')
        file.open(QFile.ReadOnly)
        stream = QTextStream(file)
        text = stream.readAll()
        self.setStyleSheet(text)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(":css/Icons/logo.png"))
        self.setGeometry(0, 0, self.width, self.height - 60)

        # Creating main container-frame, parent it to QWindow
        self.main_frame = QtWidgets.QFrame(self)
        self.main_frame.setObjectName("MainFrame")
        self.main_frame.setFixedWidth(self.width)
        self.main_frame.setFixedHeight(self.height)
        # the first sub window
        self.main_layout = QtWidgets.QVBoxLayout(self.main_frame)

        # the Icons sub frame
        self.iconsub_frame = QtWidgets.QFrame(self.main_frame)
        self.iconsub_frame.setFixedHeight(80)
        self.main_layout.addWidget(self.iconsub_frame)
        self.iconsub_layout = QtWidgets.QHBoxLayout(self.iconsub_frame)
        self.iconsub_layout.setAlignment(Qt.AlignLeft)

        # home button
        home_btn = QtWidgets.QPushButton("", self)
        home_btn.setObjectName("TransparentButtons")
        home_btn.setStyleSheet("QPushButton {background: url(:css/Icons/home.png) no-repeat transparent;} ")
        home_btn.setFixedWidth(68)
        home_btn.setFixedHeight(68)
        home_btn.setToolTip('Return home screen.')
        home_btn.clicked.connect(self.show_home)
        self.iconsub_layout.addWidget(home_btn)

        self.buttonsSub_Frame = QtWidgets.QFrame(self.main_frame)
        self.buttonsSub_Frame.setFixedWidth(self.width)
        self.buttonsSub_Frame.setFixedHeight(100)
        self.main_layout.addWidget(self.buttonsSub_Frame)
        self.buttonsSub_Layout = QtWidgets.QHBoxLayout(self.buttonsSub_Frame)
        self.buttonsSub_Layout.setAlignment(Qt.AlignCenter|Qt.AlignTop)

        QtCore.QMetaObject.connectSlotsByName(main)

        # upload content button
        contentBtn = QtWidgets.QPushButton("Upload image", self)
        contentBtn.setObjectName("MainGuiButtons")
        contentBtn.setToolTip('Upload image.')
        contentBtn.clicked.connect(self.set_content_image)
        self.buttonsSub_Layout.addWidget(contentBtn)

        #framer for the uploaded content and style images
        self.photosframe = QtWidgets.QFrame(self.main_frame)
        self.photosframe.setFixedWidth(self.width)
        self.main_layout.addWidget(self.photosframe)
        self.photosSub_Layout = QtWidgets.QHBoxLayout(self.photosframe)
        self.photosSub_Layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        #lable for  the content image
        self.contentLabel = QtWidgets.QLabel('', self)
        pixmap = QPixmap(":css/Icons/imageNeedUpload.png")
        pixmap = pixmap.scaled(256, 256)
        self.contentLabel.setPixmap(pixmap)
        self.photosSub_Layout.addWidget(self.contentLabel)
        self.contentLabel.setAlignment(Qt.AlignCenter)

        self.details_Frame = QtWidgets.QFrame(self.main_frame)
        self.details_Frame.setFixedWidth(self.width)
        self.details_Frame.setFixedHeight(60)
        self.main_layout.addWidget(self.details_Frame)
        self.details_Layout = QtWidgets.QHBoxLayout(self.details_Frame)
        self.details_Layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        self.generateBtnSub_Frame = QtWidgets.QFrame(self.main_frame)
        self.generateBtnSub_Frame.setFixedWidth(self.width)
        self.main_layout.addWidget(self.generateBtnSub_Frame)
        self.generateBtnSub_Layout = QtWidgets.QHBoxLayout(self.generateBtnSub_Frame)
        self.generateBtnSub_Layout.setAlignment(Qt.AlignCenter)

        self.generateBtn = QtWidgets.QPushButton("Generate", self)
        self.generateBtn.setToolTip('Generate image.')
        self.generateBtn.setObjectName("MainGuiButtons")
        self.generateBtn.clicked.connect(self.start_thread)
        self.generateBtnSub_Layout.addWidget(self.generateBtn)
        self.generateBtn.setEnabled(True)
       
    def start_thread(self):
        outputWindow = output_textureGui(self)
        self.t = threading.Thread(target=outputWindow.generate)
        #start the thread
        self.t.start()
        outputWindow.show()
        self.main_frame.setVisible(False)

    # Opens home window
    def show_home(self):
        
        home = main_window_gui(self)
        home.show()
        self.main_frame.setVisible(False)

    def set_content_image(self):
        fileName, _ = QtWidgets.QFileDialog.getOpenFileNames(None, "Select Image", "",
                                                             "Image Files (*.png *.jpg *.jpeg *.bmp)")
        if fileName:
            global content_path
            content_path = fileName[0]
            global flag_content_image
            flag_content_image = 1
            try:
                img = Image.open(content_path)  # open the image file
                img.verify()  # verify that it is, in fact an image
                pixmap = QtGui.QPixmap(fileName[0])
                pixmap = pixmap.scaled(256, 256)
                self.contentLabel.setPixmap(pixmap)
            except (IOError, SyntaxError) as e:
                flag_content_image = 0
                pixmap = QPixmap(":css/Icons/imageNeedUpload.png")
                pixmap = pixmap.scaled(256, 256)
                self.contentLabel.setPixmap(pixmap)
                QMessageBox.critical(self, "Error", "Image is corrupted, please upload a good image." )

class output_textureGui(QWidget):
    def __init__(self , parent=None):
        super(output_textureGui, self).__init__(parent)
        self.show
        # init the initial parameters of this GUI
        user32 = ctypes.windll.user32
        user32.SetProcessDPIAware()
        [w, h] = [user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)]
        self.title = 'Texture Synethsis'
        self.width = w
        self.height = h
        self.initUI()

    def initUI(self):
        file = QFile(':css/StyleSheet.css')
        file.open(QFile.ReadOnly)
        stream = QTextStream(file)
        text = stream.readAll()
        self.setStyleSheet(text)
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon(":css/Icons/logo.png"))
        self.setGeometry(0, 0, self.width, self.height - 60)

        # Creating main container-frame, parent it to QWindow
        self.main_frame = QtWidgets.QFrame(self)
        self.main_frame.setObjectName("MainFrame")
        self.main_frame.setFixedWidth(self.width)
        self.main_frame.setFixedHeight(self.height)
        self.main_layout = QtWidgets.QVBoxLayout(self.main_frame)

        # the Icons sub frame
        self.iconsub_frame = QtWidgets.QFrame(self.main_frame)
        self.iconsub_frame.setFixedHeight(80)
        self.main_layout.addWidget(self.iconsub_frame)
        self.iconsub_layout = QtWidgets.QHBoxLayout(self.iconsub_frame)
        self.iconsub_layout.setAlignment(Qt.AlignLeft)

        # home button
        self.home_btn = QtWidgets.QPushButton("", self)
        self.home_btn.setObjectName("TransparentButtons")
        self.home_btn.setStyleSheet("QPushButton {background: url(:css/Icons/home.png) no-repeat transparent;} ")
        self.home_btn.setFixedWidth(68)
        self.home_btn.setFixedHeight(68)
        self.home_btn.clicked.connect(self.show_home)
        self.iconsub_layout.addWidget(self.home_btn)
        self.home_btn.setToolTip('Return home screen.')

        # The output image sub frame
        self.output_sub_frame = QtWidgets.QFrame(self.main_frame)
        self.main_layout.addWidget(self.output_sub_frame)
        self.output_sub_layout = QtWidgets.QVBoxLayout(self.output_sub_frame)
        self.output_sub_frame.setFixedWidth(self.width)
        self.output_sub_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        self.output_frame = QtWidgets.QLabel(self.main_frame)
        self.output_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.output_frame.setText("")
        self.output_frame.setScaledContents(True)
        self.output_frame.setObjectName("output_frame")
        self.output_frame.setAlignment(Qt.AlignCenter)
        self.output_sub_layout.addWidget(self.output_frame)

        # The progressBar sub frame
        self.progressBar_sub_frame = QtWidgets.QFrame(self.main_frame)
        self.main_layout.addWidget(self.progressBar_sub_frame)
        self.progressBar_sub_frame.setFixedWidth(self.width)
        self.progressBar_sub_layout = QtWidgets.QHBoxLayout(self.progressBar_sub_frame)
        self.progressBar_sub_layout.setAlignment(Qt.AlignCenter)

        self.progressBar = QtWidgets.QProgressBar(self.main_frame)
        self.progressBar.setFixedWidth(self.width/3)
        self.progressBar.setProperty("value",0)
        self.progressBar.setMaximum(100)
        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setObjectName("progressBar")
        self.progressBar_sub_layout.addWidget(self.progressBar)

        # The Button save sub frame
        self.button_sub_frame = QtWidgets.QFrame(self.main_frame)
        self.main_layout.addWidget(self.button_sub_frame)
        self.button_sub_layout = QtWidgets.QVBoxLayout(self.button_sub_frame)
        self.button_sub_frame.setFixedWidth(self.width)
        self.button_sub_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        # Save button for the output image
        self.save_button = QtWidgets.QPushButton("Save your image", self)
        self.save_button.setObjectName("MainGuiButtons")
        self.save_button.clicked.connect(self.save_image)
        self.save_button.setToolTip('Save ouput image.')
        self.button_sub_layout.addWidget(self.save_button)

    def save_image(self):
        global output_image
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Select Image", "",
                                                            "Image Files (*.jpg *.png *.jpeg *.bmp)")
        if (file_name):
            output_image.save(file_name)

    def show_home(self):
        global flag_finish_generate
        if flag_finish_generate == 0:
            QMessageBox.critical(self, "Error", "You can not return home while process is running.")
        else:
            home = main_window_gui(self)
            home.show()
            self.main_frame.setVisible(False)

    def on_count_changed(self, value):
        self.progressBar.setValue(value)

    def generate(self):
        global output_image
        self.save_button.hide()
        # output_image get the result from the StyleMakerFunc.
        output_image = self.synth_texture(content_path, 50, (6, 6), "cut")
        pixmap = QtGui.QPixmap(output_image.toqpixmap())
        pixmap = pixmap.scaledToHeight(250)
        self.output_frame.setPixmap(pixmap)
        self.output_frame.setAlignment(QtCore.Qt.AlignCenter)
        self.output_frame.show()
        self.save_button.show()

        global flag_finish_generate
        flag_finish_generate = 1
        self.home_btn.setEnabled(True)
    
    def synth_texture(self, path_to_img, patchLength, numPatches, mode="cut", sequence=False):
        
        tf.enable_eager_execution()
        print("Eager execution: {}".format(tf.executing_eagerly()))

        # define calculation running step to the external thread.
        self.update_prograssBar_value = external_run_prograssBar_1()
        self.update_prograssBar_value.countChanged.connect(self.progressBar.setValue)
        
        def randomPatch(texture, patchLength):
            h, w, _ = texture.shape
            i = np.random.randint(h - patchLength)
            j = np.random.randint(w - patchLength)

            return texture[i:i+patchLength, j:j+patchLength]

        def L2OverlapDiff(patch, patchLength, overlap, res, y, x):
            error = 0
            if x > 0:
                left = patch[:, :overlap] - res[y:y+patchLength, x:x+overlap]
                error += np.sum(left**2)
            if y > 0:
                up   = patch[:overlap, :] - res[y:y+overlap, x:x+patchLength]
                error += np.sum(up**2)
            if x > 0 and y > 0:
                corner = patch[:overlap, :overlap] - res[y:y+overlap, x:x+overlap]
                error -= np.sum(corner**2)
            return error

        def randomBestPatch(texture, patchLength, overlap, res, y, x):
            h, w, _ = texture.shape
            errors = np.zeros((h - patchLength, w - patchLength))

            for i in range(h - patchLength):
                for j in range(w - patchLength):
                    patch = texture[i:i+patchLength, j:j+patchLength]
                    e = L2OverlapDiff(patch, patchLength, overlap, res, y, x)
                    errors[i, j] = e

            i, j = np.unravel_index(np.argmin(errors), errors.shape)
            return texture[i:i+patchLength, j:j+patchLength]

        def minCutPath(errors):
            # dijkstra's algorithm vertical
            pq = [(error, [i]) for i, error in enumerate(errors[0])]
            heapq.heapify(pq)
            h, w = errors.shape
            seen = set()
            while pq:
                error, path = heapq.heappop(pq)
                curDepth = len(path)
                curIndex = path[-1]
                if curDepth == h:
                    return path
                for delta in -1, 0, 1:
                    nextIndex = curIndex + delta
                    if 0 <= nextIndex < w:
                        if (curDepth, nextIndex) not in seen:
                            cumError = error + errors[curDepth, nextIndex]
                            heapq.heappush(pq, (cumError, path + [nextIndex]))
                            seen.add((curDepth, nextIndex))
        
        def minCutPatch(patch, patchLength, overlap, res, y, x):
            patch = patch.copy()
            dy, dx, _ = patch.shape
            minCut = np.zeros_like(patch, dtype=bool)
            if x > 0:
                left = patch[:, :overlap] - res[y:y+dy, x:x+overlap]
                leftL2 = np.sum(left**2, axis=2)
                for i, j in enumerate(minCutPath(leftL2)):
                    minCut[i, :j] = True
            if y > 0:
                up = patch[:overlap, :] - res[y:y+overlap, x:x+dx]
                upL2 = np.sum(up**2, axis=2)
                for j, i in enumerate(minCutPath(upL2.T)):
                    minCut[:i, j] = True
            np.copyto(patch, res[y:y+dy, x:x+dx], where=minCut)
            return patch
        
        texture = Image.open(path_to_img)
        texture = util.img_as_float(texture)
        overlap = patchLength // 6
        numPatchesHigh, numPatchesWide = numPatches
        h = (numPatchesHigh * patchLength) - (numPatchesHigh - 1) * overlap
        w = (numPatchesWide * patchLength) - (numPatchesWide - 1) * overlap
        res = np.zeros((h, w, texture.shape[2]))
        self.update_prograssBar_value.start()
        for i in range(numPatchesHigh):
            global count
            count=i
            self.update_prograssBar_value.start()
            print("Iteration: {}".format(i))
            for j in range(numPatchesWide):
                y = i * (patchLength - overlap)
                x = j * (patchLength - overlap)
                if i == 0 and j == 0 or mode == "random":
                    patch = randomPatch(texture, patchLength)
                elif mode == "best":
                    patch = randomBestPatch(texture, patchLength, overlap, res, y, x)
                elif mode == "cut":
                    patch = randomBestPatch(texture, patchLength, overlap, res, y, x)
                    patch = minCutPatch(patch, patchLength, overlap, res, y, x)
                res[y:y+patchLength, x:x+patchLength] = patch

        image = Image.fromarray((res * 255).astype(np.uint8))
        return image
        
class external_run_prograssBar_1(QThread):
    countChanged = pyqtSignal(int)
    def run(self):
        global count
        progressVal =((count + 1) / 6) * 100
        self.countChanged.emit(progressVal)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = main_window_gui()
    sys.exit(app.exec_())