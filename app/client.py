import requests

ipaddr = "http://127.0.0.1:5000/"
test = {id: 123, username: 'smari', email: 'nowy@mai.om'}
# GET user
print(requests.get('{}user/kw'.format(ipaddr)).text)

# delete user
delete = requests.delete(ipaddr + "/user/kw")
print(delete.text)

# post user
# post = requests.post(ipaddr + "/user/kw", json=test)


# put
put = requests.put(ipaddr + '/user/nowy', json=test)
