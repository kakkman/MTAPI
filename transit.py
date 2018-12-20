import json, requests, time
from threading import Event, Thread
from datetime import datetime, timedelta
import colorama
import sys

url = "http://127.0.0.1:5000/by-id/"

NUMBER_OF_STATIONS = 3


def getStation(station, line):
    req = requests.get(url+station)
    json_data = json.loads(req.text)

    name = json_data["data"][0]["name"]
    print(name)

    northBound = json_data["data"][0]["N"]
    southBound = json_data["data"][0]["S"]

    outputNorth = ["North Bound"] + formatOutput(northBound, line)
    outputSouth = ["South Bound"] + formatOutput(southBound, line)

    if len(outputNorth) < len(outputSouth):
        outputNorth.extend(" " * (len(outputSouth) - len(outputNorth)))
    else:
        outputSouth.extend(" " * (len(outputNorth) - len(outputSouth)))

    for line in zip(outputNorth, outputSouth):
        print('{:20}{}'.format(*line))

    print("")

def formatOutput(train, line):

    #set number of prints
    totalPrinted = 0

    output = []

    for index, tuple in enumerate(train):
        time = datetime.strptime(train[index]["time"].rsplit("-", 1)[0], "%Y-%m-%dT%H:%M:%S")
        timeUntil = time - datetime.now()

        if datetime.now() < time and timeUntil > timedelta(seconds=30):
            timeUntil = str(time - datetime.now()).rsplit(".", 1)[0].split(":", 1)[1]
        else:
            timeUntil = "Arriving Now"

        if train[index]["route"] in line or line == "":
            output.append(str(train[index]["route"] + " : " + timeUntil))
            totalPrinted += 1
        if totalPrinted == NUMBER_OF_STATIONS:
            break
    return output


def clear():
    print("\x1b[2J")


def put_cursor(x,y):
    print("\x1b[{};{}H".format(y+1,x+1))


def main():
    colorama.init()

    secondAve = "2468"
    Bleecker = "31e9"
    while True:
        getStation(secondAve, "")
        getStation(Bleecker, "6")
        time.sleep(5)
        clear()
        put_cursor(0, 0)


if __name__ == "__main__":
    main()
