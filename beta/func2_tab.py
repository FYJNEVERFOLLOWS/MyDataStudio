import subprocess
import time


from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QTextCursor, QPixmap, QPainter, QColor
from PyQt5.QtWidgets import *

import const
import connect_mysql
import tableWidget
import date_tools

dbc = connect_mysql.myDBC()
combolist = const.FUNC2_COMBOLIST
cmdlist = const.CMDLIST
# cmdlist = [r"D:\FYJ\PyQt\QtLearning\venv\Scripts\python.exe D:\FYJ\PyQt\choice_data\test.py", r"D:\FYJ\PyQt\MyDataStudio\venv\Scripts\python.exe D:\FYJ\PyQt\MyDataStudio\test.py"]

sqllist = const.SQLLIST
now_date = date_tools.now_time()[:10]


class MyThread(QThread):
    signalForText = pyqtSignal(str)
    finish = pyqtSignal(bool)
    def __init__(self, index=None, date=None, parent=None):
        super(MyThread, self).__init__(parent)
        # 如果有参数，可以封装在类里面
        self.index = index
        self.date = date


    def write(self, text):
        self.signalForText.emit(str(text))  # 发射信号

    def run(self):
        # p = subprocess.Popen(r"D:\FYJ\PyQt\QtLearning\venv\Scripts\python.exe D:\FYJ\PyQt\choice_data\test.py", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # if self.date is None: args = ["python", "scripts.py", self.index]
        # else : args = ["python", "scripts.py", self.index, "--date", self.date]
        if self.date is None: args = "python" + " scripts.py " + str(self.index)
        else : args = "python " + "scripts.py " + str(self.index) + " --date " + str(self.date)
        print(args)
        self.finish.emit(False)
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) # 通过成员变量传参
        while True:
            if self.isInterruptionRequested():
                self.finish.emit(True)
                p.kill()
                return
            result = p.stdout.readline()
            # print("result{}".format(result))
            if result != b'':
                print(result.decode('utf-8').strip('\r\n'))  # 对结果进行UTF-8解码以显示中文
                self.write(result.decode('utf-8').strip('\r\n'))
            else:
                break
        while True:
            if self.isInterruptionRequested():
                self.finish.emit(True)
                p.kill()
                return
            result = p.stderr.readline()
            # print("result{}".format(result))
            if result != b'':
                print(result.decode('utf-8').strip('\r\n'))  # 对结果进行UTF-8解码以显示中文
                self.write(result.decode('utf-8').strip('\r\n'))
            else:
                break
        self.finish.emit(True)
        p.stdout.close()
        p.stderr.close()
        p.wait()

class LoadingWidget(QWidget):
    def __init__(self, parent=None):
        super(LoadingWidget, self).__init__(parent)
        self.rotateAngle = 0 # 每次旋转的角度

        # 设置定时器，每50ms旋转一次
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.slotTimeout)

    def paintEvent(self, evt):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        # 画边框
        painter.setPen(Qt.white)
        painter.drawRect(self.rect())

        realSize = min(self.width(), self.height()) - 10
        painter.translate(self.width()/2.0, self.height()/2.0)
        painter.scale(realSize/1000.0, realSize/1000.0)
        painter.rotate(self.rotateAngle)

        # 画外圈
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(80, 80, 80))
        painter.drawEllipse(QPointF(0, 0), 500, 500)

        # 园内部四个扇形区域，蓝白交叉
        startAngle = 0
        spanAngle = 90 * 16
        pieRect = QRectF(QPointF(-400, -400), QPointF(400, 400))
        for i in range(4):
            color = QColor(0, 120, 200) if i % 2 else QColor(240, 240, 240)
            painter.setBrush(color)
            painter.drawPie(pieRect, startAngle, spanAngle)
            startAngle += spanAngle

    def slotTimeout(self):
        self.rotateAngle = (self.rotateAngle + 2) % 360
        self.update()

    def slotStarted(self, param):
        # print("slotStarted {}".format(param))
        if not param:
            self.timer.start(10)

    def slotFinished(self, param):
        # print("slotFinished {}".format(param))
        if param:
            self.timer.stop()

class newTab(QWidget):

    def __init__(self, docker_id, docker_name, parent):
        super(newTab, self).__init__()
        self.docker_id = docker_id
        self.docker_name = docker_name
        self.parent = parent
        self.initUI()


    def initUI(self):
        self.frame = QFrame(self)
        # self.frame.setFont(QFont('宋体', 12)) # 当只有一层tabwidget时起作用，多层tabwidget时就需要将frame里的每个组件setFont
        self.tabLayout = QVBoxLayout()
        self.setLayout(self.tabLayout)
        self.splitter1 = QSplitter(Qt.Vertical)
        self.splitter1.addWidget(self.frame)
        sp = self.frame.sizePolicy()
        sp.setVerticalStretch(3)
        self.frame.setSizePolicy(sp)


        self.tabLayout.addWidget(self.splitter1)
        optionFrame = QFrame(self.frame)
        optionFrame.setGeometry(QRect(200, 0, 1500, 300))

        # 执行按钮
        select_but = QPushButton("开始执行", optionFrame)
        select_but.move(500, 0)
        select_but.clicked.connect(self.showSqlResult)  # 查询按钮

        self.loading = LoadingWidget(optionFrame)
        self.loading.move(600, 0)

        # 停止执行按钮
        terminate_but = QPushButton("停止执行", optionFrame)
        terminate_but.move(700, 0)
        terminate_but.clicked.connect(self.killSubProcess)  # 强制杀死执行当前脚本的子线程

        # 新增标签页按钮
        self.newTab_but = QPushButton("新建查询", optionFrame)
        self.newTab_but.move(800, 0)

        self.date = QDateEdit(QDate.fromString(now_date, "yyyy-MM-dd"), optionFrame)
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
        self.combobox.activated[int].connect(self.setTradeDate)

        self.outputWidget = QTabWidget()
        sp = self.outputWidget.sizePolicy()
        sp.setVerticalStretch(7)
        self.outputWidget.setSizePolicy(sp)
        self.splitter1.addWidget(self.outputWidget)

        self.infoWidget = QWidget()
        self.infoWidget.resize(1100, 800)
        self.infoWidgetLayout = QHBoxLayout(self.infoWidget)

        self.textBrowser = QTextBrowser()
        self.infoWidgetLayout.addWidget(self.textBrowser)
        self.textBrowser.resize(1100, 800)
        self.textBrowser.setFont(QFont('宋体', 12))
        self.textBrowser.ensureCursorVisible()  # 游标可用

        self.resultWidget = QWidget()
        self.tableWidget = tableWidget.newTableWidget()
        resultWidgetLayout = QHBoxLayout(self.resultWidget)
        resultWidgetLayout.addWidget(self.tableWidget, Qt.AlignCenter)

        self.outputWidget.addTab(self.infoWidget, "信息")
        self.outputWidget.addTab(self.resultWidget, "查询结果")


        # 每个组件逐一设置字体，很无奈
        optionFrame.setFont(QFont('宋体', 12))
        select_but.setFont(QFont('宋体', 12))
        self.newTab_but.setFont(QFont('宋体', 12))
        terminate_but.setFont(QFont('宋体', 12))
        self.date.setFont(QFont('宋体', 12))
        self.combobox.setFont(QFont('宋体', 12))

    def killSubProcess(self):
        if hasattr(self, 't'):
            self.t.requestInterruption()

    def setTradeDate(self, index):
        if index == 5:
            # print(date_tools.now_date())
            self.date.setDate(QDate.currentDate())
        else:
            self.date.setDate(QDate.fromString(now_date, "yyyy-MM-dd"))


    def showSqlResult(self):
        start_time = time.time()
        index = self.combobox.currentIndex()
        date = self.date.date().toString("yyyy-MM-dd")  # 获取日期控件当前设置的日期

        if date == "":
            QMessageBox.information(self, "提示", "请选择日期！")
        else:
            if index < 5:
                sql = sqllist[index].format(date)
                # 把sql执行结果传参给resultWidget的tablewidget
                results, cols = dbc.select(sql)
                if results == "Error:":
                    querytime = "数据库执行查询出现异常"

                else:
                    cnt_cols = len(cols)
                    self.tableWidget.setRowCount(len(results))  # 一定要设置行数，否则不会显示出tableWidget
                    self.tableWidget.setColumnCount(cnt_cols)
                    self.tableWidget.setHorizontalHeaderLabels(cols)  # 先设置列数后，设置表头才能生效
                    self.tableWidget.horizontalHeader().setStyleSheet("color: #00007f")
                    self.tableWidget.setAlternatingRowColors(True)  # 设置行背景颜色交替
                    self.tableWidget.setSortingEnabled(True)
                    self.tableWidget.setStyleSheet("border: 0px; alternate-background-color: #C9E4CC")
                    x = 0
                    for row in results:
                        for y in range(cnt_cols):
                            self.tableWidget.setItem(x, y, QTableWidgetItem(str(row[y])))
                        x += 1
                    self.tableWidget.expaction.triggered.connect(lambda: self.tableWidget.export(cols))  # 使用lambda表达式传递自定义参数

                    end_time = time.time()
                    querytime = "查询耗时：{}秒".format(end_time - start_time)


                self.textBrowser.clear()
                self.textBrowser.setPlainText(querytime)

            else:
                self.killSubProcess()

                # 清除上一次的查询结果
                self.tableWidget.setRowCount(0) # 一定要设置行数，否则不会显示出tableWidget
                self.tableWidget.setColumnCount(0)
                # 执行指令
                print('Running...')
                try:
                    self.t = MyThread(index, date)
                    self.t.signalForText.connect(self.onUpdateText)
                    self.t.finish.connect(self.loading.slotStarted)
                    self.t.finish.connect(self.loading.slotFinished)
                    self.t.start()
                except Exception as e:
                    raise e

                self.textBrowser.clear()


    def onUpdateText(self, text):
        cursor = self.textBrowser.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.textBrowser.append(text)
        self.textBrowser.setTextCursor(cursor)
        self.textBrowser.ensureCursorVisible()

    def refresh_parent(self, parent):
        self.parent = parent
        # self.signal_doc.connect(self.parent.signal_doc)

    def refresh_docker_name(self, name):
        self.docker_name = name

