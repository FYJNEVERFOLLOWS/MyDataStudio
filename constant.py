import os.path

INTERPRETER_PATH = r"D:\Git_tasks\task_new\azamsServer\venv\Scripts\python.exe"
PROJECT_PATH = r"D:\Git_tasks\task_new\azamsServer"

MYSQL_HOST = "your mysql host path"
MYSQL_USER = "your username"
MYSQL_PASSWD = "azReader"


MAIN1_PATH = os.path.join(PROJECT_PATH, 'main_1.py')
MAIN2_PATH = os.path.join(PROJECT_PATH, 'main_2.py')


COMBOLIST = [u'账户资产信息', u'产品信息', u'账户持仓信息', u'策略指令信息', u'策略净值估值信息', u'账户交易信息', u'账户交易流水信息']
COMBODICT = {0: [u'权益历史信息表', u'期货账户历史信息表', u'两融账户历史信息表', u'期权账户历史信息表'],
             1: [u'产品资产值表', u'产品出入金表', u'产品净值表'],
             2: [u'权益账户持仓历史信息表', u'期货账户持仓历史信息表', u'两融账户持仓历史信息表', u'期权账户持仓历史信息表'],
             3: [u'转债期货策略指令信息表', u'转债两融策略指令信息表', u'期权中高频策略', u'期权中低频多头策略', u'期权中低频空头策略', u'补单指令信息表', u'股票策略指令信息表'],
             4: [u'转债期货策略估值信息表', u'转债两融策略估值信息表', u'期权中高频策略估值信息表1', u'期权中高频策略估值信息表2', u'期权中高频策略估值信息表3', u'股票策略估值信息表',
                 u'转债期货策略持仓信息表', u'转债两融策略持仓信息表', u'期权中高频策略持仓信息表1', u'期权中高频策略持仓信息表2', u'期权中高频策略持仓信息表3', u'股票策略持仓信息表',
                 u'转债期货策略净值信息表', u'转债两融策略净值信息表', u'期权中高频策略净值信息表1', u'期权中高频策略净值信息表2', u'期权中高频策略净值信息表3', u'股票策略净值信息表'],
             5: [u'交易记录信息表', u'权益交易信息表', u'期货交易信息表', u'两融交易信息表', u'期权交易信息表'],
             6: [u'权益账户交易历史信息表', u'期货账户交易历史信息表', u'两融账户交易历史信息表', u'期权账户交易历史信息表']}
COLDICT = {0: {
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
SQLDICT = {0: {0: 'acc_equity', 1: 'acc_futures', 2: 'acc_margin', 3: 'acc_option'},
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

FUNC2_COMBOLIST = ['债股策略估值持仓比对-转债', '债股策略估值持仓比对-股票', '股票策略估值持仓比对', '期权策略估值持仓比对', '股指策略估值持仓比对']
EXEC_COMBOLIST = ['main_1', 'main_2']
CMDLIST = [INTERPRETER_PATH + " " + MAIN1_PATH, INTERPRETER_PATH + " " + MAIN2_PATH]

SQLLIST = [
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


