import pymysql
import json
import datetime

# info = {'user': 'root', 'password': 'Cqmyg1sdss', 'host': '127.0.0.1', 'database': 'Warehouse', 'charset': 'utf8'}
simple_data = [1, ["A", 2, 0, 0, 0, 0], ["B", 0, 1, 1, 0, 0], ["C", 0, 0, 0, 1, 3], ["D", 0, 2, 0, 0, 0],
               ["E", 0, 0, 2, 0, 0],
               ["F", 1, 0, 0, 0, 0], ["G", 0, 0, 1, 2, 3], ["H", 0, 0, 0, 0, 0], ["I", 1, 0, 2, 0, 0],
               ["J", 1, 1, 1, 1, 1],
               ["all", 5, 4, 7, 4, 7]]


class Database(object):
    __database = None

    def __init__(self, dbinfo):
        """传入一个dictionary存储连接信息"""
        self.database = pymysql.connect(**dbinfo)

    def __del__(self):
        self.database.close()

    def query(self, sql, isdic=False):
        """ 执行sql语句，返回tuple（effect_row, res）"""
        effect_row = None  # 默认None
        res = ()  # 默认空tuple
        if isdic:
            cursor = self.database.cursor(pymysql.cursors.DictCursor)  # 获取字典游标
        else:
            cursor = self.database.cursor()  # 获取游标
        try:
            effect_row = cursor.execute(sql)
            res = cursor.fetchall()
            self.database.commit()  # 提交更改
        except:
            self.database.rollback()  # 如果有错误回滚
            print('Error when executing \"' + sql + '\"\n<already rollback>')
        finally:
            cursor.close()  # 关闭游标
        return effect_row, res


# def test1():
#     db = Database(info)
#     a, res = db.query("SELECT * FROM Records WHERE houseId=1 ORDER BY datetime DESC LIMIT 1", True)
#     print(a)
#     print(res)
#     print(json.dumps(res, default=str))  # default=str可以将datetime格式转成string
#     # trans = json.loads(json.dumps(res, default=str))[0]
#     trans = res[0]
#     print(trans)
#     aaa = list(trans.items())[3:]
#     print(trans.items())
#     for i in aaa:
#         print(i[1])


# test1()
# test2()


# def add_record(data):
#     timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     # db = Database(info)
#     db.query('INSERT INTO Records (houseId, datetime) VALUES ("%d", "%s")' % (data[0], timestamp))  # 创建一个record
#
#     # 拿到刚插入的recordNo
#     rows, record_no = db.query(
#         'SELECT recordNo FROM Records WHERE houseId="%d" AND datetime="%s"' % (data[0], timestamp))
#     shelf_nos = []
#     for i in data[1:]:
#         # print(i)
#         db.query(
#             'INSERT INTO Shelf (position, recordNo, g1, g2, g3, g4, g5) VALUES ("%s", "%d", "%d", "%d", "%d", "%d", "%d")'
#             % (i[0], record_no[0][0], i[1], i[2], i[3], i[4], i[5]))
#         rows, shelf_no = db.query(
#             'SELECT shelfNo FROM Shelf WHERE position="%s" AND recordNo=%d' % (i[0], record_no[0][0]))
#         shelf_nos.append(shelf_no[0][0])
#
#     db.query('UPDATE Records SET A="%d", B="%d", C="%d", D="%d", E="%d", F="%d", G="%d", H="%d", I="%d", J="%d", total="%d" \
#              WHERE recordNo="%d"' % (shelf_nos[0], shelf_nos[1], shelf_nos[2], shelf_nos[3], shelf_nos[4], shelf_nos[5],
#                                      shelf_nos[6], shelf_nos[7], shelf_nos[8], shelf_nos[9], shelf_nos[10],
#                                      record_no[0][0]))

# add_record(simple_data)
