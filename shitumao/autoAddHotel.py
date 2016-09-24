#encoding:utf-8
import requests
import datetime
from bs4 import BeautifulSoup
import MySQLdb

Default_Header = {
                  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                'rv:39.0) Gecko/20100101 Firefox/39.0'}
_session = requests.session()
_session.headers.update(Default_Header) 

hotelIndexFile = open('config.txt','r')
hotelIndexLines = hotelIndexFile.readlines()

BASE_URL = 'http://www.mafengwo.cn/hotel/ajax.php?sAction=getBookingInfo&poi_id='

def getPrice(poi_id,hotelName,stm):
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
    except:
        hotelLowestPrice = 10000
        
    update(stm,hotelName,hotelLowestPrice,'C021')
    print hotelName,poi_id,hotelLowestPrice
    
def getFac(hotelName,hotelUrl,stm):
    hotelHtmlSoup = BeautifulSoup(_session.get(hotelUrl).content)
    ulContent = hotelHtmlSoup.find('ul',attrs={'class':'property_tags'})
    ulSoup = BeautifulSoup(str(ulContent))
    liList = ulSoup.findAll('li')
    facStr = ''
    
    for everyli in liList:
        print everyli.text.strip('\n')+';',
        facStr = facStr + everyli.text.strip('\n')+';'
    
    update(stm,hotelName,facStr,'C022')
    print hotelName,facStr,hotelUrl
    
        
def ConnectDB(DBName):
    '''连接时指定数据库名'''
    return MySQLdb.connect('','test','test',DBName,charset='utf8')

def Close(db):
    """关闭数据库连接"""
    db.close()

def update(db,hotelName,hotelLowestPrice,c_column):
    sql = 'update T_04_001 set ' + c_column + ' = ' + str(hotelLowestPrice) + ' where C002 = ' + hotelName
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        
def updateprice():
    stm = ConnectDB('stmtest')
    for i in hotelIndexLines:
        detailHotel = i.strip('\n').split('|')
        getPrice(detailHotel[1],detailHotel[0],stm)
    Close(stm)
    
def updateFac():
    stm = ConnectDB('stmtest')
    for i in hotelIndexLines:
        detailHotel = i.strip('\n').split('|')
        getPrice(detailHotel[1],detailHotel[0],stm)
    Close(stm) 
        
if __name__=='__main__':
    selectVal = raw_input('请选择：1、添加价格2、添加设施')
    if selectVal == '1':
        updateprice()
    else:
        updateFac()
