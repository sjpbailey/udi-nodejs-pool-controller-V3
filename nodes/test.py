import asyncio
import aiohttp
import requests

from poolcontrolpy.poolcontrolpy import Controller


async def checkconnection():

    async with aiohttp.ClientSession() as client:
        controller = Controller(client, "192.168.1.53", 4200)
        return await controller.checkconnect()


resp = asyncio.run(checkconnection())
print(resp)
# Get all data from nodejs pool controller api
