import requests
import json


x = requests.get('http://192.168.1.53:4200/config/circuits/')
# print(json.dumps(x.json(), indent=4, sort_keys=True))


y = requests.get("http://192.168.1.53:4200/state/all/")
# print(json.dumps(y.json(), indent=4, sort_keys=True))

# print(type(y))

# z = requests.get("http://192.168.1.53:4200/temperatures")
# print(json.dumps(z.json(), indent=4, sort_keys=True))
# print(z.text)


a = requests.get("http://192.168.1.53:4200/config/options/pumps/")
# print(json.dumps(a.json(), indent=4, sort_keys=True))


u = requests.get("http://192.168.1.53:4200/state/circuit/setState/")
# print(json.dumps(u.json(), indent=4, sort_keys=True))
# print(u.text)


p = requests.get("http://192.168.1.53:4200/config/options/bodies/")
print(json.dumps(p.json(), indent=4, sort_keys=True))
# print(p.text)
for i in p:
    print(i[1])
