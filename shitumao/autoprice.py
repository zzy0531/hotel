#encoding:utf-8
import requests
import datetime
import re
from bs4 import BeautifulSoup
import MySQLdb

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

MAFENGWO_URL = 'http://www.mafengwo.cn/hotel/'
BASE_URL = 'http://www.mafengwo.cn/hotel/ajax.php?sAction=getBookingInfo&poi_id='
QUNAER_URL = ''

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
    
def getFac(hotelUrl,hotelName,stm):
    hotelHtmlSoup = BeautifulSoup(_session.get(hotelUrl).content)
    ulContent = hotelHtmlSoup.find('ul',attrs={'class':'property_tags'})
    ulSoup = BeautifulSoup(str(ulContent))
    liList = ulSoup.findAll('li')
    facStr = ''
    
    for everyli in liList:
        print everyli.text.strip('\n')+';',
        facStr = facStr + everyli.text.strip('\n').encode('utf-8')+';'
    
    update(stm,hotelName,'"'+facStr+'"','C022')
    print hotelName,facStr,hotelUrl
    
def getStar(hotelIndex,hotelName,stm):
    hotelUrl = MAFENGWO_URL + str(hotelIndex) + '.html'
    h_star = 0
    try:
        hotelContent = BeautifulSoup(_session.get(hotelUrl).content)
        h_star = hotelContent.find('span',attrs={'class':re.compile(r'(?<=icon-bg hotel-star star)')})
        h_star = str(h_star['class'][-1])[-1:]
    except:
        pass
    update(stm,hotelName,h_star,'C020')
    print hotelName,h_star,hotelIndex
    
def getEva(hotelIndex,hotelName,stm):
    hotelUrl = MAFENGWO_URL + str(hotelIndex) + '.html'
    h_brief = ' '
    try:
        hotelContent = BeautifulSoup(_session.get(hotelUrl).content)
        briefInfo = hotelContent.find('div',attrs={'class':'exp'})
        try:
            try:    
                h_brief = briefInfo.text.encode('utf-8').strip('\n').split('\n')[4]
            except:
                h_brief = briefInfo.text.strip('\n')
        except:
            pass
    except:
        pass
    update(stm,hotelName,'"'+h_brief+'"','C013')
    print hotelName,h_brief,hotelIndex
    
def getLongLat(hotelIndex,hotelName,stm):
    try:
        hotel_index = 'http://hotel.qunar.com/eh/locator.jsp?seq='+hotelIndex
        html_index = _session.get(hotel_index).content
        rexx = r"(?<=var bpoint = ').*?(?=';)"
        index = re.findall(rexx, html_index)
        soup = BeautifulSoup(html_index)
        h2 = soup.find('h2')
        LongLatList = index[0].split(',')
        print h2.text,LongLatList[0],LongLatList[1]
        longLatSql = 'update T_04_001 set C018 = ' + LongLatList[0] + ',C019 = ' + LongLatList[1] + ' where C002 = "' + hotelName + '";'
        updateSql(stm, longLatSql)
    except:
        pass
    
    try:
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
        
        updateSql(stm, TelSql)
        updateSql(stm, DecorationSql)
        print h2.text,hotelTel,hotelDecoration,areaName
    except:
        pass
    
        
def ConnectDB(DBName):
    '''连接时指定数据库名'''
    return MySQLdb.connect('','test','test',DBName,charset='utf8')

def Close(db):
    """关闭数据库连接"""
    db.close()

def update(db,hotelName,hotelLowestPrice,c_column):
    sql = 'update T_04_001 set ' + c_column + ' = ' + str(hotelLowestPrice) + ' where C002 = "' + hotelName + '"'
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        
def updateSql(db,commonSql):
    cursor = db.cursor()
    try:
        cursor.execute(commonSql)
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
    for i in hotelUrlLines:
        detailHotel = i.strip('\n').split('|')
        getFac(detailHotel[1],detailHotel[0],stm)
    Close(stm) 
    
def updateStar():
    stm = ConnectDB('stmtest')
    for i in hotelIndexLines:
        detailHotel = i.strip('\n').split('|')
        getStar(detailHotel[1],detailHotel[0],stm)
    Close(stm)
    
def updateEva():
    stm = ConnectDB('stmtest')
    for i in hotelIndexLines:
        detailHotel = i.strip('\n').split('|')
        getEva(detailHotel[1],detailHotel[0],stm)
    Close(stm)
    
def updateLongLat():
    stm = ConnectDB('stmtest')
    for i in hotelIndexQunarLines:
        detailHotel = i.strip('\n').split('|')
        getLongLat(detailHotel[1],detailHotel[0],stm)
    Close(stm)
        
if __name__=='__main__':
    selectVal = raw_input('请选择：1、更新价格\n2、更新设施\n3、更新星级\n4、更新评价\n5、更新坐标和电话\n')
    if selectVal == '1':
        updateprice()
    elif selectVal == '2':
        updateFac()
    elif selectVal == '3':
        updateStar()
    elif selectVal == '4':
        updateEva()
    elif selectVal == '5':
        updateLongLat()
