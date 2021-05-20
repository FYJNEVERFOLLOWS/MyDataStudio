import subprocess
import sys
import time

from PyQt5 import sip

from PyQt5.QtCore import *
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtWidgets import *

import showSqlResult
import constant

combolist = ['债股策略估值持仓比对-转债', '债股策略估值持仓比对-股票', '股票策略估值持仓比对', '期权策略估值持仓比对', '股指策略估值持仓比对']
exec_combolist = ['main_1', 'main_2']
cmdlist = [constant.INTERPRETER_PATH +" " + constant.MAIN1_PATH, constant.INTERPRETER_PATH +" " + constant.MAIN2_PATH]
# cmdlist = [r"D:\FYJ\PyQt\QtLearning\venv\Scripts\python.exe D:\FYJ\PyQt\choice_data\test.py", r"D:\FYJ\PyQt\MyDataStudio\venv\Scripts\python.exe D:\FYJ\PyQt\MyDataStudio\test.py"]

sqllist = [
            "SELECT A1.date, A1.product_id, A1.code, IFNULL(t1.amount,0) as totalAmount, IFNULL(t2.amount,0)  as ftsAmount, IFNULL(t3.amount,0) as marginAmount, "
            "(IFNULL(t1.amount,0) - IFNULL(t2.amount, 0) - IFNULL(t3.amount, 0)) as DIFAmount " 
            "FROM "
            "(SELECT product_id, code, date FROM pos_equity WHERE date='{0}' and product_id in ('FH1', 'HT1', 'HT3', 'HT7', 'LH1', 'LH1', 'ZS1') "
            "UNION "
            "SELECT product_id, code, date FROM stgy_pos_futures WHERE date='{0}' and code not LIKE 'I%' "
            "UNION "
            "SELECT product_id, cbond_code as code, date FROM stgy_pos_margin WHERE date='{0}' "
            ") as A1 "
            "LEFT JOIN "
            "(SELECT product_id, code, sum(quantity) as amount, date from pos_equity where date='{0}' GROUP BY product_id, code ) AS t1 "
            "ON (t1.product_id, t1.code) = (A1.product_id, A1.code) "
            "LEFT JOIN "
            "(SELECT product_id, code, amount, date from stgy_pos_futures WHERE date='{0}') as t2 "
            "ON (t2.product_id, t2.code) = (A1.product_id, A1.code) "
            "LEFT JOIN "
            "(SELECT product_id, cbond_code as code, cbond_amount as amount, date from stgy_pos_margin WHERE date='{0}') as t3 "
            "ON (t3.product_id, t3.code) = (A1.product_id, A1.code) "
            "WHERE A1.code not LIKE '5%' "
            "order by product_id, code ",
            "SELECT  A1.date, A1.product_id, A1.code, IFNULL(t1.amount,0) as totalAmount, IFNULL(t2.amount,0) as marginAmount, (IFNULL(t1.amount,0) - IFNULL(t2.amount,0)) as DIFAmount FROM "
            "(SELECT product_id, code, date FROM pos_margin WHERE date='{0}' and product_id  NOT IN('FH2', 'FH3', 'FH9', 'FH10', 'HT2') "
            "UNION "
            "SELECT product_id, stock_code as code, date FROM stgy_pos_margin WHERE date='{0}' "
            ") as A1 "            
            "LEFT JOIN "
            "(SELECT date, product_id, code, sum(sell_margin_quantity) as amount FROM pos_margin WHERE date='{0}' GROUP BY product_id, code, date) as t1 "
            "ON (t1.product_id, t1.code) = (A1.product_id, A1.code) "
            "LEFT JOIN "
            "(SELECT date, product_id, stock_code as code, IFNULL(-stock_amount,0) as amount FROM stgy_pos_margin WHERE date='{0}') as t2 "
            "on (t2.product_id, t2.code) = (A1.product_id, A1.code) ",
            "SELECT A1.date, A1.product_id, A1.code, IFNULL(t1.amount,0) as totalAmount, IFNULL(t2.amount,0) as stgyAmount, (IFNULL(t1.amount,0) - IFNULL(t2.amount,0)) as DIFAmount "
            "FROM "            
            "(SELECT product_id, code, date FROM pos_equity where date='{0}' and product_id in ('FH2', 'FH3', 'FH9', 'FH10', 'HT2') "
            "UNION "
            "SELECT product_id, code, date from stgy_pos_stock WHERE date='{0}' "
            ") AS A1 "            
            "LEFT JOIN "
            "(SELECT product_id, code, sum(quantity) as amount, date from pos_equity where date='{0}' AND product_id in ('FH2', 'FH3', 'FH9', 'FH10', 'HT2') GROUP BY product_id, code) AS t1 "
            "ON (t1.product_id, t1.code) = (A1.product_id, A1.code) "
            "LEFT JOIN "
            "(SELECT product_id, code, SUM(amount) as amount, date from stgy_pos_stock WHERE date='{0}' GROUP BY product_id, code) AS t2 "
            "ON (t2.product_id, t2.code) = (A1.product_id, A1.code) "            
            "WHERE A1.code not LIKE '5%' "
            "ORDER BY product_id, code ",
    
            "SELECT A1.date, A1.product_id, A1.code, A1.side, IFNULL(t1.amount,0) as total_amount, "
            "IFNULL(t2.amount,0) as high_amount, IFNULL(t3.amount,0) as lowLongAmount, IFNULL(t4.amount,0) as lowShortAmount, (IFNULL(t1.amount,0) - IFNULL(t2.amount,0) - IFNULL(t3.amount,0) -IFNULL(t4.amount,0)) as DIFAmount, "
            "IFNULL(t5.amount,0) as tradeAmount, t5.pos_effect, IFNULL(t6.amount,0) as sigAmount "
            "FROM "
            "(SELECT product_id, code, side, date FROM pos_option where date='{0}' "
            "UNION "
            "SELECT product_id, code, CAST('SELL' AS CHAR) as side, date from stgy_pos_option1 WHERE date='{0}' "
            "UNION "
            "SELECT product_id, code, CAST('BUY' AS CHAR) as side, date from stgy_pos_option2 WHERE date='{0}' "
            "UNION "
            "SELECT product_id, code, CAST('SELL' AS CHAR) as side, date from stgy_pos_option3 WHERE date='{0}' "
            "UNION "
            "SELECT product_id, code, direction as side, date from trade_option WHERE date='{0}' "
            ") "
            "AS A1 "
            "LEFT JOIN "
            "(SELECT product_id, code, sum(quantity) as amount, side, date from pos_option where date='{0}' GROUP BY product_id, code, side) AS t1 "
            "ON (t1.product_id, t1.code, t1.side) = (A1.product_id, A1.code, A1.side) "
            "LEFT JOIN "
            "(SELECT product_id, code, ABS(amount) as amount, CAST('BUY' AS CHAR) as side, date from stgy_pos_option1 WHERE date='{0}') AS t2 "
            "ON (t2.product_id, t2.code, t2.side) = (A1.product_id, A1.code, A1.side) "
            "LEFT JOIN "
            "(SELECT product_id, code, ABS(amount) as amount, CAST('BUY' AS CHAR) as side, date from stgy_pos_option2 WHERE date='{0}') as t3 "
            "ON (t3.product_id, t3.code, t3.side) = (A1.product_id, A1.code, A1.side) "
            "LEFT JOIN "
            "(SELECT product_id, code, ABS(amount) as amount, CAST('SELL' AS CHAR) as side, date from stgy_pos_option3 WHERE date='{0}') as t4 "
            "ON (t4.product_id, t4.code, t4.side) = (A1.product_id, A1.code, A1.side) "
            "LEFT JOIN "
            "(SELECT date, product_id, code, direction as side, pos_effect, SUM(total_amount) as amount FROM "
            "(SELECT date, product_id, code, symbol, direction, pos_effect, total_volume as total_amount, avg_price, trans_type, CAST('option' AS CHAR) as source FROM trade_option WHERE date='{0}' "
            "ORDER BY date, product_id, code) AS trade_union GROUP BY product_id, code, direction) as t5 "
            "on (t5.product_id, t5.code, t5.side) = (A1.product_id, A1.code, A1.side) "
            "LEFT JOIN "
            "(SELECT product_id, code, ABS(SUM(amount)) as amount, side, date FROM "
                "("
                "SELECT product_id, code, amount, date, CAST(IF(amount < 0, 'SELL', 'BUY') AS CHAR) as side FROM sig_option1 WHERE date='{0}' "
                "UNION "
                "SELECT product_id, code, amount, date, CAST(IF(amount < 0, 'SELL', 'BUY') AS CHAR) as side FROM sig_option2 WHERE date='{0}' "
                "UNION "
                "SELECT product_id, code, amount, date, CAST(IF(amount < 0, 'SELL', 'BUY') AS CHAR) as side FROM sig_option3 WHERE date='{0}' "
                ") as T GROUP BY product_id, date, code, side) as t6 "
            "ON (t6.product_id, t6.code, t6.side) = (A1.product_id, A1.code, A1.side) "
            "ORDER BY product_id, code, side ",
            "SELECT A1.date, A1.product_id, A1.code, A1.side, IFNULL(t1.quantity,0) as totalAmount, ABS(IFNULL(t2.quantity,0)) as stgyAmount, (ABS(IFNULL(t1.quantity,0)) - ABS(IFNULL(t2.quantity,0))) as DIFAmount "
            "FROM "            
            "("
            "SELECT product_id, code, side, date FROM stgy_pos_sidxfts WHERE date='{0}' "
            "UNION "
            "SELECT product_id, code, CAST('BUY' AS CHAR) as side, date from pos_sfutures WHERE date='{0}' AND exchange = 'CFFEX' AND buy_quantity > 0 "
            "UNION "
            "SELECT product_id, code, CAST('SELL' AS CHAR) as side, date from pos_sfutures WHERE date='{0}' AND exchange = 'CFFEX' AND sell_quantity > 0 "
            ") "
            "AS A1 "            
            "LEFT JOIN "           
            "(SELECT product_id, code, buy_quantity as quantity, CAST('BUY' AS CHAR) as side, date from pos_sfutures where date='{0}' AND exchange = 'CFFEX' AND buy_quantity > 0 "
            "UNION "
            "SELECT product_id, code, sell_quantity as quantity, CAST('SELL' AS CHAR) as side, date from pos_sfutures where date='{0}' AND exchange = 'CFFEX' AND sell_quantity > 0) "
            "AS t1 "
            "ON (t1.product_id, t1.code, t1.side) = (A1.product_id, A1.code, A1.side) "
            "LEFT JOIN "
            "(SELECT product_id, code, amount as quantity, side, date from stgy_pos_sidxfts WHERE date='{0}') as t2 "
            "ON (t2.product_id, t2.code, t2.side) = (A1.product_id, A1.code, A1.side) "            
            "ORDER BY product_id, code, side"
           ]


class MyThread(QThread):
    signalForText = pyqtSignal(str)

    def __init__(self, param=None, parent=None):
        super(MyThread, self).__init__(parent)
        # 如果有参数，可以封装在类里面
        self.param = param

    def write(self, text):
        self.signalForText.emit(str(text))  # 发射信号

    def run(self):
        # p = subprocess.Popen(r"D:\Git_tasks\task_new\azamsServer\venv\Scripts\python.exe D:\Git_tasks\task_new\azamsServer\main_2.py", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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



