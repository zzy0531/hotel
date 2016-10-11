#encoding:utf-8
import re
tempFile = open('temp.txt','r')
tempLines = tempFile.readlines()
rexx = r'(?<=code:")[A-Z]{3}(?=")'
rex_name = r'(?<=name:)'
for x in tempLines:
    tempList = re.findall(rexx,x)
    for i in tempList:
        print i