"""Simple client- app example how can methods be used"""
# !/usr/bin/env python3
import argparse
import json
import sys
from enum import Enum

import requests


class Method(Enum):
    post = "post"
    put = "put"
    get = "get"
    delete = "delete"


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
URL = "http://127.0.0.1:5000/" + 'anns/' + str(ann_id)


##### MANUAL
## CRUD FOR RICHARDSON SECOND CRITERIA
# post- create -> work
# post = requests.post(URL, json=test)

# get - read -> work
# get = requests.get(URL)

# put - update - > work
# put = requests.put(URL, json=test_modified)

# delete - delete -> work
# delete = requests.delete(URL)


##### AUTO
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ip', type=str,
                        help='A required string server URL argument')
    parser.add_argument('method', type=Method,
                        help='A required string post/get/put/delete argument')
    parser.add_argument('--index', type=int,
                        help='A required string /132')
    parser.add_argument('--filename', type=str)
    args = parser.parse_args()

    if args.ip:
        ipaddr = args.ip
    else:
        ipaddr = "http://127.0.0.1:5000/"

    # GETS
    if Method.get is args.method:
        link = ipaddr + 'anns'
        if args.index:
            link = ipaddr + 'anns/' + str(args.index)
        get = requests.get(link)
        return get.text

    # DELETE
    elif Method.delete is args.method and args.index:
        link = ipaddr + 'anns/' + str(args.index)
        delete = requests.delete(link)
        return delete.text

    if args.filename:
        with open(args.filename) as f:
            d = json.load(f)
        # PUT
        if Method.put is args.method:
            if 'id' not in d.keys() and not args.index:
                sys.stderr.write('You need to input id of the announce yuo wanna edit in dile or type id by --index ID')
                return
            if args.index:
                d['id'] = str(args.index)
            link = ipaddr + 'anns/' + str(d['id'])
            put = requests.put(link, json=d)
            return put.text

        # POSTS
        elif Method.post is args.method:
            link = ipaddr + 'anns'
            if args.index:
                link += '/' + args.index
            post = requests.post(link, json=d)
            return post.text
        else:
            sys.stderr.write('METHOD --url URL(IFNOT127...) --filename FILENAME --index ID')
            return
    else:
        sys.stderr.write('METHOD --url URL(IFNOT127...) --filename FILENAME --index ID')


main()
