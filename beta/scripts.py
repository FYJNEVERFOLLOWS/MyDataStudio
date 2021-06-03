import os
import time
import argparse
import sys
sys.path.append("..") #把上级目录加入到变量中
from utils.const import *
from utils.tools import file_copy
from core.server import AmsServer
from core.server2 import AmsServer as AmsServer2
import pymongo

from core.allocator import Allocator
from com.logger import logger
from model.stragety_cmargin import StrategyCMargin
from model.stragety_stock import StrategyStock
from model.stragety_option import StrategyOption
from model.strategy_sidxfts import StrategySidxfts
from constant import PDT_CHECK_FILE_PATH, STGY_CMARGIN_DIR
from utils.date_tools import now_date, util_get_previous_trade_day

def main1(date):
    """
    上传交易流水和交易信号
    """
    ams_server = AmsServer2(date)
    # """
    while 1:
        check_in = ams_server.checker.main_check_input_files(ams_server.now_date, data_cls_li=[TRANS])
        if check_in:
            break
        else:
            print('wait...')
            time.sleep(20)
    # """
    ams_server.piker.main_pick_data_2_xlsx(ams_server.now_date, data_cls_li=[TRANS], export_119=True)
    for data_cls in [TRANS, SIG]:
        ams_server.loader.main_upload_data_2_sql(ams_server.now_date, data_cls=data_cls)
    ams_server.close()


def main2(date):
    """
    上传资产、持仓，生成净值表
    """
    ams_server = AmsServer2(date)
    data_cls_li = [DEPO, ACC, POS]
    # """
    while 1:
        check_in = ams_server.checker.main_check_input_files(ams_server.now_date, data_cls_li=data_cls_li)
        if check_in:
            break
        else:
            print('wait...')
            time.sleep(20)
    # """
    ams_server.piker.main_pick_data_2_xlsx(ams_server.now_date, data_cls_li=data_cls_li, export_119=True)
    for data_cls in data_cls_li:
        ams_server.loader.main_upload_data_2_sql(ams_server.now_date, data_cls=data_cls)
    ams_server.main_product_product_value()
    ams_server.main_upload_product_value()
    ams_server.main_download_product_value()
    ams_server.close()


def main_sig_1(param):
    yes_day = param
    dist_sfts = Allocator(StrategyCMargin,
                          yes_day=yes_day
                          )
    while 1:
        if dist_sfts.is_data_finished():
            dist_sfts.main_push_signal_2_mg()
            dist_sfts.main_save_trade_signal()
            break
        else:
            logger.info('wait...')
            time.sleep(60)


def main_sig_2(param):
    yes_day = param
    dist_sfts = Allocator(StrategyStock,
                          yes_day=yes_day
                          )
    while 1:
        if dist_sfts.is_data_finished():
            dist_sfts.main_push_signal_2_mg()
            dist_sfts.main_save_trade_signal()
            break
        else:
            logger.info('wait...')
            time.sleep(60)

def main_sig_3(param):
    yes_day = param
    dist_sfts = Allocator(StrategyOption,
                          yes_day=yes_day
                          )
    while 1:
        if dist_sfts.is_data_finished():
            dist_sfts.main_push_signal_2_mg()
            dist_sfts.main_save_trade_signal()
            break
        else:
            logger.info('wait...')
            time.sleep(60)

def main_sig_4(param):
    yes_day = param
    dist_sfts = Allocator(StrategySidxfts,
                          yes_day=yes_day
                          )
    while 1:
        if dist_sfts.is_data_finished():
            dist_sfts.main_push_signal_2_mg()
            dist_sfts.main_save_trade_signal()
            break
        else:
            logger.info('wait...')
            time.sleep(60)

def main_sig_c():
    yes_day = util_get_previous_trade_day(now_date())
    all_cm = Allocator(StrategyCMargin,
                       yes_day=yes_day
                       )
    while 1:
        if all_cm.is_data_finished([PDT_CHECK_FILE_PATH]):

            all_cm.main_save_trade_transaction()

            all_stk = Allocator(StrategyStock,
                                yes_day=yes_day
                                )
            all_stk.main_save_trade_transaction()

            all_op = Allocator(StrategyOption,
                               yes_day=yes_day
                               )
            all_op.main_save_trade_transaction()

            all_sfts = Allocator(StrategySidxfts,
                                 yes_day=yes_day
                                )
            all_sfts.main_save_trade_transaction()
            break
        else:
            logger.info('wait...')
            time.sleep(20)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='命令行中传入要执行的脚本序号及可选参数日期')
    # type是要传入的参数的数据类型  help是该参数的提示信息
    parser.add_argument('index', type=str, help='传入要执行的脚本序号')
    parser.add_argument('--date', type=str, help='传入的日期')

    args = parser.parse_args()

    # 获得传入的参数
    if args.index == '5':
        print("正在执行脚本main_1，设定的日期为{}，请稍候......".format(args.date))
        main1(args.date)
    elif args.index == '6':
        print("正在执行脚本main_2，设定的日期为{}，请稍候......".format(args.date))
        main2(args.date)
    elif args.index == '7':
        print("正在执行脚本main_sig_1，设定的日期为{}，请稍候......".format(args.date))
        main_sig_1(args.date)
    elif args.index == '8':
        print("正在执行脚本main_sig_2，设定的日期为{}，请稍候......".format(args.date))
        main_sig_2(args.date)
    elif args.index == '9':
        print("正在执行脚本main_sig_3，设定的日期为{}，请稍候......".format(args.date))
        main_sig_3(args.date)
    elif args.index == '10':
        print("正在执行脚本main_sig_4，设定的日期为{}，请稍候......".format(args.date))
        main_sig_4(args.date)
    elif args.index == '11':
        print("正在执行脚本main_sig_c，设定的日期为{}，请稍候......".format(args.date))
        main_sig_c()