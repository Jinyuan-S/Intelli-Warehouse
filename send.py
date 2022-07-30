import requests
import json
import random

# send_data = {'type': 'login', 'id': '101', 'pwd': '123456'}
#
# r = requests.post("http://127.0.0.1:5000/user", json=send_data)
# print(r.text)
# thing = json.loads(r.text)
# print(thing)

# # send_data = {'type': 'now', 'houseId': '1'}
# send_data = {'type': 'interval', 'from': '2022-06-06 17:31:46', 'to': '2022-07-06 17:31:46'}
# r = requests.post("http://127.0.0.1:5000/inquire", json=send_data)
# print(r.text)
# thing = json.loads(r.text)
# print(thing['status'])

send_data = [1, ["A", 2, 1, 0, 0, 0], ["B", 0, 1, 1, 0, 0], ["C", 0, 0, 0, 1, 3], ["D", 0, 2, 0, 0, 0],
               ["E", 0, 0, 2, 0, 10],
               ["F", 1, 0, 0, 0, 0], ["G", 0, 0, 1, 2, 3], ["H", 0, 0, 0, 0, 0], ["I", 1, 0, 2, 0, 0],
               ["J", 1, 1, 1, 1, 1],
               ["all", 5, 5, 7, 4, 17]]
r = requests.post("http://127.0.0.1:5000/test", json=send_data)
print(r.text)
thing = json.loads(r.text)
print(thing)


