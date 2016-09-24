#encoding:utf-8
#http://info.sporttery.cn/football/pool_result.php?m=1
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
import xlwt

Default_Header = {
                  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                'rv:39.0) Gecko/20100101 Firefox/39.0'}
_session = requests.session()
_session.headers.update(Default_Header) 

_session.mount('http://', HTTPAdapter(max_retries=2))#设置超时回滚次数

hotelIndexFile = open('config.txt','r')
hotelIndexLines = hotelIndexFile.readlines()

book = xlwt.Workbook(encoding='utf-8')
sheet1 = book.add_sheet('Sheet 1')

BASE_URL = 'http://www.tripadvisor.cn/'
HOTEL_URL = BASE_URL + 'Hotel_Review-g294220-d4582336-Reviews-Fairmont_Nanjing-Nanjing_Jiangsu.html'

def everyHotel(hotelIndex,countnum):
    hotelUrl = hotelIndex
    hotelHtmlSoup = BeautifulSoup(_session.get(hotelUrl).content)
    ulContent = hotelHtmlSoup.find('ul',attrs={'class':'property_tags'})
    ulSoup = BeautifulSoup(str(ulContent))
    liList = ulSoup.findAll('li')
    
    facStr = ''
    
    for everyli in liList:
        print everyli.text.strip('\n')+';',
        facStr = facStr + everyli.text.strip('\n')+';'
    
    print ''
    
    sheet1.write(countnum,0,hotelIndex)
    sheet1.write(countnum,1,facStr)
    book.save('f:\demofac02.xls')
    
if __name__=='__main__':
    countnum = 0
    for hotelIndex in hotelIndexLines:
        if hotelIndex.strip('\n') == '33333333333333333333333333333333333':
            print '============================'
        else:
            countnum = countnum + 1
            everyHotel(hotelIndex.strip('\n'),countnum)