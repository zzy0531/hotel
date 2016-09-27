#encoding:utf-8
import requests
from bs4 import BeautifulSoup
import re
# import autoprice

Default_Header = {'X-Requested-With': 'XMLHttpRequest',
                  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                'rv:39.0) Gecko/20100101 Firefox/39.0',
                  'Host': 'www.mafengwo.cn'}
_session = requests.session()
_session.headers.update(Default_Header) 

hotelIndexFile = open('config.txt','r')
hotelIndexLines = hotelIndexFile.readlines()

BASE_URL = 'http://www.mafengwo.cn/hotel/'

def readhotelListPage(hotelIndex,hotelName,db):
        hotelUrl = 'http://www.mafengwo.cn/hotel/' + str(hotelIndex) + '.html'
        hotelContent = BeautifulSoup(_session.get(hotelUrl).content)
        hotelList = []
        briefInfo = hotelContent.find('div',attrs={'class':'exp'})
        h_star = hotelContent.find('span',attrs={'class':re.compile(r'(?<=icon-bg hotel-star star)')})
        h_address = hotelContent.find('div',attrs={'class':'location'})
        h_baseInfo = hotelContent.findAll('span',attrs={'class':'content'})[0:3]
        h_ul = hotelContent.findAll('ul',attrs={'class':'facility-item clearfix'})[0]
        h_ul_soup = BeautifulSoup(str(h_ul))
        h_ul_li = h_ul_soup.findAll('li')
        h_dl = hotelContent.find('div',attrs={'id':'_j_description'})
        h_nump1 = hotelContent.findAll('div',attrs={'class':re.compile(r'(?<=num p)')})
        
        try:    
            hotelList.append(str(h_star['class'][-1])[-1:])
        except:
            hotelList.append(str(0))
            
            
        h_brief = ''
        try:
            try:    
                h_brief = briefInfo.text.encode('utf-8').strip('\n').split('\n')[4].replace(' ','')
            except:
                h_brief = briefInfo.text.encode('utf-8').strip('\n').replace(' ','')
        except:
            pass
        hotelList.append(h_brief)
        
        
        try:
            hotelList.append(h_address.text[3:-4].encode('utf-8'))
        except:
            hotelList.append('noValue')
            
        try:
            if ':00' in h_baseInfo[0].text.encode('utf-8'):
                hotelList.append(h_baseInfo[0].text.encode('utf-8'))
            else:
                hotelList.append('noValue')
        except:
            hotelList.append('noValue')
            
        try:    
            if ':00' in h_baseInfo[1].text.encode('utf-8'):
                hotelList.append(h_baseInfo[1].text.encode('utf-8'))
            else:
                hotelList.append('noValue')
        except:
            hotelList.append('noValue')
                
        try:
            if '年' in h_baseInfo[2].text.encode('utf-8'):
                hotelList.append(h_baseInfo[2].text.encode('utf-8'))
            else:
                hotelList.append('noValue')
        except:
            hotelList.append('noValue')
                
        
            
        
        h_res_ul = []
        for i in h_ul_li:
            try:
                h_res_ul.append(i.text.encode('utf-8'))
            except:
                hotelList.append('noValue')
        
        if '免费wifi' in h_res_ul:
            hotelList.append('1')
        else:
            hotelList.append('0')
        
        if '免费停车场' in h_res_ul:
            hotelList.append('1')
        else:
            hotelList.append('0')
        
        if '接送机' in h_res_ul:
            hotelList.append('1')
        else:
            hotelList.append('0')
            
        try:   
            hotelList.append(h_dl.text.encode('utf-8').strip('\n').replace('酒店攻略\n',''))
        except:
            hotelList.append('noValue')
        
        
        for i in [0,2,4,5]:
            try:
                hotelList.append(str("%.1f" %(float(h_nump1[i].text.encode('utf-8'))*0.5)))
            except:
                hotelList.append(str("%.1f" %0.0))
                
                
        
        useSql01 = 'update T_04_001 set C007 = "' + hotelList[2] + '" , C020 = ' + hotelList[0] + ',C009 = ' + hotelList[10] +',C010 = '+hotelList[11] + ',C011 = ' +hotelList[12] + ',C012 = '+hotelList[13] + ',C013 = "'+hotelList[1] + '",C023 = "' + hotelList[3] +'",C024=' + hotelList[8] + ',C025 = ' + hotelList[6] + ',C026 = ' + hotelList[7]+ ' where C002 = "' + hotelName + '"'
        print useSql01
#         autoprice.updateSql(db, useSql01)
        useSql02 = 'update T_04_002 set C003 = ' + hotelList[5][0:4] + ',C004 = ' + hotelList[5][0:4] + ',C005 = "' + hotelList[9] + '" where C002 = ' + hotelName
#         autoprice.updateSql(db, useSql02)
        
if __name__=='__main__':
#     db = autoprice.ConnectDB('stmtest')
    db = ''
    for i in hotelIndexLines:
        detailHotel = i.strip('\n').split('|')
        readhotelListPage(str(detailHotel[1]),detailHotel[0],db)
#     autoprice.Close(db)
        
