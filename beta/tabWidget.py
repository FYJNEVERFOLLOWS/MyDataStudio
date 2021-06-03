import time
from functools import partial

from PyQt5 import sip
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import func1_tab
import func2_tab
import const
import comboCheckBox
import connect_mysql
import tableWidget

dbc = connect_mysql.myDBC()
combolist = const.COMBOLIST
comboDict = const.COMBODICT
colDict = const.COLDICT
sqlDict = const.SQLDICT

class MyDialog(QDialog):
    dragRelease = pyqtSignal(QPoint)
    # signal_doc = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.content = None
        # self.signal_doc.connect(self.refresh_dock_name)

    def set_content_widget(self, page: QWidget):
        if not page:
            return

        self.content = page
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(page)
        return

    def get_content_widget(self):
        return self.content

    def event(self, event):
        if event.type() == QEvent.NonClientAreaMouseButtonRelease:
            self.dragRelease.emit(QCursor.pos())
        return QDialog.event(self, event)


class MyTabBar(QTabBar):

    beginDragOut = pyqtSignal(int)
    beginDragIn = pyqtSignal(QEvent)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.theDragPress = False
        self.theDragOut = False

    def mousePressEvent(self, event):
        QTabBar.mousePressEvent(self, event)

        if event.button() == Qt.LeftButton and self.currentIndex() > 0:
            self.theDragPress = True
            # print('theDragPress')

    def mouseMoveEvent(self, event):
        QTabBar.mouseMoveEvent(self, event)

        if self.theDragPress and event.buttons():
            if not self.theDragOut and not self.contentsRect().contains(event.pos()):
                self.theDragOut = True
                # print('theDragOut')
                self.beginDragOut.emit(self.currentIndex())
                # QDrag.exec后就不会触发release了，自己手动触发
                # 不过他好像还是在鼠标弹起之后才会进行动画，待解决

                mouseEvent = QMouseEvent(QEvent.MouseButtonRelease,
                                               self.mapFromGlobal(QCursor.pos()),
                                               Qt.LeftButton, Qt.LeftButton, Qt.NoModifier)
                QApplication.postEvent(self, mouseEvent)

    def mouseReleaseEvent(self, event):
        QTabBar.mouseReleaseEvent(self, event)
        self.theDragPress = False
        self.theDragOut = False
        # print('mouseReleaseEvent')

class newTabWidget(QTabWidget):

    def __init__(self, func):
        super(newTabWidget, self).__init__()
        self.tab_bar = MyTabBar(self)
        self.init_tabBar()
        self.docker_id = 3


        self.fixedPages = []

        self.dockers = []
        self.tab_id_map = {0: 0, 1: 1, 2: 2} # key: docker_id, value: tab_id

        self.initUI(func)
        self.tabcnt = 3
        self.idx2tabid_dict = {0: 1, 1: 2, 2: 3}

    @property
    def tab_id_remap(self):
        return {v: k for k, v in self.tab_id_map.items()}

    def initUI(self, func):
        # 创建3个选项卡小控件窗口
        if func == 1:
            self.tab0 = func1_tab.newTab(0, "查询0", self)
            self.tab1 = func1_tab.newTab(1, "查询1", self)
            self.tab2 = func1_tab.newTab(2, "查询2", self)
            self.tab0.newTab_but.clicked.connect(self.newTab1UI)  # 新建按钮
            self.tab1.newTab_but.clicked.connect(self.newTab1UI)  # 新建按钮
            self.tab2.newTab_but.clicked.connect(self.newTab1UI)  # 新建按钮

        elif func == 2 :
            self.tab0 = func2_tab.newTab(0, "查询0", self)
            self.tab1 = func2_tab.newTab(1, "查询1", self)
            self.tab2 = func2_tab.newTab(2, "查询2", self)
            self.tab0.newTab_but.clicked.connect(self.newTab2UI)  # 新建按钮
            self.tab1.newTab_but.clicked.connect(self.newTab2UI)  # 新建按钮
            self.tab2.newTab_but.clicked.connect(self.newTab2UI)  # 新建按钮

        self.dockers.append(self.tab0)
        self.dockers.append(self.tab1)
        self.dockers.append(self.tab2)
        self.setTabPosition(QTabWidget.North)
        self.setTabsClosable(True)  # 设置标签页为可关闭
        self.tabCloseRequested.connect(self.close_tab)
        # 将三个选项卡添加到顶层窗口中
        self.addTab(self.tab0, "查询0")
        self.addTab(self.tab1, "查询1")
        self.addTab(self.tab2, "查询2")
        # self.currentChanged[int].connect(self.changeTabUI)
        self.setStyleSheet("QTabBar::tab { height: 30px; width: 100px; font: 14px}")
        # self.tabBarDoubleClicked.connect(self.newTabUI)
        self.tabBarDoubleClicked.connect(self.popWin)

        # add_btn = QPushButton("ADD_MARK")
        # add_btn.clicked.connect(self.add_tab)
        # self.tab_bar.setTabButton(0, QTabBar.RightSide, add_btn)
        # self.setTabEnabled(0, False)


    def init_tabBar(self):
        self.setTabBar(self.tab_bar)
        self.setMovable(True)
        # 点击页签上的关闭按钮时，触发信号
        self.tab_bar.setTabsClosable(True)
        self.tab_bar.tabCloseRequested.connect(self.close_tab)
        # 拖拽到外部 - 还未释放鼠标
        self.tab_bar.beginDragOut.connect(self.on_begin_dragout)

    def on_begin_dragout(self, index):
        drag_tab = self.widget(index)
        # 固定tab就不让拖出
        if not drag_tab or drag_tab in self.fixedPages:
            return

        # 把当前页作为快照拖拽
        # 尺寸加了标题栏和边框
        pixmap = QPixmap(drag_tab.size() + QSize(2, 31))
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)

        if painter.isActive():
            # 这里想做标题栏贴在内容之上
            # 但是没法获取默认标题栏的图像啊，就随便画一个矩形框
            # 如果设置了外部主题颜色，需要改下
            title_rect = QRect(0, 0, pixmap.width(), 30)
            painter.fillRect(title_rect, Qt.white)
            painter.drawText(title_rect, Qt.AlignLeft|Qt.AlignVCenter, " " + drag_tab.windowTitle())
            painter.drawRect(pixmap.rect())
        painter.end()
        drag_tab.render(pixmap, QPoint(1,30))

        mime = QMimeData()
        drag = QDrag(self.tab_bar)
        drag.setMimeData(mime)
        drag.setPixmap(pixmap)
        drag.setHotSpot(QPoint(10, 0))

        # 鼠标弹起后drag就释放了，这时候去判断是否拖拽到了外部
        drag.destroyed.connect(partial(self.on_drag_destroyed, drag_tab))
        drag.exec(Qt.MoveAction)

    def on_drag_destroyed(self, drag_tab, event):
        bar_point = self.tab_bar.mapFromGlobal(QCursor.pos())
        if not self.tab_bar.contentsRect().contains(bar_point):
            self.pop_page(drag_tab)

    def pop_page(self, docker):
        self.remove_tab(self.indexOf(docker))
        self.pop = MyDialog(self)
        self.pop.setAttribute(Qt.WA_DeleteOnClose)
        self.pop.set_content_widget(docker)
        self.pop.setWindowTitle(docker.docker_name)
        self.pop.resize(docker.size())
        # 拖出来的位置有点偏移
        self.pop.move(QCursor().pos() - QPoint(10, 10))

        # 判断独立窗口是否拖回tab
        self.pop.dragRelease.connect(partial(self.close_pop, self.pop))

        self.pop.show()
        docker.show()
        self.pop.activateWindow()
        self.pop.setFocus()

    def close_pop(self, pop, pos):
        bar_point = self.tab_bar.mapFromGlobal(pos)
        # 如果又拖回了tabbar范围内，就把widget取出来放回tab
        if self.tab_bar.contentsRect().contains(bar_point):
            docker = pop.get_content_widget()
            self.add_tab(docker)
            docker.refresh_parent(self)
            pop.disconnect()
            pop.close()

    def add_tab(self, docker=None):
        if not docker:
            docker_name = "查询%d" % self.docker_id
            docker = func1_tab.newTab(self.docker_id, docker_name, self)
        print(docker.docker_id)
        # docker = ScriptDocker(self.docker_id, docker_name, self)
        # docker = self.dockers[docker.docker_id]
        print(docker)
        self.addTab(docker, docker.docker_name)
        tab_id = self.indexOf(docker)
        self.tab_id_map[docker.docker_id] = tab_id
        self.setCurrentIndex(tab_id)
        self.dockers.append(docker)
        # self.docker_id += 1
        print("self.docker_id = {}".format(self.docker_id))


    def remove_tab(self, tab_id):
        docker_id = self.tab_id_remap[tab_id]
        print("docker_id= {}".format(docker_id))
        self.removeTab(tab_id)
        self.tab_id_map.pop(docker_id)
        self.refresh_dock_id()
        print(self.dockers)
        self.dockers.pop(docker_id)
        return

    def refresh_dock_id(self):
        self.tab_id_map = {docker_id: self.indexOf(self.dockers[docker_id])
                           for docker_id in self.tab_id_map.keys()}
        return

    # def refresh_dock_name(self, name_str):
    #     name, docker_id = name_str.split("LOG_MARK") # ?
    #     tab_id = self.tab_id_map.get(int(docker_id))
    #     if tab_id:
    #         self.setTabText(tab_id, name)
    #     return

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
        exec('self.tab{} = func1_tab.newTab({}, "查询{}", self)'.format(self.docker_id, self.docker_id, self.docker_id))
        exec('self.addTab(self.tab{}, "查询{}")'.format(self.docker_id, self.docker_id))
        exec('self.tab{}.newTab_but.clicked.connect(self.newTab1UI)'.format(self.docker_id))  # 查询按钮
        exec('tab_id = self.indexOf(self.tab{})'.format(self.docker_id))
        exec('self.tab_id_map[self.docker_id] = tab_id')
        exec('self.setCurrentIndex(tab_id)')
        exec('self.dockers.append(self.tab{})'.format(self.docker_id))
        self.docker_id += 1

    def newTab2UI(self):
        exec('self.tab{} = func2_tab.newTab({}, "查询{}", self)'.format(self.docker_id, self.docker_id, self.docker_id))
        exec('self.addTab(self.tab{}, "查询{}")'.format(self.docker_id, self.docker_id))
        exec('self.tab{}.newTab_but.clicked.connect(self.newTab2UI)'.format(self.docker_id))  # 查询按钮
        exec('tab_id = self.indexOf(self.tab{})'.format(self.docker_id))
        exec('self.tab_id_map[self.docker_id] = tab_id')
        exec('self.setCurrentIndex(tab_id)')
        exec('self.dockers.append(self.tab{})'.format(self.docker_id))
        self.docker_id += 1


    def close_tab(self, index):
        if self.count() == 1:
            # QCoreApplication.quit()
            self.close()
        else:
            self.removeTab(index)
            # after removingTab, the idx2tabid_dict shall change:
            self.refresh_dock_id()

        # for i in range(1, self.docker_id):
        #     flag = eval("hasattr(self.tab{}, 't')".format(i))
        #     if flag:
        #         exec('print(i, self.tab{}.t.isRunning())'.format(i))
        #         exec('self.tab{}.t.requestInterruption()'.format(i))
        #         time.sleep(2)
        #         exec('print(i, self.tab{}.t.isRunning())'.format(i))


