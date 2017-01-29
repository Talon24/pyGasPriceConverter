#!/usr/bin/env python3
import sys
import decimal
import requests
import urllib
import re

from decimal import *

def getUnitFactor(UnitFrom, UnitTo):
    UnitList ={'l':1, 'gal':3.785411784 } #Base: Liters
    if UnitFrom in UnitList and UnitTo in UnitList:
        return 1 / Decimal(UnitList[UnitFrom]) * Decimal(UnitList[UnitTo])
    else:
        print('Unsupported unit name!')
        raise Exception('UnitError')

def getCurrencyFactor(CurrencyFrom, CurrencyTo):
    supportedCurrencies = [
    "EUR","USD","JPY","BGN","CZK","DKK","GBP","HUF",
    "PLN","RON","SEK","CHF","NOK","HRK","RUB","TRY",
    "AUD","BRL","CAD","CNY","HKD","IDR","ILS","INR",
    "KRW","MXN","MYR","NZD","PHP","SGD","THB","ZAR"]

    if CurrencyTo in supportedCurrencies and CurrencyFrom in supportedCurrencies:
        Factor = Decimal(1)
        if CurrencyFrom != CurrencyTo:
            url = "http://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml"
            s = urllib.request.urlopen(url)
            xml1 = s.read().decode() #read the xml
            xml2 = xml1.partition("<Cube>")[2].partition("</Cube>")[0]+ "</Cube>" #get relevant part

            # Check if xml readable
            if re.findall("currency",xml2) == []:
                print("No Connection")
                raise Exception('ConnectionError')

            #Convert Currency to Base (EUR)
            if CurrencyFrom != 'EUR':
                line = re.findall("currency=.*" + CurrencyFrom + ".*\'.*\'",xml2)
                Factor = 1 / Decimal(re.findall("\d*\.\d*", line[0])[0])
            else:
                Factor = Factor

            #Convert Base to Goal Currency
            if CurrencyTo != 'EUR':
                line2 = re.findall("currency=.*" + CurrencyTo + ".*\'.*\'",xml2)
                Factor *= Decimal(re.findall("\d*\.\d*", line2[0])[0])

        return Factor

    else:
        print('Unsupported currency name!')
        raise Exception('CurrencyError')
def main():
    if len(sys.argv) >= 6:
        StartValue    = Decimal(sys.argv[1].replace(",",".")) #To get both decimal seperators
        StartCurrency =         sys.argv[2].upper()
        StartUnit     =         sys.argv[3].lower()
        GoalCurrency  =         sys.argv[4].upper()
        GoalUnit      =         sys.argv[5].lower()

        try:
            UnitFactor     = getUnitFactor    (StartUnit, GoalUnit)
            CurrencyFactor = getCurrencyFactor(StartCurrency, GoalCurrency)
        except Exception:
            return 0

        GoalValue = StartValue * UnitFactor * CurrencyFactor

        print(str(StartValue)     + " " + StartCurrency + "/" + StartUnit + " Converts to")
        print(str(GoalValue)[0:6] + " " + GoalCurrency +  "/" + GoalUnit)

if 1 == 1:
    main()
