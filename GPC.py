#!/usr/bin/env python3
import sys
import decimal
import requests

from decimal import *


def getUnitFactor(UnitFrom, UnitTo):
    UnitList ={'l':Decimal(1), 'gal':Decimal(3.785411784) } #Base: Liters
    return UnitList[UnitFrom] / UnitList[UnitTo]

def getCurrencyFactor(CurrencyFrom, CurrencyTo):
    #request the ecb for values here
    return 5

def main():
    if len(sys.argv) == 6:
        StartValue = Decimal(sys.argv[1].replace(",",".")) #To get both decimal seperators
        StartCurrency = sys.argv[2].upper()
        StartUnit = sys.argv[3]
        GoalCurrency = sys.argv[4]
        GoalUnit = sys.argv[5]

        UnitFactor = getUnitFactor        (StartUnit, GoalUnit)
        CurrencyFactor = getCurrencyFactor(StartCurrency, GoalCurrency)

        GoalValue = StartValue * UnitFactor * CurrencyFactor
        print(GoalValue)

        #Debug
        print("--------")
        print(sys.argv)
        print(StartValue)
        print(StartUnit)
        print(UnitFactor)


if 1 == 1:
    main()
