import subprocess
import time

from PyQt5 import sip

from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import *

import showSqlResult
import constant

combolist = constant.FUNC2_COMBOLIST
exec_combolist = ['main_1', 'main_2']
cmdlist = constant.CMDLIST
# cmdlist = [r"D:\FYJ\PyQt\QtLearning\venv\Scripts\python.exe D:\FYJ\PyQt\choice_data\test.py", r"D:\FYJ\PyQt\MyDataStudio\venv\Scripts\python.exe D:\FYJ\PyQt\MyDataStudio\test.py"]

sqllist = constant.SQLLIST


class MyThread(QThread):
    signalForText = pyqtSignal(str)

    def __init__(self, param=None, parent=None):
        super(MyThread, self).__init__(parent)
        # 如果有参数，可以封装在类里面
        self.param = param

    def write(self, text):
        self.signalForText.emit(str(text))  # 发射信号

    def run(self):
        # p = subprocess.Popen(r"D:\FYJ\PyQt\QtLearning\venv\Scripts\python.exe D:\FYJ\PyQt\choice_data\test.py", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p = subprocess.Popen(cmdlist[self.param], stdout=subprocess.PIPE, stderr=subprocess.PIPE) # 通过成员变量传参
        while True:
            result = p.stdout.readline()
            # print("result{}".format(result))
            if result != b'':
                print(result.decode('utf-8').strip('\r\n'))  # 对结果进行UTF-8解码以显示中文
                self.write(result.decode('utf-8').strip('\r\n'))
            else:
                break
        while True:
            result = p.stderr.readline()
            # print("result{}".format(result))
            if result != b'':
                print(result.decode('utf-8').strip('\r\n'))  # 对结果进行UTF-8解码以显示中文
                self.write(result.decode('utf-8').strip('\r\n'))
            else:
                break
        p.stdout.close()
        p.stderr.close()
        p.wait()


class newTab(QWidget):

    def __init__(self):
        super(newTab, self).__init__()
        self.initUI()


    def initUI(self):
        self.frame = QFrame(self)
        # self.frame.setFont(QFont('宋体', 12)) # 当只有一层tabwidget时起作用，多层tabwidget时就需要将frame里的每个组件setFont
        self.tabLayout = QVBoxLayout()
        self.setLayout(self.tabLayout)
        self.splitter1 = QSplitter(Qt.Vertical)
        self.splitter1.addWidget(self.frame)
        sp = self.frame.sizePolicy()
        sp.setVerticalStretch(1)
        self.frame.setSizePolicy(sp)


        self.tabLayout.addWidget(self.splitter1)
        optionFrame = QFrame(self.frame)
        optionFrame.setGeometry(QRect(100, 0, 1500, 300))

        # 查询按钮
        select_but = QPushButton("开始查询", optionFrame)
        select_but.move(500, 0)
        select_but.clicked.connect(self.showSqlResult)  # 查询按钮
        # 新增标签页按钮
        self.newTab_but = QPushButton("新建查询", optionFrame)
        self.newTab_but.move(1000, 0)
        # 执行程序按钮
        exec_but = QPushButton("开始执行", optionFrame)
        exec_but.move(800, 0)
        exec_but.clicked.connect(self.realtime_display)
        self.date = QDateEdit(QDate.currentDate().addDays(-1), optionFrame)
        self.date.setDisplayFormat("yyyy-MM-dd")  # 设置日期格式
        self.date.setMinimumDate(QDate.currentDate().addDays(-365))  # 设置最小日期
        self.date.setMaximumDate(QDate.currentDate())  # 设置最大日期
        self.date.setCalendarPopup(True)
        self.date.move(0, 0)

        # self.initQueryArea()

        self.combobox = QComboBox(optionFrame)
        self.combobox.setFixedSize(250, 25)
        self.combobox.move(200, 0)
        self.combobox.addItems(combolist)

        self.cmdCombobox = QComboBox(optionFrame)
        self.cmdCombobox.setFixedSize(100, 25)
        self.cmdCombobox.move(650, 0)
        self.cmdCombobox.addItems(exec_combolist)

        self.runWidget = QWidget()
        self.runWidgetLayout = QHBoxLayout(self.runWidget)
        self.runWidget.resize(1100, 800)
        self.runTextBrowser = QTextBrowser()
        self.runWidgetLayout.addWidget(self.runTextBrowser)
        self.runTextBrowser.setFont(QFont('宋体', 12))
        self.runTextBrowser.ensureCursorVisible()  # 游标可用



        # 每个组件逐一设置字体，很无奈
        optionFrame.setFont(QFont('宋体', 12))
        select_but.setFont(QFont('宋体', 12))
        exec_but.setFont(QFont('宋体', 12))
        self.newTab_but.setFont(QFont('宋体', 12))
        self.date.setFont(QFont('宋体', 12))
        self.combobox.setFont(QFont('宋体', 12))
        self.cmdCombobox.setFont(QFont('宋体', 12))


    def showSqlResult(self):
        start_time = time.time()
        index = self.combobox.currentIndex()
        date = self.date.date().toString("yyyy-MM-dd")  # 获取日期控件当前设置的日期

        if date == "":
            QMessageBox.information(self, "提示", "请选择日期！")
        else:
            if self.splitter1.count() > 1:
                sip.delete(self.outputWidget)

            self.outputWidget = QTabWidget()
            sp = self.outputWidget.sizePolicy()
            sp.setVerticalStretch(50)
            self.outputWidget.setSizePolicy(sp)
            self.splitter1.addWidget(self.outputWidget)
            self.infoWidget = QWidget()
            self.infoWidget.resize(1100, 800)
            self.textBrowser = QTextBrowser(self.infoWidget)
            self.textBrowser.resize(1100, 800)
            self.textBrowser.setFont(QFont('宋体', 12))
            self.textBrowser.ensureCursorVisible()  # 游标可用

            sql = sqllist[index].format(date)
            # 向SqlResultWin传参sql
            self.resultWidget = showSqlResult.SqlResultWin(sql)

            end_time = time.time()
            querytime = "查询耗时：{}秒".format(end_time - start_time)

            self.textBrowser.setPlainText(querytime)
            self.textBrowser.resize(1100, 800)
            self.textBrowser.setFont(QFont('宋体', 12))
            self.outputWidget.addTab(self.resultWidget, "查询结果")
            self.outputWidget.addTab(self.infoWidget, "信息")



    def realtime_display(self):
        print('Running...')
        index = self.cmdCombobox.currentIndex()
        try:
            self.t = MyThread(index)
            self.t.signalForText.connect(self.onUpdateText)
            self.t.start()
        except Exception as e:
            raise e

        loop = QEventLoop()
        QTimer.singleShot(2000, loop.quit)
        loop.exec_()

    def onUpdateText(self, text):
        if self.splitter1.count() > 1:
            self.outputWidget.addTab(self.runWidget, "运行结果")
        else:
            self.outputWidget = QTabWidget()
            sp = self.outputWidget.sizePolicy()
            sp.setVerticalStretch(50)
            self.outputWidget.setSizePolicy(sp)
            self.splitter1.addWidget(self.outputWidget)
            self.outputWidget.addTab(self.runWidget, "运行结果")
            # self.outputWidget.setCurrentIndex(2) # 这句不起作用

        cursor = self.runTextBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.runTextBrowser.append(text)
        self.runTextBrowser.setTextCursor(cursor)
        self.runTextBrowser.ensureCursorVisible()



