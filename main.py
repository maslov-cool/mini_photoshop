import io
import sys

from PyQt6 import uic  # Импортируем uic
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QPixmap, QImage, QTransform, QColor
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog

template = """<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>461</width>
    <height>429</height>
   </rect>
  </property>
  <property name="windowTitle">
   <string>PIL 2.0</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <widget class="QPushButton" name="pushButton">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>20</y>
      <width>101</width>
      <height>31</height>
     </rect>
    </property>
    <property name="text">
     <string>R</string>
    </property>
    <attribute name="buttonGroup">
     <string notr="true">channelButtons</string>
    </attribute>
   </widget>
   <widget class="QPushButton" name="pushButton_2">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>70</y>
      <width>101</width>
      <height>31</height>
     </rect>
    </property>
    <property name="text">
     <string>G</string>
    </property>
    <attribute name="buttonGroup">
     <string notr="true">channelButtons</string>
    </attribute>
   </widget>
   <widget class="QPushButton" name="pushButton_3">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>120</y>
      <width>101</width>
      <height>31</height>
     </rect>
    </property>
    <property name="text">
     <string>B</string>
    </property>
    <attribute name="buttonGroup">
     <string notr="true">channelButtons</string>
    </attribute>
   </widget>
   <widget class="QPushButton" name="pushButton_4">
    <property name="geometry">
     <rect>
      <x>10</x>
      <y>180</y>
      <width>101</width>
      <height>31</height>
     </rect>
    </property>
    <property name="text">
     <string>ALL</string>
    </property>
    <attribute name="buttonGroup">
     <string notr="true">channelButtons</string>
    </attribute>
   </widget>
   <widget class="QPushButton" name="pushButton_5">
    <property name="geometry">
     <rect>
      <x>30</x>
      <y>320</y>
      <width>171</width>
      <height>51</height>
     </rect>
    </property>
    <property name="text">
     <string>Против часовой стрелки</string>
    </property>
    <attribute name="buttonGroup">
     <string notr="true">rotateButtons</string>
    </attribute>
   </widget>
   <widget class="QPushButton" name="pushButton_6">
    <property name="geometry">
     <rect>
      <x>240</x>
      <y>320</y>
      <width>191</width>
      <height>51</height>
     </rect>
    </property>
    <property name="text">
     <string>По часовой стрелке</string>
    </property>
    <attribute name="buttonGroup">
     <string notr="true">rotateButtons</string>
    </attribute>
   </widget>
   <widget class="QLabel" name="curr_image">
    <property name="geometry">
     <rect>
      <x>120</x>
      <y>10</y>
      <width>311</width>
      <height>271</height>
     </rect>
    </property>
    <property name="text">
     <string/>
    </property>
    <property name="curr_image" stdset="0">
     <pixmap/>
    </property>
   </widget>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>461</width>
     <height>26</height>
    </rect>
   </property>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
 </widget>
 <resources/>
 <connections/>
 <buttongroups>
  <buttongroup name="channelButtons"/>
  <buttongroup name="rotateButtons"/>
 </buttongroups>
</ui>
"""


class MyPillow(QMainWindow):
    def __init__(self):
        super().__init__()
        f = io.StringIO(template)
        uic.loadUi(f, self)  # Загружаем дизайн

        self.initUI()

    def initUI(self):
        file_address = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        img_orig_and_now = [QImage(file_address) for _ in range(2)]
        self.curr_image.setPixmap(QPixmap(img_orig_and_now[0]))
        h, w = img_orig_and_now[0].size().height(), img_orig_and_now[0].size().width()

        self.pushButton.clicked.connect(lambda: self.red(h, w, img_orig_and_now))
        self.pushButton_2.clicked.connect(lambda: self.green(h, w, img_orig_and_now))
        self.pushButton_3.clicked.connect(lambda: self.blue(h, w, img_orig_and_now))
        self.pushButton_4.clicked.connect(lambda: self.orig(img_orig_and_now))
        self.pushButton_5.clicked.connect(lambda: self.against(img_orig_and_now))
        self.pushButton_6.clicked.connect(lambda: self.by(img_orig_and_now))

    def red(self, h, w, img):
        for i in range(h):
            for j in range(w):
                img[1].setPixelColor(QPoint(i, j), QColor(img[0].pixelColor(i, j).red(), 0, 0))
        self.curr_image.setPixmap(QPixmap.fromImage(img[1]))

    def green(self, h, w, img):
        for i in range(h):
            for j in range(w):
                img[1].setPixelColor(QPoint(i, j), QColor(0, img[0].pixelColor(i, j).green(), 0))
        self.curr_image.setPixmap(QPixmap.fromImage(img[1]))

    def blue(self, h, w, img):
        for i in range(h):
            for j in range(w):
                img[1].setPixelColor(QPoint(i, j), QColor(0, 0, img[0].pixelColor(i, j).blue()))
        self.curr_image.setPixmap(QPixmap.fromImage(img[1]))

    def orig(self, img):
        img[1] = img[0].copy()
        self.curr_image.setPixmap(QPixmap.fromImage(img[1]))

    def against(self, img):
        self.curr_image.setPixmap(QPixmap.fromImage(img[1].transformed(QTransform().rotate(-90))))
        img[0] = img[0].transformed(QTransform().rotate(-90))
        img[1] = img[1].transformed(QTransform().rotate(-90))

    def by(self, img):
        self.curr_image.setPixmap(QPixmap.fromImage(img[1].transformed(QTransform().rotate(90))))
        img[0] = img[0].transformed(QTransform().rotate(90))
        img[1] = img[1].transformed(QTransform().rotate(90))


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyPillow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
