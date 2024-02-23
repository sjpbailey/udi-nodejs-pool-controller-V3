import asyncio
import aiohttp
import requests
import json

"""from poolcontrolpy.poolcontrolpy import Controller


async def checkconnection():

    async with aiohttp.ClientSession() as client:
        controller = Controller(client, "192.168.1.53", 4200)
        return await controller.checkconnect()


resp = asyncio.run(checkconnection())
print(resp)
# Get all data from nodejs pool controller api"""

x = requests.get('http://192.168.1.53:4200/config/circuits/')

# print(x.text)


y = requests.get("http://192.168.1.53:4200/state/all/")
# y = json.dumps(y)
print(type(y))
print(y.text)

print(type(y))

z = requests.get("http://192.168.1.53:4200/state/pump/1/")

# print(z.text)
