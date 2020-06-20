"""Simple client- app example how can methods be used"""
import requests

ipaddr = "http://127.0.0.1:5000/"
test = {
    "name": "nowy item",
    "body": "bodyss",
    "price": 120,
    "user_id": 2
}

test_modified = {
    "name": "zmofydikowany item",
    "body": "zmodyfikowane body",
    "price": 70,
    "user_id": 2
}
ann_id = 174  # new announce id
URL = ipaddr + '/anns/' + str(ann_id)

## CRUD FOR RICHARDSON SECOND CRITERIA
# post- create -> work
post = requests.post(URL, json=test)

# get - read -> work
# get = requests.get(URL)

# put - update - > work
# put = requests.put(URL, json=test_modified)

# delete - delete -> work
# delete = requests.delete(URL)
