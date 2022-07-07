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


@app.route('/upload')
def receive_data ():


if __name__ == '__main__':
    app.run()
