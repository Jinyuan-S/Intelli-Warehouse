from flask import Flask, request
import json
from database import *

app = Flask(__name__)
db_info = {'user': 'root', 'password': 'Cqmyg1sdss', 'host': '127.0.0.1', 'database': 'Warehouse', 'charset': 'utf8'}
db = Database(db_info)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


@app.route('/user', methods=['POST'])
def user():
    req = request.json
    ret = {}
    if req['type'] == 'login':
        rows, user_info = db.query('SELECT * FROM Worker WHERE workerId="%s"' % (req['id']))
        if rows == 1 and user_info[0][5] == req['pwd']:
            ret['status'] = 0  # 正常
            ret['result'] = user_info[0]  # [[101, "Mona", "Jabber", "2015-07-06", "male", "654321", 1]]
        elif rows == 0:
            ret['status'] = 102  # 用户不存在
            ret['result'] = []
        else:
            ret['status'] = 101  # 用户密码错误
            ret['result'] = []
    elif req['type'] == 'changepwd':
        rows, user_info = db.query('UPDATE Worker SET pwd="%s" WHERE workerId="%s"' % (req['newpwd'], req['id']))
        if rows == 1:
            ret['status'] = 0  # 正常
            rows, user_info = db.query('SELECT * FROM Worker WHERE workerId="%s"' % (req['id']))
            ret['result'] = user_info[0]  # [[101, "Mona", "Jabber", "2015-07-06", "male", "654321", 1]]
        else:  # rows = 0
            ret['status'] = 102  # 用户不存在
            ret['result'] = []
    elif req['type'] == 'changeinfo':
        for i in req['info']:
            db.query('UPDATE Worker SET "%s"="%s" WHERE workerId="%s"' % (i, req['info'][i], req['id']))
        rows, user_info = db.query('SELECT * FROM Worker WHERE workerId="%s"' % (req['id']))
        ret['status'] = 0
        ret['result'] = user_info[0]  # 返回更新后的信息
    return json.dumps(ret, default=str)


@app.route('/inquire', methods=['POST'])
def inquire():
    req = request.json
    ret = {}

    def expand(query_records):
        for record_info in query_records:
            shelf_record = list(record_info.items())[3:]
            for single_record in shelf_record:
                r, shelf_info = db.query('SELECT * FROM Shelf WHERE shelfNo="%d";' % (single_record[1]), isdic=True)
                record_info[single_record[0]] = shelf_info[0]
        return query_records

    if req['type'] == 'now':
        rows, records = db.query('SELECT * FROM Records WHERE houseId="%s" ORDER BY datetime DESC LIMIT 1'
                                 % (req['houseId']), True)
        if rows == 0:
            ret['status'] = 201  # 此仓库暂无记录
            ret['result'] = []
        else:
            records = expand(records)
            ret['status'] = 0
            ret['result'] = records[0]

    elif req['type'] == 'interval':
        rows, records = db.query('SELECT * FROM Records WHERE houseId=1 AND datetime>="%s" \
                AND datetime<="%s" ORDER BY datetime DESC;' % (req['from'], req['to']), True)
        # print(records)
        if rows == 0:
            ret['status'] = 202  # 此仓库暂无记录
            ret['result'] = []
        else:
            records = expand(records)
            ret['status'] = 0
            ret['result'] = records
    return json.dumps(ret, default=str)


@app.route('/upload', methods=['POST'])
def receive_data ():
    req = request.json
    ret = {}

    def add_record(data):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # db = Database(info)
        db.query('INSERT INTO Records (houseId, datetime) VALUES ("%d", "%s")' % (data[0], timestamp))  # 创建一个record

        # 拿到刚插入的recordNo
        rows, record_no = db.query(
            'SELECT recordNo FROM Records WHERE houseId="%d" AND datetime="%s"' % (data[0], timestamp))
        shelf_nos = []
        for i in data[1:]:
            # print(i)
            db.query(
                'INSERT INTO Shelf (position, recordNo, g1, g2, g3, g4, g5) VALUES ("%s", "%d", "%d", "%d", "%d", "%d", "%d")'
                % (i[0], record_no[0][0], i[1], i[2], i[3], i[4], i[5]))
            rows, shelf_no = db.query(
                'SELECT shelfNo FROM Shelf WHERE position="%s" AND recordNo=%d' % (i[0], record_no[0][0]))
            shelf_nos.append(shelf_no[0][0])

        db.query('UPDATE Records SET A="%d", B="%d", C="%d", D="%d", E="%d", F="%d", G="%d", H="%d", I="%d", J="%d", total="%d" \
                 WHERE recordNo="%d"' % (
        shelf_nos[0], shelf_nos[1], shelf_nos[2], shelf_nos[3], shelf_nos[4], shelf_nos[5],
        shelf_nos[6], shelf_nos[7], shelf_nos[8], shelf_nos[9], shelf_nos[10],
        record_no[0][0]))

    add_record(req)
    ret['status'] = '0'
    return json.dumps(ret, default=str)


@app.route('/test', methods=['POST'])
def testtest ():
    req = request.json
    # head = request.headers
    addr = request.remote_addr
    content_len = request.content_length
    req_date = request.date
    ret = {}
    print(addr)
    print(content_len)
    print(req_date)
    print(request.content_md5)
    return json.dumps(ret, default=str)


if __name__ == '__main__':
    app.run()
