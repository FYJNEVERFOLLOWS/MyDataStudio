from PyQt5 import sip

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import const
import comboCheckBox
import connect_mysql
import tableWidget

dbc = connect_mysql.myDBC()
combolist = const.COMBOLIST
comboDict = const.COMBODICT
colDict = const.COLDICT
sqlDict = const.SQLDICT

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
        sp.setVerticalStretch(5)
        self.frame.setSizePolicy(sp)
        self.splitter2 = QSplitter(Qt.Vertical)
        self.splitter2.addWidget(self.splitter1)
        sp = self.splitter1.sizePolicy()
        sp.setVerticalStretch(6)
        self.splitter1.setSizePolicy(sp)

        # self.tabLayout.addWidget(self.splitter1)
        self.tabLayout.addWidget(self.splitter2)
        optionFrame = QFrame(self.frame)

        # self.frame.setStyleSheet('background-color:red;')  # 设置背景色
        optionFrame.setGeometry(QRect(200, 0, 1200, 30))
        cat1_lbl = QLabel("大类", optionFrame)
        cat1_lbl.move(0, 3)

        self.combo1 = QComboBox(optionFrame)
        self.combo1.setFixedSize(200, 25)
        self.combo1.move(40, 0)

        self.combo1.activated[int].connect(self.initCombo2)
        # self.combo1.activated[int].connect(self.select_but)
        self.combo1.activated[int].connect(self.initCheckBox)

        # 大类
        self.combo1.addItems(combolist)
        # 小类
        cat2_lbl = QLabel("小类", optionFrame)
        cat2_lbl.move(270, 3)
        self.combo2 = QComboBox(optionFrame)
        self.combo2.setFixedSize(250, 25)
        self.combo2.move(320, 0)
        # self.combo2.setCurrentIndex(0)  # 设置默认值
        self.combo2.addItems(comboDict[0])
        self.combo2.activated[int].connect(self.initCheckBox)

        # 查询按钮
        select_but = QPushButton("开始查询", optionFrame)
        select_but.move(600, 0)
        select_but.clicked.connect(self.showSqlResult)  # 查询按钮
        # 新增标签页按钮
        self.newTab_but = QPushButton("新建查询", optionFrame)
        self.newTab_but.move(800, 0)

        self.resultWidget = tableWidget.newTableWidget()
        self.splitter2.addWidget(self.resultWidget)
        sp = self.resultWidget.sizePolicy()
        sp.setVerticalStretch(4)
        self.resultWidget.setSizePolicy(sp)

        # 每个组件逐一设置字体，很无奈
        optionFrame.setFont(QFont('宋体', 12))
        cat1_lbl.setFont(QFont('宋体', 12))
        cat2_lbl.setFont(QFont('宋体', 12))
        self.combo1.setFont(QFont('宋体', 12))
        self.combo2.setFont(QFont('宋体', 12))
        select_but.setFont(QFont('宋体', 12))
        self.newTab_but.setFont(QFont('宋体', 12))

        self.initCheckBox()

    def initCombo2(self, firstidx):  # 用activated信号实现下拉列表的两级联动
        self.combo2.clear()
        if firstidx == 0:
            self.combo2.addItems(comboDict[0])
        elif firstidx == 1:
            self.combo2.addItems(comboDict[1])
        elif firstidx == 2:
            self.combo2.addItems(comboDict[2])
        elif firstidx == 3:
            self.combo2.addItems(comboDict[3])
        elif firstidx == 4:
            self.combo2.addItems(comboDict[4])
            self.combo2.setMaxVisibleItems(20)  # 令复选框最多显示20项
        elif firstidx == 5:
            self.combo2.addItems(comboDict[5])
        elif firstidx == 6:
            self.combo2.addItems(comboDict[6])

    def initCheckBox(self):
        if self.splitter1.count() > 1:
            # self.splitter1.removeWidget(self.checkWidget)
            sip.delete(self.checkWidget)

        firstIndex = self.combo1.currentIndex()
        secondIndex = self.combo2.currentIndex()

        self.checkWidget = QWidget()
        checkWidgetlayout = QHBoxLayout(self.checkWidget)
        groupBox = QGroupBox("请设置搜索条件（必须设置起止日期和产品代码）")
        groupBox.setFont(QFont('宋体', 12))
        self.groupBoxLayout = QGridLayout(groupBox)
        self.checkBoxall = QCheckBox("&全选/全不选")
        self.checkBoxall.stateChanged[int].connect(self.switchSelectAll)
        self.groupBoxLayout.addWidget(self.checkBoxall, 0, 0)
        self.groupBoxLayout.setSpacing(20)  # 像素.应为两个组件之间的距离

        self.start_date = QDateEdit(QDate(2021, 3, 1))
        self.start_date.setDisplayFormat("yyyy-MM-dd")  # 设置日期格式
        self.start_date.setMinimumDate(QDate.currentDate().addDays(-365))  # 设置最小日期
        self.start_date.setMaximumDate(QDate.currentDate())  # 设置最大日期
        self.start_date.setCalendarPopup(True)

        self.end_date = QDateEdit(QDate.currentDate())
        self.end_date.setDisplayFormat("yyyy-MM-dd")  # 设置日期格式
        self.end_date.setMinimumDate(QDate.currentDate().addDays(-365))  # 设置最小日期
        self.end_date.setMaximumDate(QDate.currentDate())  # 设置最大日期
        self.end_date.setCalendarPopup(True)

        self.groupBoxLayout.addWidget(self.start_date, 0, 1)
        self.groupBoxLayout.addWidget(self.end_date, 0, 2)

        sql = "SELECT DISTINCT product_id FROM {} ORDER BY product_id ASC".format(sqlDict[firstIndex][secondIndex])
        results, list_cols = dbc.select(sql)
        items = []
        for row in results:
            items.append(str(row[0]))
        productWidget = QWidget()
        self.product_id = comboCheckBox.ComboCheckBox(productWidget, items)
        self.product_id.All(2)
        self.groupBoxLayout.addWidget(self.product_id, 0, 3)

        cbname_list = colDict[firstIndex][secondIndex]
        for i in range(len(cbname_list)):
            # 其他静态编译语言只能在代码中手动写出所有变量名，但Python可以动态创建变量
            exec('self.checkBox{} = QCheckBox(cbname_list[{}])'.format(i,
                                                                       i))  # 得到变量self.checkBoxi(i in range(len(cbname_list))
            exec('self.checkBox{}.setChecked(True)'.format(i))  # exec返回值为none，要把表达式写进去
            exec('self.groupBoxLayout.addWidget(self.checkBox{}, (i + 4) / 6, (i + 4) % 6)'.format(
                i))  # exec里写表达式，用于执行表达式
            exec("self.checkBox{}.setFont(QFont('宋体', 12))".format(i))

        checkWidgetlayout.addWidget(groupBox)
        # checkWidgetlayout.setStretch(0, 9)
        # checkWidgetlayout.setStretch(1, 1)  # 左右组件比列设置为9:1
        sp = self.checkWidget.sizePolicy()
        sp.setVerticalStretch(5)
        self.checkWidget.setSizePolicy(sp)

        self.splitter1.addWidget(self.checkWidget)

        self.checkBoxall.setFont(QFont('宋体', 12))
        self.start_date.setFont(QFont('宋体', 12))
        self.end_date.setFont(QFont('宋体', 12))
        self.checkWidget.setFont(QFont('宋体', 12))
        self.checkBoxall.setFont(QFont('宋体', 12))
        # self.tabLayout.setStretch(0, 3)
        # self.tabLayout.setStretch(1, 7)  # 上下组件比列设置为3:7
        # 该例子设置groupbox1/2/3的比例为1：3：1
        # layout.setStretchFactor(groupbox1, 1)
        # layout.setStretchFactor(groupbox2, 3)
        # layout.setStretchFactor(groupbox3, 1)

    def switchSelectAll(self, state):
        if state == 0:
            for i in range(self.groupBoxLayout.count() - 4):
                exec('self.checkBox{}.setCheckState(2)'.format(i))
        if state == 2:
            for i in range(self.groupBoxLayout.count() - 4):
                exec('self.checkBox{}.setCheckState(0)'.format(i))

    def showSqlResult(self):
        showFlag = False
        firstIndex = self.combo1.currentIndex()
        secondIndex = self.combo2.currentIndex()

        start_date = self.start_date.date().toString("yyyy-MM-dd")  # 获取日期控件当前设置的日期
        end_date = self.end_date.date().toString("yyyy-MM-dd")  # 获取日期控件当前设置的日期
        # 检测每个复选框是否被选中
        col_selected = ['date', 'product_id']  # 记录选中的复选框，日期和产品代码为必选
        col_temp = colDict[firstIndex][secondIndex]
        for i in range(self.groupBoxLayout.count() - 4):
            flag = eval('self.checkBox{}.isChecked()'.format(i))  # 计算指定表达式的值
            # exec('flag = self.checkBox{}.isChecked()'.format(i))执行无效，flag的值不会变，为什么？
            if flag:
                col_selected.append(col_temp[i])
        if len(self.product_id.getCheckItems()) == 0:
            QMessageBox.information(self, "提示", "请选择产品代码！")
        else:
            cols = ''
            for idx, col in enumerate(col_selected):
                if idx > 0:
                    cols += ', '
                cols += col

            array_pdtid_selected = ''  # 自己构建字符串而不是用tuple(pdtid_selected)，一来因为tuple只有一个元素时会在末尾加','（进而引起SQL执行错误），二来避免SQL注入
            for val in self.product_id.getCheckItems():
                array_pdtid_selected += "'" + val + "',"  # 后面用[:-1]切片去掉最后一个逗号
            sql = "SELECT {} FROM {} WHERE product_id IN ({}) and date_format(date,'%Y-%m-%d') >= '{}' and date_format(date,'%Y-%m-%d') <= '{}'".format(
                cols, sqlDict[firstIndex][secondIndex], array_pdtid_selected[:-1], start_date, end_date)
            # 把sql执行结果传参给resultWidget的tablewidget
            results, cols = dbc.select(sql)

            cnt_cols = len(cols)
            self.resultWidget.setRowCount(len(results))  # 一定要设置行数，否则不会显示出tableWidget
            self.resultWidget.setColumnCount(cnt_cols)
            self.resultWidget.setHorizontalHeaderLabels(cols)  # 先设置列数后，设置表头才能生效
            self.resultWidget.horizontalHeader().setStyleSheet("color: #00007f")
            self.resultWidget.setAlternatingRowColors(True)  # 设置行背景颜色交替
            self.resultWidget.setSortingEnabled(True)
            self.resultWidget.setStyleSheet("border: 0px; alternate-background-color: #C9E4CC")
            x = 0
            for row in results:
                for y in range(cnt_cols):
                    self.resultWidget.setItem(x, y, QTableWidgetItem(str(row[y])))
                x += 1
            self.resultWidget.expaction.triggered.connect(lambda: self.resultWidget.export(cols))  # 使用lambda表达式传递自定义参数

    def refresh_parent(self, parent):
        self.parent = parent
        # self.signal_doc.connect(self.parent.signal_doc)

    def refresh_docker_name(self, name):
        self.docker_name = name

        # self.log_event_type = LOG_MARK.join([EVENT_SCRIPT_LOG, str(self.docker_id)])
        # 链接signal
        # self.register_event()

        # script_engine = main_engine.get_engine(APP_NAME)
        # if script_engine.docker_id != self.docker_id:
        #     script_engine = ScriptEngine(self.main_engine, self.event_engine)
        #     script_engine.refresh_dock_id(self.docker_id)
        #     main_engine.add_engine_by_name(APP_NAME+str(docker_id), script_engine)
        # self.script_engine = script_engine


        # self.script_engine.init()

    def show(self):
        """"""
        # self.showMaximized
        self.showNormal()

    # def process_log_event(self, event: Event):
    #     """"""
    #     log = event.data
    #     # holder = '\n' + ' ' * 43
    #     # log_msg = f"{log.msg}".replace('\n', holder)
    #     log_msg = log.msg
    #     msg = f"{log.time}  {log_msg}"
    #     self.log_monitor.append(msg)