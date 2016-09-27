#encoding:utf-8
import requests
import datetime
import re
from bs4 import BeautifulSoup

Default_Header = {
                  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                'rv:39.0) Gecko/20100101 Firefox/39.0'}
_session = requests.session()
_session.headers.update(Default_Header) 

hotelIndexFile = open('config.txt','r')
hotelIndexLines = hotelIndexFile.readlines()

hotelUrlFile = open('config-mao.txt','r')
hotelUrlLines = hotelUrlFile.readlines()

hotelIndexQunar = open('config-qunar.txt','r')
hotelIndexQunarLines = hotelIndexQunar.readlines()
for i in hotelIndexQunarLines:
    detailHotel = i.strip('\n').split('|')
    hotelIndex = detailHotel[1]
    hotelName = detailHotel[0]
    hotelSuffix = ''
    tempUrlList = hotelIndex.split('_')
    if len(tempUrlList) == 2:
           hotelSuffix = tempUrlList[0] + '/dt-' + tempUrlList[1]
    else:
        hotelSuffix = tempUrlList[0] + '_' +tempUrlList[1] + '/dt-' + tempUrlList[2]
    hotelUrl = 'http://hotel.qunar.com/city/' + hotelSuffix
    htmlSoup = BeautifulSoup(_session.get(hotelUrl,timeout=3).content)
    citeList = htmlSoup.findAll('cite')
    hotelTel = '025-52361101'
    
    tempList = []
    for cite in citeList:
        tempList.append(cite.text.encode('utf-8').strip('\n').replace(' ','').replace('(',''))
    signIndex = tempList.index('带有')
    areaName = '附近无商圈、区域'
    areaName = '、'.join(tempList[0:signIndex])
    hotelDecoration = '暂无数据'
    for cite in tempList:
        if '电话' in cite:
            hotelTel = cite.replace('电话','')
        if '装修' in cite:
            hotelDecoration = cite[0:4]
    TelSql = 'update T_04_001 set C006 = "' + hotelTel + '" ,C005 = "' + areaName +'" where C002 = "' + hotelName + '"'
    DecorationSql = 'update T_04_002 set C004 = "' +  hotelDecoration +'" where C002 = "' + hotelName + '"'
    print TelSql
    print DecorationSql