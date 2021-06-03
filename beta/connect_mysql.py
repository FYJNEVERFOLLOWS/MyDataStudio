# !/usr/bin/python3

import pymysql
import const

class myDBC():
    def __init__(self):
        super(myDBC, self).__init__()

    def select(self, sql):
        # 打开数据库连接
        db = pymysql.connect(host=const.MYSQL_HOST, user=const.MYSQL_USER, password=const.MYSQL_PASSWD, database="azams")

        # 使用cursor()方法获取操作游标
        cursor = db.cursor()
        print("connect_mysql:\n" + sql)

        # SQL 查询语句
        # sql = "SELECT * FROM sig_stock"
        try:
            # 执行SQL语句
            cursor.execute(sql)
            # 使用 fetchone() 方法获取单条数据.
            # data = cursor.fetchone()
            # 获取所有记录列表
            results = cursor.fetchall()
            list_cols = []
            for field_desc in cursor.description:
                list_cols.append(field_desc[0])
            return results, list_cols
            # for row in results:
            #     print(row)
                # id = row[0]
                # code = row[1]
                # amount = row[2]
                # part = row[3]
                # date = row[4]
                # product_id = row[5]
                # # 打印结果
                # print("id=%d,code=%s,amount=%f,part=%d,date=%s,product_id=%s" % \
                #       (id, code, amount, part, date,product_id))
        except:
            return "Error:", "unable to fetch data"

        # 关闭数据库连接
        db.close()

if __name__ == "__main__":
    dbc = myDBC()
    # results, cols= dbc.select("SELECT * FROM acc_equity WHERE date_format(date,'%Y-%m-%d') >= '2021-01-01' and date_format(date,'%Y-%m-%d') <= '2021-04-19'")
    results, cols= dbc.select("SELECT * FROM  WHERE date_format(date,'%Y-%m-%d') >= '2021-05-01' and date_format(date,'%Y-%m-%d') <= '2021-04-19'")
    print(results, cols)
    # dbc.select("SELECT * FROM pdt_deposit")
    # dbc.select("SELECT * FROM pos_futures")
    # dbc.select("SELECT * FROM sig_stock")