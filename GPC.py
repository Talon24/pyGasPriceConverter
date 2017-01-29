#!/usr/bin/env python3
import sys
import decimal
import requests
import urllib
import re

from decimal import *

def getUnitFactor(UnitFrom, UnitTo):
    UnitList ={'l':Decimal(1), 'gal':Decimal(3.785411784) } #Base: Liters
    if UnitFrom in UnitList and UnitTo in UnitList:
        return 1 / UnitList[UnitFrom] * UnitList[UnitTo]
    else:
        raise Exception('Unsupported unit name!')

def getCurrencyFactor(CurrencyFrom, CurrencyTo):
    supportedCurrencies = ["EUR","USD","JPY","BGN","CZK","DKK","GBP","HUF","PLN","RON","SEK","CHF","NOK","HRK","RUB","TRY","AUD","BRL","CAD","CNY","HKD","IDR","ILS","INR","KRW","MXN","MYR","NZD","PHP","SGD","THB","ZAR"]
    if CurrencyTo in supportedCurrencies and CurrencyFrom in supportedCurrencies:
        if CurrencyFrom != CurrencyTo:
            url = "http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
            s = urllib.request.urlopen(url)
            contentsXML = s.read()
            xml1 = contentsXML.decode()#.partition('<cube>')
            xml2 = xml1.partition("<Cube>")[2].partition("</Cube>")[0]+ "</Cube>"
            Factor = Decimal(1)

            if CurrencyFrom != 'EUR':
                line = re.findall("currency=.*" + CurrencyFrom + ".*\'.*\'",xml2)
                Factor = 1 / Decimal(re.findall("\d*\.\d*", line[0])[0])
            else:
                Factor = Factor
            if CurrencyTo != 'EUR':
                line2 = re.findall("currency=.*" + CurrencyTo + ".*\'.*\'",xml2)
                Factor *= Decimal(re.findall("\d*\.\d*", line2[0])[0])
            else:
                Factor *= 1
        else:
            Factor = 1
        return Factor
    else:
        raise Exception('Unsupported currency name!')
def main():
    if len(sys.argv) == 6:
        StartValue = Decimal(sys.argv[1].replace(",",".")) #To get both decimal seperators
        StartCurrency = sys.argv[2].upper()
        StartUnit = sys.argv[3]
        GoalCurrency = sys.argv[4].upper()
        GoalUnit = sys.argv[5]

        try:
            UnitFactor = getUnitFactor        (StartUnit, GoalUnit)
            CurrencyFactor = getCurrencyFactor(StartCurrency, GoalCurrency)
        except:
            print("Error")
            return 0

        GoalValue = StartValue * UnitFactor * CurrencyFactor

        print(str(GoalValue) + " " + GoalCurrency + " per " + str(GoalUnit))

if 1 == 1:
    main()
