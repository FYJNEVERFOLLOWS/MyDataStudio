import sys
from PyQt5 import sip

from PyQt5.QtCore import *
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *

import comboCheckBox
import connect_mysql
import showSqlResult

dbc = connect_mysql.myDBC()
combolist = [u'账户资产信息', u'产品信息', u'账户持仓信息', u'策略指令信息', u'策略净值估值信息', u'账户交易信息', u'账户交易流水信息']
comboDict = {0: [u'权益历史信息表', u'期货账户历史信息表', u'两融账户历史信息表', u'期权账户历史信息表'],
             1: [u'产品资产值表', u'产品出入金表', u'产品净值表'],
             2: [u'权益账户持仓历史信息表', u'期货账户持仓历史信息表', u'两融账户持仓历史信息表', u'期权账户持仓历史信息表'],
             3: [u'转债期货策略指令信息表', u'转债两融策略指令信息表', u'期权中高频策略', u'期权中低频多头策略', u'期权中低频空头策略', u'补单指令信息表', u'股票策略指令信息表'],
             4: [u'转债期货策略估值信息表', u'转债两融策略估值信息表', u'期权中高频策略估值信息表1', u'期权中高频策略估值信息表2', u'期权中高频策略估值信息表3', u'股票策略估值信息表',
                 u'转债期货策略持仓信息表', u'转债两融策略持仓信息表', u'期权中高频策略持仓信息表1', u'期权中高频策略持仓信息表2', u'期权中高频策略持仓信息表3', u'股票策略持仓信息表',
                 u'转债期货策略净值信息表', u'转债两融策略净值信息表', u'期权中高频策略净值信息表1', u'期权中高频策略净值信息表2', u'期权中高频策略净值信息表3', u'股票策略净值信息表'],
             5: [u'交易记录信息表', u'权益交易信息表', u'期货交易信息表', u'两融交易信息表', u'期权交易信息表'],
             6: [u'权益账户交易历史信息表', u'期货账户交易历史信息表', u'两融账户交易历史信息表', u'期权账户交易历史信息表']}
colDict = {0: {
    0: ['product_name', 'account_id', 'account_type', 'total_value', 'market_value', 'total_cash', 'available_cash',
        'holding_pnl'],
    1: ['product_name', 'account_id', 'account_type', 'total_value', 'margin', 'total_cash', 'available_cash',
        'position_pnl', 'trading_pnl', 'transaction_cost', 'risk_degree'],
    2: ['product_name', 'account_id', 'account_type', 'total_assets', 'net_assets', 'total_liability', 'pnl',
        'available_margin', 'maintenance_margin_rate', 'available_cash', 'total_cash', 'interest'],
    3: ['product_name', 'account_id', 'account_type', 'total_value', 'margin', 'total_cash', 'available_cash',
        'preminum_received', 'preminum_paid', 'transaction_cost', 'risk_degree']},
    1: {0: ['total_value', 'transfer_cash'],
        1: ['product_name', 'trusteeship_cash', 'transfer_cash', 'direction', 'counter_account',
            'counter_account_id', 'note'],
        2: ['total_value', 'transfer_cash', 'total_value_yes', 'pct_chg', 'static_net_value', 'net_value']},
    2: {0: ['account_id', 'account_type', 'code', 'symbol', 'exchange', 'quantity', 'sellable', 'avg_price',
            'avg_price2', 'last_price', 'market_value', 'holding_pnl'],
        1: ['account_id', 'account_type', 'code', 'symbol', 'exchange', 'buy_quantity', 'buy_avg_open_price',
            'sell_quantity', 'sell_avg_open_price', 'margin', 'position_pnl'],
        2: ['account_id', 'account_type', 'open_date', 'delivery_date', 'code', 'symbol', 'exchange',
            'sell_avg_open_price', 'sell_margin_rate', 'sell_margin', 'sell_transaction_cost',
            'sell_margin_quantity', 'sell_total_margin_quantity'],
        3: ['account_id', 'account_type', 'code', 'symbol', 'exchange', 'side', 'quantity', 'avg_open_price',
            'margin', 'position_pnl', 'pnl']},
    3: {0: ['code', 'amount', 'part'],
        1: ['stock_code', 'stock_amount', 'cbond_code', 'cbond_amount'],
        2: ['code', 'amount'],
        3: ['code', 'amount'],
        4: ['code', 'amount'],
        5: ['code', 'amount'],
        6: ['code', 'amount', 'part']},
    4: {0: ['code', 'symbol', 'avg_price', 'amount', 'avg_price_old', 'amount_old', 'avg_price_reb',
            'amount_reb', 'part', 'close', 'close_yes', 'mvalue', 'mvalue_yes', 'mvalue_reb', 'pct_chg',
            'pos_pert', 'pnl_reb', 'pnl_old_holding', 'pnl'],
        1: ['stock_code', 'stock_symbol', 'stock_avg_price', 'stock_amount', 'stock_avg_price_old',
            'stock_amount_old', 'stock_avg_price_reb', 'stock_amount_reb', 'cbond_code', 'cbond_symbol',
            'cbond_avg_price', 'cbond_amount', 'cbond_avg_price_old',
            'cbond_amount_old', 'cbond_avg_price_reb', 'cbond_amount_reb', 'stock_close', 'cbond_close',
            'stock_mvalue', 'cbond_mvalue', 'stock_close_yes', 'cbond_close_yes', 'stock_mvalue_yes',
            'cbond_mvalue_yes', 'stock_mvalue_reb', 'cbond_mvalue_reb',
            'pct_chg', 'stock_pct_chg', 'cbond_pct_chg', 'stock_pos_pert', 'cbond_pos_pert', 'stock_pnl_reb',
            'stock_pnl_old_holding', 'cbond_pnl_reb', 'cbond_pnl_old_holding', 'stock_pnl', 'cbond_pnl', 'pnl'],
        2: ['code', 'symbol', 'underlying', 'avg_price', 'amount', 'avg_price_old', 'amount_old',
            'avg_price_reb', 'amount_reb', 'multiplier', 'close', 'close_yes', 'mvalue', 'mvalue_yes',
            'mvalue_reb', 'pnl_reb', 'pnl_old_holding', 'pnl'],
        3: ['code', 'symbol', 'underlying', 'avg_price', 'amount', 'avg_price_old', 'amount_old',
            'avg_price_reb', 'amount_reb', 'multiplier', 'close', 'close_yes', 'mvalue', 'mvalue_yes',
            'mvalue_reb', 'pnl_reb', 'pnl_old_holding', 'pnl'],
        4: ['code', 'symbol', 'underlying', 'avg_price', 'amount', 'avg_price_old', 'amount_old',
            'avg_price_reb', 'amount_reb', 'multiplier', 'close', 'close_yes', 'mvalue', 'mvalue_yes',
            'mvalue_reb', 'pnl_reb', 'pnl_old_holding', 'pnl'],
        5: ['code', 'symbol', 'avg_price', 'amount', 'avg_price_old', 'amount_old', 'avg_price_reb',
            'amount_reb', 'part', 'close', 'close_yes', 'mvalue', 'mvalue_yes', 'mvalue_reb', 'pct_chg',
            'pos_pert', 'pnl_reb', 'pnl_old_holding', 'pnl'],
        6: ['code', 'symbol', 'avg_price', 'amount', 'avg_price_old', 'amount_old', 'avg_price_reb',
            'amount_reb', 'part'],
        7: ['stock_code', 'stock_symbol', 'stock_avg_price', 'stock_amount', 'stock_avg_price_old',
            'stock_amount_old', 'stock_avg_price_reb', 'stock_amount_reb', 'cbond_code', 'cbond_symbol',
            'cbond_avg_price', 'cbond_amount', 'cbond_avg_price_old',
            'cbond_amount_old', 'cbond_avg_price_reb', 'cbond_amount_reb'],
        8: ['code', 'symbol', 'underlying', 'avg_price', 'amount', 'avg_price_old', 'amount_old',
            'avg_price_reb', 'amount_reb'],
        9: ['code', 'symbol', 'underlying', 'avg_price', 'amount', 'avg_price_old', 'amount_old',
            'avg_price_reb', 'amount_reb'],
        10: ['code', 'symbol', 'underlying', 'avg_price', 'amount', 'avg_price_old', 'amount_old',
             'avg_price_reb', 'amount_reb'],
        11: ['code', 'symbol', 'avg_price', 'amount', 'avg_price_old', 'amount_old', 'avg_price_reb',
             'amount_reb', 'part'],
        12: ['part', 'cbond_mvalue', 'futures_mvalue', 'cbond_mvalue_yes', 'futures_mvalue_yes',
             'cbond_mvalue_reb', 'futures_mvalue_reb', 'cbond_pct_chg', 'futures_pct_chg', 'pct_chg',
             'cbond_pos_pert', 'futures_pos_pert',
             'futures_wgt', 'cbond_pnl_reb', 'cbond_pnl_old_holding', 'futures_pnl_reb',
             'futures_pnl_old_holding', 'cbond_pnl', 'futures_pnl', 'pnl'],
        13: ['stock_mvalue', 'cbond_mvalue', 'stock_mvalue_yes', 'cbond_mvalue_yes', 'stock_mvalue_reb',
             'cbond_mvalue_reb', 'stock_pct_chg', 'cbond_pct_chg', 'pct_chg', 'stock_pnl_reb',
             'stock_pnl_old_holding',
             'cbond_pnl_reb', 'cbond_pnl_old_holding', 'stock_pnl', 'cbond_pnl', 'pnl'],
        14: ['mvalue', 'mvalue_yes', 'mvalue_reb', 'pnl_reb', 'pnl_old_holding', 'pnl', 'underlying'],
        15: ['mvalue', 'mvalue_yes', 'mvalue_reb', 'pnl_reb', 'pnl_old_holding', 'pnl', 'underlying'],
        16: ['mvalue', 'mvalue_yes', 'mvalue_reb', 'pnl_reb', 'pnl_old_holding', 'pnl', 'underlying'],
        17: ['part', 'mvalue', 'mvalue_yes', 'mvalue_reb', 'pnl_reb', 'pnl_old_holding', 'pnl']},
    5: {0: ['code', 'symbol', 'direction', 'pos_effect', 'amount', 'avg_price', 'trans_type', 'source'],
        1: ['code', 'symbol', 'direction', 'total_amount', 'avg_price', 'trans_type'],
        2: ['code', 'symbol', 'direction', 'pos_effect', 'total_volume', 'avg_price', 'trans_type'],
        3: ['code', 'symbol', 'direction', 'total_amount', 'avg_price', 'trans_type'],
        4: ['code', 'symbol', 'direction', 'pos_effect', 'total_volume', 'avg_price', 'trans_type']},
    6: {0: ['account_id', 'time', 'code', 'symbol', 'exchange', 'direction', 'amount', 'price', 'trans_type'],
        1: ['account_id', 'time', 'code', 'symbol', 'exchange', 'direction', 'pos_effect', 'volume', 'price',
            'fee', 'realized_pnl', 'trans_type'],
        2: ['account_id', 'time', 'code', 'symbol', 'exchange', 'direction', 'amount', 'price', 'trans_type'],
        3: ['account_id', 'time', 'code', 'symbol', 'exchange', 'direction', 'pos_effect', 'volume', 'price',
            'trans_type']}}
sqlDict = {0: {0: 'acc_equity', 1: 'acc_futures', 2: 'acc_margin', 3: 'acc_option'},
           1: {0: 'pdt_acc_value', 1: 'pdt_deposit', 2: 'pdt_net_value'},
           2: {0: 'pos_equity', 1: 'pos_futures', 2: 'pos_margin', 3: 'pos_option'},
           3: {0: 'sig_futures', 1: 'sig_margin', 2: 'sig_option1', 3: 'sig_option2', 4: 'sig_option3', 5: 'sig_other',
               6: 'sig_stock'},
           4: {0: 'stgy_ass_futures', 1: 'stgy_ass_margin', 2: 'stgy_ass_option1', 3: 'stgy_ass_option2',
               4: 'stgy_ass_option3', 5: 'stgy_ass_stock',
               6: 'stgy_pos_futures', 7: 'stgy_pos_margin', 8: 'stgy_pos_option1', 9: 'stgy_pos_option2',
               10: 'stgy_pos_option3', 11: 'stgy_pos_stock',
               12: 'stgy_value_futures', 13: 'stgy_value_margin', 14: 'stgy_value_option1', 15: 'stgy_value_option2',
               16: 'stgy_value_option3', 17: 'stgy_value_stock'},
           5: {0: 'trade_all', 1: 'trade_equity', 2: 'trade_futures', 3: 'trade_margin', 4: 'trade_option'},
           6: {0: 'trans_equity', 1: 'trans_futures', 2: 'trans_margin', 3: 'trans_option'}}

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
            if self.splitter2.count() > 1:
                sip.delete(self.resultWidget)

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


            self.resultWidget = showSqlResult.SqlResultWin(sql)
            self.splitter2.addWidget(self.resultWidget)
            sp = self.resultWidget.sizePolicy()
            sp.setVerticalStretch(4)
            self.resultWidget.setSizePolicy(sp)
