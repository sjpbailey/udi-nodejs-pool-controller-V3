import requests
import json


x = requests.get('http://192.168.1.53:4200/config/circuits/')
# print(json.dumps(x.json(), indent=4, sort_keys=True))

# "http://192.168.1.53:4200/state/all/"
# "http://192.168.1.53:4200/state/temps/"
y = requests.get("http://192.168.1.53:4200/state/all/")
# print(y.text)
response = (json.dumps(y.json(), indent=4, sort_keys=True))

print(response)


# z = requests.get("http://192.168.1.53:4200/temperatures")
# print(json.dumps(z.json(), indent=4, sort_keys=True))
# print(z.text)


a = requests.get("http://192.168.1.53:4200/state/pump/1")
# print(json.dumps(a.json(), indent=4, sort_keys=True))


u = requests.get("http://192.168.1.53:4200/state/circuit/setState/")
# print(json.dumps(u.json(), indent=4, sort_keys=True))
# print(u.text)


p = requests.get("http://192.168.1.53:4200/config/options/schedules/")
# print(json.dumps(p.json(), indent=4, sort_keys=True))
# print(p.text)
# "http://192.168.1.53:4200/config/options/schedules/"
# "http://192.168.1.53:4200/config/options/bodies/"
