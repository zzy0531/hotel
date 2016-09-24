#http://www.mafengwo.cn/hotel/ajax.php?sAction=getBookingInfo&poi_id=5330&check_in=2016-10-23&check_out=2016-10-24&booking_flag=hotel_new
#encoding:utf-8
import requests
import datetime
from bs4 import BeautifulSoup
import xlwt
Default_Header = {
                  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                'rv:39.0) Gecko/20100101 Firefox/39.0'}
_session = requests.session()
_session.headers.update(Default_Header) 

hotelIndexFile = open('config.txt','r')
hotelIndexLines = hotelIndexFile.readlines()

book = xlwt.Workbook(encoding='utf-8')
sheet1 = book.add_sheet('Sheet 1')

BASE_URL = 'http://www.mafengwo.cn/hotel/ajax.php?sAction=getBookingInfo&poi_id='

def getPrice(poi_id,countnum):
    now_time = datetime.datetime.now()
    tomo_time = now_time + datetime.timedelta(days=+1)
    tomo_time_nyr = tomo_time.strftime('%Y-%m-%d')
    now_time_nyr = now_time.strftime('%Y-%m-%d')
    pageUrl = BASE_URL + str(poi_id) + '&check_in=' + now_time_nyr + '&check_out=' + tomo_time_nyr + '&booking_flag=hotel_new'
    pageUrlJson = _session.get(pageUrl).json()
    priceSoup = BeautifulSoup(pageUrlJson['html'])
    lowestPrice =  priceSoup.findAll('strong',attrs={'class':'_j_booking_price'})
    
    hotelLowestPrice = 100000
    
    try:
        for everyprice in lowestPrice:
            everyprice = str(everyprice.text[1:].encode('utf-8'))
            if int(everyprice) < int(hotelLowestPrice):
                hotelLowestPrice = int(everyprice)
                
        print poi_id,hotelLowestPrice
    except:
        hotelLowestPrice = 'noValue'
    sheet1.write(countnum,0,poi_id)
    sheet1.write(countnum,1,hotelLowestPrice)
    book.save('f:\demoprice03.xls')
    
if __name__=='__main__':
    countnum = 0
    for hotelIndex in hotelIndexLines:
        if hotelIndex.strip('\n') == '33333333333333333333333333333333333':
            print '============================'
        else:
            countnum = countnum + 1
            hotelList = hotelIndex.split('/')
            hotelId = hotelList[len(hotelList)-1].split('.')[0]
            getPrice(hotelId.strip('\n'),countnum)
    
