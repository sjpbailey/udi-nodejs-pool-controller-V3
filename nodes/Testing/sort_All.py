import requests
import json


x = requests.get('http://192.168.1.53:4200/config/circuits/')
# print(json.dumps(x.json(), indent=4, sort_keys=True))

# "http://192.168.1.53:4200/state/all/"
# "http://192.168.1.53:4200/state/temps/"
y = requests.get("http://192.168.1.53:4200/state/all/")
# print(y.text)
response = (json.dumps(y.json(), indent=4, sort_keys=True))

# print(response)


z = requests.get("http://192.168.1.53:4200/state/temps/")
# print(json.dumps(z.json(), indent=4, sort_keys=True))
# for temps in z:
#    print(temps[0])
# print(z.text)


a = requests.get("http://192.168.1.53:4200/state/pump/1")
# print(json.dumps(a.json(), indent=4, sort_keys=True))

# "http://192.168.1.53:4200/state/circuits/"
u = requests.get("http://192.168.1.53:4200/state/circuit/6/")
# print(json.dumps(u.json(), indent=4, sort_keys=True))
# print(u.text)


p = requests.get("http://192.168.1.53:4200/config/options/schedules/")
# print(json.dumps(p.json(), indent=4, sort_keys=True))
# print(p.text)
# "http://192.168.1.53:4200/config/options/schedules/"
# "http://192.168.1.53:4200/config/options/bodies/"

data = {
    "alias": "Backyard",
    "appVersion": "8.0.1",
    "appVersionState": {
        "equipmentType": "appVersion",
        "gitLocalBranch": "master",
        "gitLocalCommit": "a2e1e75549b1246b3757d7deb7f1ddabeb702d92",
        "githubRelease": "8.0.2",
        "installed": "8.0.1",
        "nextCheckTime": "2024-02-25T23:50:02.867-0800",
        "status": {
            "desc": "New version available",
            "name": "behind",
            "val": 1
        }
    },
    "batteryVoltage": 0,
    "chemControllers": [],
    "chemDosers": [],
    "chlorinators": [],
    "circuitGroups": [],
    "circuits": [
        {
            "action": {
                "desc": "Ready",
                "name": "ready",
                "val": 0
            },
            "endTime": "2024-02-25T09:20:51.782-0800",
            "equipmentType": "circuit",
            "freezeProtect": False,
            "id": 6,
            "isActive": True,
            "isOn": False,
            "manualPriorityActive": False,
            "name": "Pool",
            "priority": "manual",
            "showInFeatures": False,
            "startDelay": False,
            "stopDelay": False,
            "type": {
                "body": 1,
                "desc": "Pool",
                "hasHeatSource": True,
                "name": "pool",
                "val": 12
            }
        }
    ],
    "clockMode": {
        "name": "12 Hour",
        "val": 12
    },
    "clockSource": {
        "desc": "Server",
        "name": "server",
        "val": 3
    },
    "controllerType": "nixie",
    "covers": [],
    "delay": {},
    "delays": [],
    "equipment": {
        "bootLoaderVersion": "",
        "controllerType": "nixie",
        "dual": False,
        "equipmentType": "equipment",
        "maxBodies": 1,
        "maxCircuitGroups": 16,
        "maxCircuits": 40,
        "maxFeatures": 32,
        "maxHeaters": 16,
        "maxLightGroups": 16,
        "maxPumps": 16,
        "maxSchedules": 100,
        "maxValves": 32,
        "messages": [
            {
                "code": "rs485:0:connection",
                "createDate": "2024-02-24T21:13:19.765-0800",
                "message": "Primary RS485 port disconnected",
                "type": {
                    "desc": "Error",
                    "icon": "fas fa-triangle-exclamation",
                    "name": "error",
                    "val": 4
                }
            }
        ],
        "model": "Nixie Single Body",
        "shared": False,
        "single": True,
        "softwareVersion": "1.0.0"
    },
    "features": [],
    "filters": [
        {
            "body": {
                "desc": "Pool",
                "name": "pool",
                "val": 0
            },
            "cleanPercentage": 100,
            "equipmentType": "filter",
            "filterType": {
                "desc": "Cartridge",
                "hasBackwash": False,
                "name": "cartridge",
                "val": 1
            },
            "id": 1,
            "isOn": False,
            "name": "Filter 1",
            "pressure": 0,
            "pressureUnits": {
                "desc": "Pounds per Sqare Inch",
                "name": "psi",
                "val": 0
            },
            "refPressure": 0
        }
    ],
    "freeze": False,
    "heaters": [
        {
            "bodyId": 0,
            "endTime": "2024-02-24T22:48:39.691-0800",
            "equipmentType": "heater",
            "id": 256,
            "isOn": False,
            "name": "Heater 1",
            "shutdownDelay": False,
            "startTime": "2024-02-24T21:21:04.574-0800",
            "startupDelay": False,
            "type": {
                "desc": "Gas Heater",
                "hasAddress": False,
                "name": "gas",
                "val": 1
            }
        }
    ],
    "lightGroups": [],
    "mode": {
        "desc": "Auto",
        "name": "auto",
        "val": 0
    },
    "model": "Nixie Single Body",
    "nextSunrise": "2024-02-25T14:32:43.000-0800",
    "nextSunset": "2024-02-25T01:44:04.000-0800",
    "pumps": [
        {
            "address": 96,
            "circuits": [
                {
                    "circuit": {
                        "action": {
                            "desc": "Ready",
                            "name": "ready",
                            "val": 0
                        },
                        "endTime": "2024-02-25T09:20:51.782-0800",
                        "equipmentType": "circuit",
                        "freezeProtect": False,
                        "id": 6,
                        "isActive": True,
                        "isOn": False,
                        "manualPriorityActive": False,
                        "name": "Pool",
                        "priority": "manual",
                        "showInFeatures": False,
                        "startDelay": False,
                        "stopDelay": False,
                        "type": {
                            "body": 1,
                            "desc": "Pool",
                            "hasHeatSource": True,
                            "name": "pool",
                            "val": 12
                        }
                    },
                    "id": 1,
                    "master": 1,
                    "speed": 2200,
                    "units": {
                        "desc": "RPM",
                        "name": "rpm",
                        "val": 0
                    }
                }
            ],
            "command": 0,
            "driveState": 255,
            "equipmentType": "pump",
            "flow": 0,
            "id": 50,
            "isActive": True,
            "maxFlow": 130,
            "maxSpeed": 3450,
            "minFlow": 15,
            "minSpeed": 450,
            "mode": 0,
            "name": "Pump 1",
            "ppc": 0,
            "pumpOnDelay": False,
            "rpm": 0,
            "status": {
                "desc": "Ok",
                "name": "ok",
                "val": 0
            },
            "time": 1241,
            "type": {
                "desc": "Intelliflo VSF",
                "hasAddress": True,
                "maxCircuits": 8,
                "maxFlow": 130,
                "maxSpeed": 3450,
                "minFlow": 15,
                "minSpeed": 450,
                "name": "vsf",
                "val": 4
            },
            "watts": 0
        }
    ],
    "schedules": [
        {
            "circuit": {
                "action": {
                    "desc": "Ready",
                    "name": "ready",
                    "val": 0
                },
                "endTime": "2024-02-25T09:20:51.782-0800",
                "equipmentType": "circuit",
                "freezeProtect": False,
                "id": 6,
                "isActive": True,
                "isOn": False,
                "manualPriorityActive": False,
                "name": "Pool",
                "priority": "manual",
                "showInFeatures": False,
                "startDelay": False,
                "stopDelay": False,
                "type": {
                    "body": 1,
                    "desc": "Pool",
                    "hasHeatSource": True,
                    "name": "pool",
                    "val": 12
                }
            },
            "clockMode": {
                "name": "12 Hour",
                "val": 12
            },
            "coolSetpoint": 100,
            "display": {
                "desc": "Always",
                "name": "always",
                "val": 0
            },
            "endTime": 840,
            "endTimeType": {
                "desc": "Manual",
                "name": "manual",
                "val": 0
            },
            "equipmentType": "schedule",
            "heatSetpoint": 78,
            "heatSource": {
                "desc": "No Change",
                "name": "nochange",
                "val": 32
            },
            "id": 1,
            "isOn": False,
            "manualPriorityActive": False,
            "scheduleDays": {
                "days": [
                    {
                        "bitval": 64,
                        "desc": "Sunday",
                        "dow": 0,
                        "name": "sun"
                    },
                    {
                        "bitval": 32,
                        "desc": "Saturday",
                        "dow": 6,
                        "name": "sat"
                    },
                    {
                        "bitval": 16,
                        "desc": "Friday",
                        "dow": 5,
                        "name": "fri"
                    },
                    {
                        "bitval": 8,
                        "desc": "Thursday",
                        "dow": 4,
                        "name": "thu"
                    },
                    {
                        "bitval": 4,
                        "desc": "Wednesday",
                        "dow": 3,
                        "name": "wed"
                    },
                    {
                        "bitval": 2,
                        "desc": "Tuesday",
                        "dow": 2,
                        "name": "tue"
                    },
                    {
                        "bitval": 1,
                        "desc": "Monday",
                        "dow": 1,
                        "name": "mon"
                    }
                ],
                "val": 127
            },
            "scheduleTime": {
                "calculated": True,
                "calculatedDate": "2024-02-24T00:00:00.000-0800",
                "endTime": "2024-02-25T14:00:59.999-0800",
                "shouldBeOn": False,
                "startTime": "2024-02-25T10:00:00.000-0800"
            },
            "scheduleType": {
                "days": "multi",
                "desc": "Repeats",
                "endTime": True,
                "heatSetpoint": True,
                "heatSource": True,
                "name": "repeat",
                "startDate": False,
                "startTime": True,
                "val": 128
            },
            "startDate": "2024-02-02T00:00:00.000-0800",
            "startTime": 600,
            "startTimeType": {
                "desc": "Manual",
                "name": "manual",
                "val": 0
            },
            "triggered": False
        }
    ],
    "startTime": "2024-02-24T21:13:19.595-0800",
    "status": {
        "desc": "Ready",
        "name": "ready",
        "percent": 100,
        "val": 1
    },
    "sunrise": "2024-02-24T14:34:02.000-0800",
    "sunset": "2024-02-24T01:43:03.000-0800",
    "systemUnits": {
        "desc": "English",
        "name": "english",
        "val": 0
    },
    "temps": {
        "air": 67.8,
        "bodies": [
            {
                "circuit": 6,
                "heatMode": {
                    "desc": "Heater",
                    "name": "heater",
                    "val": 2
                },
                "heatStatus": {
                    "desc": "Off",
                    "name": "off",
                    "val": 0
                },
                "heaterCooldownDelay": False,
                "heaterOptions": {
                    "gas": 1,
                    "heatpump": 0,
                    "hybrid": 0,
                    "mastertemp": 0,
                    "maxetherm": 0,
                    "solar": 0,
                    "total": 1,
                    "ultratemp": 0
                },
                "id": 1,
                "isCovered": False,
                "isOn": False,
                "name": "Pool",
                "setPoint": 78,
                "showInDashboard": True,
                "startDelay": False,
                "stopDelay": False,
                "temp": 69.89,
                "type": {
                    "desc": "Pool",
                    "name": "pool",
                    "val": 0
                }
            }
        ],
        "equipmentType": "temps",
        "units": {
            "desc": "Fahrenheit",
            "name": "F",
            "val": 0
        },
        "waterSensor1": 68.08,
        "waterSensor2": 0
    },
    "time": "2024-02-24T23:55:00.814-0800",
    "valve": 0,
    "valveMode": {},
    "valves": [],
    "virtualCircuits": [
        {
            "equipmentType": "virtualCircuit",
            "id": 244,
            "isActive": True,
            "isOn": False,
            "name": "Pool Heater",
            "type": {
                "desc": "Pool Heater",
                "name": "poolHeater",
                "val": 244
            }
        },
        {
            "equipmentType": "virtualCircuit",
            "id": 246,
            "isActive": True,
            "isOn": False,
            "name": "Freeze",
            "type": {
                "desc": "Freeze",
                "name": "freeze",
                "val": 246
            }
        },
        {
            "equipmentType": "virtualCircuit",
            "id": 247,
            "isActive": True,
            "isOn": False,
            "name": "Pool/Spa",
            "type": {
                "desc": "Pool/Spa",
                "name": "poolSpa",
                "val": 247
            }
        },
        {
            "equipmentType": "virtualCircuit",
            "id": 258,
            "isActive": True,
            "isOn": False,
            "name": "Any Heater",
            "type": {
                "desc": "Any Heater",
                "name": "anyHeater",
                "val": 258
            }
        }
    ]
}


print()
print("Pool Location {}".format(data["alias"]))
print()
print("App Version {}".format(data["appVersion"]))
print()
print("Schedule {}".format(data["schedules"][0]))
print()
# ["name"]))
print("Pool Name {}".format(data["schedules"][0]["circuit"]["name"]))

"""print()

print("Air Temp {}".format(data["air"]))
print()
print("Water Temp {}".format(data["waterSensor1"]))
print()

print("Circuit {}".format(data["bodies"][0]["circuit"]))
print("ID {}".format(data["bodies"][0]["id"]))
print("Heater Name {}".format(data["bodies"][0]["heatMode"]["name"]))
print()
print("Setpoint {}".format(data["bodies"][0]["setPoint"]))
print("Temperature {}".format(data["bodies"][0]["temp"]))
print()

print("Heat Options Gas {}".format(data["bodies"][0]["heaterOptions"]["gas"]))
print()
print("Heat Options HeatPump {}".format(
    data["bodies"][0]["heaterOptions"]["heatpump"]))
print()
print("Heat Options Hybrid {}".format(
    data["bodies"][0]["heaterOptions"]["hybrid"]))
print()
print("Heat Options MasterTemp {}".format(
    data["bodies"][0]["heaterOptions"]["mastertemp"]))
print()
print("Heat Options Maxetherm {}".format(
    data["bodies"][0]["heaterOptions"]["maxetherm"]))
print()
print("Heat Options Solar {}".format(
    data["bodies"][0]["heaterOptions"]["solar"]))
print()
print("Heat Options Ultratemp {}".format(
    data["bodies"][0]["heaterOptions"]["ultratemp"]))
print()
print("Total Heaters {}".format(data["bodies"][0]["heaterOptions"]["total"]))
print()
# print(data["bodies"][0])


# print(data["heater"]["name"])
# print(data["setpoint"])


# Closing file
# f.close()"""
