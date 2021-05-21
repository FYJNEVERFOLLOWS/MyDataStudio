import sys
import time

from PyQt5 import sip
from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


import tabWidget

class MyMainWin(QMainWindow):
    def __init__(self, parent=None):
        super(MyMainWin, self).__init__(parent)
        self.initUI()

    def initUI(self):
        # self.toolbar = self.addToolBar('返回')
        self.setWindowTitle("数据查询软件（双击标签页可弹出此标签页）")
        self.resize(1600, 900)
        self.setFont(QFont('宋体', 12))
        # self.layout = QHBoxLayout()
        self.tabWidget1 = tabWidget.newTabWidget(1)
        self.tabWidget2 = tabWidget.newTabWidget(2)
        self.tabWidget1.setFont(QFont('宋体', 12))
        self.tabWidget2.setFont(QFont('宋体', 12))
        # self.tabWidget.setMaximumHeight(900)

        # self.layout.addWidget(self.tabWidget)

        self.topTabWidget = QTabWidget()
        self.topTabWidget.addTab(self.tabWidget1, "功能1") # tabwidget嵌套tabwidget
        self.topTabWidget.addTab(self.tabWidget2, "功能2") # tabwidget嵌套tabwidget
        # self.topTabWidget.addTab(QWidget(), "功能3") # tabwidget嵌套tabwidget
        self.topTabWidget.setTabPosition(QTabWidget.South) # 设置选项卡的显示位置为页面下方
        self.setCentralWidget(self.topTabWidget)


    def closeEvent(self, event):  # 重写closeEvent方法，实现主窗口关闭时关闭所有子窗口
        sys.stdout = sys.__stdout__
        for i in range(1, self.tabWidget1.tabcnt + 1):
            flag = eval("hasattr(self.tabWidget1.tab{}, 'subwin')".format(i))
            if flag:
                exec('self.tabWidget1.tab{}.subwin.close()'.format(i))
        for i in range(1, self.tabWidget2.tabcnt + 1):
            flag = eval("hasattr(self.tabWidget2.tab{}, 'subwin')".format(i))
            if flag:
                exec('self.tabWidget2.tab{}.subwin.close()'.format(i))

        #########################  kill the thread  ###########################
        for i in range(1, self.tabWidget2.tabcnt + 1):
            flag = eval("hasattr(self.tabWidget2.tab{}, 't')".format(i))
            if flag:
                exec('print(i, self.tabWidget2.tab{}.t.isRunning())'.format(i))
                runflag = eval("self.tabWidget2.tab{}.t.isRunning()".format(i))
                if runflag:
                    exec('self.tabWidget2.tab{}.t.requestInterruption()'.format(i))
                    time.sleep(5)
                exec('print(i, self.tabWidget2.tab{}.t.isRunning())'.format(i))
        #########################################################################




if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MyMainWin()
    mw.show()
    app.exec_()
