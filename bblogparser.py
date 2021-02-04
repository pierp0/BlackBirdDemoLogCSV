#!/usr/bin/python

'''
   [ Targets ]
   Spread Entry:  0.80%
   Spread Target: 0.40%



   [ 01/10/2021 20:26:15 ]
   Bitfinex:    36,378.00 / 36,394.00
   Bitstamp:    35,970.00 / 36,029.01
   Gemini:  35,729.72 / 35,955.16
   Kraken:  36,010.10 / 36,010.20
   ----------------------------
   Bitstamp/Bitfinex:    0.97% [target  0.80%, min -0.94%, max  1.10%]   trailing  1.02%  1/1
INFO: Opportunity found but no trade will be generated (Demo mode)
   Gemini/Bitfinex:  1.18% [target  0.80%, min -1.07%, max  1.42%]   trailing  1.34%  1/1
INFO: Opportunity found but no trade will be generated (Demo mode)
    Kraken/Bitfinex:    -0.17% [target  0.80%, min -0.35%, max -0.09%]

WARNING: 8 second(s) too late at 01/08/2021 22:20:42
'''

import os
import re


def lineIsDate(line):
    if re.match("^\s*\[\s{1}\d{2}\/\d{2}\/\d{4}\s{1}\d{2}\:\d{2}\:\d{2}\s{1}\]\s*$", line):
        return True
    return False


def lineIsTargets(line):
    if "[ Targets ]" in line:
        return True
    return False


def lineIsAnExchange(line):
    return True


# Get all files in local dir
fileList = os.listdir("./")
block = {}

# for every file check if it's a blackbird_log file
for file in fileList:
    if "blackbird_log" in file:
        with open(file, 'r') as logFile:
            # Read the file content
            fileContent = logFile.readlines()
            # For every line
            for linePtr in range(0, len(fileContent)):
                # Check if it's a block date
                if lineIsDate(fileContent[linePtr]):
                    dt = fileContent[linePtr].strip(" ").strip("[").strip("]").split()
                    block['date'] = dt[0].strip()
                    block['time'] = dt[1].strip()
                    linePtr += 1
                    block['exchange'] = {}
                    print(block['date'])
                    print(block['time'])
                    while "----------------------------" not in fileContent[linePtr]:
                        if lineIsAnExchange(fileContent[linePtr]):
                            exc = fileContent[linePtr].replace(" ", "").replace("\t", "").replace(
                                ",", "").replace(".", ",").replace("/", ":").strip().split(":")
                            block['exchange'] = {exc[0]: {"bid": exc[1], "ask": exc[2]}}

                elif lineIsTargets(fileContent[linePtr]):
                    linePtr += 1
                    if "Spread Entry" in fileContent[linePtr]:
                        block['sentry'] = fileContent[linePtr].replace(
                            "Spread Entry:  ", "").replace("%", "").strip()
                    else:
                        pass  # Error control
                    linePtr += 1
                    if "Spread Target" in fileContent[linePtr]:
                        block['starget'] = fileContent[linePtr].replace(
                            "Spread Target: ", "").replace("%", "").strip()
                    else:
                        pass  # Error control
                else:
                    pass


'''
class block():
    pass

class exchange():

    def __init__(self, name, bid, ask):
        self.name = name
        self.bid = setBid(bid)
        self.ask = setAsk(ask)

    def setBid():

    def setAsk():
        pass
'''
