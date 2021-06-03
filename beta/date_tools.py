
import pandas as pd
import tushare as ts
import datetime as dtm


trade_date_sse = None


def util_get_trade_calendar():
    """
    获取交易日历,从服务器返回的日期是数字，需要转换为字符串
    :param server_ip:目标服务器地址
    :return: trade_date_sse(list)：交易日历列表
    """
    global trade_date_sse
    if not trade_date_sse:
        token = '07f4c7a56ed3b7a92ab538f994e77e71d59fc47b44177799a1848aeb'
        cal_df = ts.pro_api(token).trade_cal(start_date='20110101')
        trade_dates = sorted(cal_df.loc[cal_df['is_open'] == 1, 'cal_date'].tolist())
        trade_dates = ['-'.join([day[:4], day[4:6], day[6:8]]) for day in trade_dates]
        trade_date_sse = trade_dates
    return


util_get_trade_calendar()


def util_get_real_date(date,  towards=-1):
    """
    获取真实的交易日期,其中,第三个参数towards是表示向前/向后推
    towards=1 日期向后迭代
    towards=-1 日期向前迭代
    @ yutiansut

    """
    global trade_date_sse
    trade_list = trade_date_sse
    if towards == 1:
        while date not in trade_list:
            date = str(dtm.datetime.strptime(
                str(date)[0:10], '%Y-%m-%d') + dtm.timedelta(days=1))[0:10]
        else:
            return str(date)[0:10]
    elif towards == -1:
        while date not in trade_list:
            date = str(dtm.datetime.strptime(
                str(date)[0:10], '%Y-%m-%d') - dtm.timedelta(days=1))[0:10]
        else:
            return str(date)[0:10]


def util_date_gap(date, gap, methods):
    '''
    获取当前日期之前（后）的第n个交易日
    :param date: 字符串起始日 类型 str eg: 2018-11-11
    :param gap: 整数 间隔多数个交易日
    :param methods:  gt大于 ，gte 大于等于， 小于lt ，小于等于lte ， 等于===
    :return:str
    '''
    def _get_date(date_):
        if methods in ['>', 'gt']:
            return trade_date_sse[trade_date_sse.index(date_) + gap]
        elif methods in ['>=', 'gte']:
            return trade_date_sse[trade_date_sse.index(date_) + gap - 1]
        elif methods in ['<', 'lt']:
            return trade_date_sse[trade_date_sse.index(date_) - gap]
        elif methods in ['<=', 'lte']:
            return trade_date_sse[trade_date_sse.index(date_) - gap + 1]
        elif methods in ['==', '=', 'eq']:
            return date_

    def _get_date2(date_):
        dt = pd.Timestamp(date_)
        if methods in ['>', 'gt']:
            return str((dt + pd.offsets.BDay() * gap).date())
        elif methods in ['>=', 'gte']:
            return str((dt + pd.offsets.BDay() * (gap -1)).date())
        elif methods in ['<', 'lt']:
            return str((dt - pd.offsets.BDay() * gap).date())
        elif methods in ['<=', 'lte']:
            return str((dt - pd.offsets.BDay() * (gap + 1)).date())
        elif methods in ['==', '=', 'eq']:
            return date_

    date_s = str(pd.Timestamp(date).date())
    max_retry = 20
    retry = 0
    while retry < max_retry:
        try:
            target_date = _get_date(date_s)
            break
        except:
            retry += 1
            if methods.startswith('g'):
                date_s = str((pd.Timestamp(date_s) - dtm.timedelta(1)).date())
            elif methods.startswith('l'):
                date_s = str((pd.Timestamp(date_s) + dtm.timedelta(1)).date())
            else:
                return 'wrong date'
    else:
        target_date = _get_date2(date)
    return target_date


def util_get_previous_trade_day(date, n=1):
    """得到前一个交易日"""
    return util_date_gap(date, n, 'lt')


def now_time():
    # ATTN:当日超过20点，当前时间是当天15点，否则是上一交易日15点
    if dtm.datetime.now().hour < 15:
        now_t = util_get_real_date(str(dtm.datetime.today().date() - dtm.timedelta(days=1)), -1) + ' 15:00:00'
    else:
        now_t = util_get_real_date(str(dtm.datetime.today().date()), -1) + ' 15:00:00'

    return now_t


if __name__ == '__main__':
    print(now_time())
    print(now_time()[:10])