import requests
import json

# send_data = {'type': 'login', 'id': '101', 'pwd': '123456'}
#
# r = requests.post("http://127.0.0.1:5000/user", json=send_data)
# print(r.text)
# thing = json.loads(r.text)
# print(thing)

# send_data = {'type': 'now', 'houseId': '1'}
send_data = {'type': 'interval', 'from': '2022-06-06 17:31:46', 'to': '2022-07-06 17:31:46'}
r = requests.post("http://127.0.0.1:5000/inquire", json=send_data)
print(r.text)
thing = json.loads(r.text)
print(thing['status'])
