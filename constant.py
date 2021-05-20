import os.path

INTERPRETER_PATH = r"D:\Git_tasks\task_new\azamsServer\venv\Scripts\python.exe"
PROJECT_PATH = r"D:\Git_tasks\task_new\azamsServer"

MONGO_HOST = "192.168.1.119"
MONGO_USER = "reader"
MONGO_PASSWD = "azReader"


MAIN1_PATH = os.path.join(PROJECT_PATH, 'main_1.py')
MAIN2_PATH = os.path.join(PROJECT_PATH, 'main_2.py')
STGY_OPTION_DIR = os.path.join(REC_HOST_PATH, '期权策略')
STGY_SIDXFTS_DIR = os.path.join(REC_HOST_PATH, '股指策略')
PDT_DIR = os.path.join(REC_HOST_PATH, '产品情况')

PDT_TRADE_PATH = os.path.join(PDT_DIR, '#交易情况')
PDT_CHECK_FILE_PATH = os.path.join(PDT_DIR, '交易检查记录.txt')
