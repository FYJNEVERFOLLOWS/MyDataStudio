from PyQt5 import sip

from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *


import func1_tab
import func2_tab


class newTabWidget(QTabWidget):
    tabcnt = 3
    idx2tabid_dict = {0: 1, 1: 2, 2: 3}

    def __init__(self, func):
        super(newTabWidget, self).__init__()
        self.initUI(func)

    def initUI(self, func):
        # 创建3个选项卡小控件窗口
        if func == 1:
            self.tab1 = func1_tab.newTab()
            self.tab2 = func1_tab.newTab()
            self.tab3 = func1_tab.newTab()
            self.tab1.newTab_but.clicked.connect(self.newTab1UI)  # 新建按钮
            self.tab2.newTab_but.clicked.connect(self.newTab1UI)  # 新建按钮
            self.tab3.newTab_but.clicked.connect(self.newTab1UI)  # 新建按钮
        elif func == 2 :
            self.tab1 = func2_tab.newTab()
            self.tab2 = func2_tab.newTab()
            self.tab3 = func2_tab.newTab()
            self.tab1.newTab_but.clicked.connect(self.newTab2UI)  # 新建按钮
            self.tab2.newTab_but.clicked.connect(self.newTab2UI)  # 新建按钮
            self.tab3.newTab_but.clicked.connect(self.newTab2UI)  # 新建按钮

        # self.tab1.newTab_but.clicked.connect(lambda: self.newTabUI(func))  # 新建按钮
        # self.tab2.newTab_but.clicked.connect(lambda: self.newTabUI(func))  # 新建按钮
        # self.tab3.newTab_but.clicked.connect(lambda: self.newTabUI(func))  # 新建按钮
        # self.tab1.newTab_but.clicked.connect(self.newTabUI)  # 新建按钮
        # self.tab2.newTab_but.clicked.connect(self.newTabUI)  # 新建按钮
        # self.tab3.newTab_but.clicked.connect(self.newTabUI)  # 新建按钮

        self.setTabPosition(QTabWidget.North)
        self.setTabsClosable(True)  # 设置标签页为可关闭
        self.tabCloseRequested.connect(self.close_tab)
        # 将三个选项卡添加到顶层窗口中
        self.addTab(self.tab1, "查询1")
        self.addTab(self.tab2, "查询2")
        self.addTab(self.tab3, "查询3")
        # self.currentChanged[int].connect(self.changeTabUI)
        self.setStyleSheet("QTabBar::tab { height: 30px; width: 100px; font: 14px}")
        # self.tabBarDoubleClicked.connect(self.newTabUI)
        self.tabBarDoubleClicked.connect(self.popWin)

    def popWin(self, index):
        # 注：主窗口的槽函数不能直接使用局部变量创建弹出窗口，否则槽函数结束局部变量会结束生命周期导致弹出窗口消失，可以使用成员变量或应用变量。
        # exec('self.subwin{} = self.tab{}'.format(index + 1, index + 1))

        tabid = self.idx2tabid_dict[index]
        exec('self.tab{}.subwin = QWidget()'.format(tabid))
        exec('self.tab{}.subwin.setLayout(self.tab{}.tabLayout)'.format(tabid, tabid))

        exec("self.tab{}.subwin.setFont(QFont('宋体', 12))".format(tabid))
        # self.subwin.setStyleSheet("QLabel{font-size:12px;font-weight:bold;font-family:Simsun;}")
        exec("self.tab{}.subwin.setWindowTitle('查询{}')".format(tabid, tabid))

        exec("self.tab{}.subwin.resize(1280, 720)".format(tabid))
        exec("self.tab{}.subwin.show()".format(tabid))
        self.removeTab(index)

        # after removingTab, the idx2tabid_dict show change:
        for i in range(index, self.count()):
            self.idx2tabid_dict[i] = self.idx2tabid_dict[i + 1]
        self.idx2tabid_dict.pop(self.count())

    def newTab1UI(self):
        self.tabcnt += 1
        # self.addTab(tab.newTab(), "新建查询")
        exec('self.tab{} = func1_tab.newTab()'.format(self.tabcnt))
        exec('self.addTab(self.tab{}, "查询{}")'.format(self.tabcnt, self.tabcnt))
        exec('self.tab{}.newTab_but.clicked.connect(self.newTab1UI)'.format(self.tabcnt))  # 查询按钮
        self.idx2tabid_dict[self.count() - 1] = self.tabcnt

    def newTab2UI(self):
        self.tabcnt += 1
        # self.addTab(tab.newTab(), "新建查询")
        exec('self.tab{} = func2_tab.newTab()'.format(self.tabcnt))
        exec('self.addTab(self.tab{}, "查询{}")'.format(self.tabcnt, self.tabcnt))
        exec('self.tab{}.newTab_but.clicked.connect(self.newTab2UI)'.format(self.tabcnt))  # 查询按钮
        self.idx2tabid_dict[self.count() - 1] = self.tabcnt


    def close_tab(self, index):
        if self.count() == 1:
            # QCoreApplication.quit()
            self.close()
        else:
            self.removeTab(index)
            # after removingTab, the idx2tabid_dict show change:
            for i in range(index, self.count()):
                self.idx2tabid_dict[i] = self.idx2tabid_dict[i + 1]
            self.idx2tabid_dict.pop(self.count())