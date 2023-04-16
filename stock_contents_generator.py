import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class stock_contents_generator:
  def __init__(self):
    self.URL = 'https://finance.naver.com/'
    raw = requests.get(self.URL)
    self.html = BeautifulSoup(raw.text,'lxml')
    self.units_up =  self.html.select('#_topItems2>tr')  # up 30% list
    self.units_down =  self.html.select('#_topItems3>tr ') #down 30% list
    self.contents_html = ''
    self.tags = '주식'
    self.today = str(datetime.now().strftime("%Y-%m-%d"))
  


  def gen_contents_as_html(self):
    a=''
    b=''
    a = self.gen_units_up() 
    b = self.gen_units_down()
    return a+b
    

  def gen_units_up(self):
    self.contents_html = self.contents_html + '<br />'
    self.contents_html = '<h2 data-ke-size="size26">'+self.today+'일자 상한가 목록</h2>'
    
    #print('금일 상한가 종목')
    #print()
    
    for unit in self.units_up[:5]:
      self.title_up = unit.select_one('#_topItems2 > tr> th > a').text
      price_up = unit.select_one('#_topItems2 > tr> td')
      up = unit.select_one('#_topItems2 > tr > td:nth-child(3)').text
      percent_up = unit.select_one('#_topItems2 > tr> td:nth-child(4)')
      
      up = up.replace('상한가', '↑')
      
      news_up = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query='+self.title_up
      raw2 = requests.get(news_up)
      html2= BeautifulSoup(raw2.text,'lxml')
      news_up_box = html2.find('div',{'class':'group_news'})
      news_up_list = news_up_box.find_all('div',{'class':'news_area'}) # 박스
      
      #print('종목명:',self.title_up)
      self.tags = self.tags + ',' + self.title_up
      #print('주당 가격:',price_up.text+'원')
      #print('전날 대비 가격 변동:',up)
      #print('전날 대비 등락 :',percent_up.text)

      self.contents_html = self.contents_html + '<p data-ke-size="size16">종목명:&nbsp;<span style="color: #ee2323;">'+self.title_up+'</span> <br />'
      self.contents_html = self.contents_html + '주당&nbsp;가격:&nbsp;<span style="color: #ee2323;">'+price_up.text+'원</span> <br />'
      self.contents_html = self.contents_html + '전날&nbsp;대비&nbsp;가격&nbsp;변동:&nbsp;<span style="color: #ee2323;">&uarr;&nbsp;'+up+'</span> <br />'
      self.contents_html = self.contents_html + '전날&nbsp;대비&nbsp;등락&nbsp;:&nbsp;&nbsp;&nbsp;<span style="color: #ee2323;">+'+percent_up.text+'</span> <br />'
      
      #print('관련 뉴스 기사')
      self.contents_html = self.contents_html + '관련&nbsp;뉴스&nbsp;기사 <br />'
      
      for new in news_up_list[:3]:
          new_title_up = new.find('a',{'class' : 'news_tit'})
          #print('뉴스:',new_title_up.text)
          #self.contents_html = self.contents_html + '뉴스&nbsp;이름:&nbsp;' + new_title_up.text + '<br />'
          
          link_up = new.find('a',{'class' : 'api_txt_lines dsc_txt_wrap'})

          new_up = link_up['href']
          #self.contents_html = self.contents_html + new_up + '<br />'

          self.contents_html = self.contents_html + '뉴스:&nbsp;<a href="' + new_up + '" target="_blank" rel="noopener">' + new_title_up.text + '</a><br />'
          
          #print(new_up)

      self.contents_html = self.contents_html + '</p>'
      #print()
      self.contents_html = self.contents_html + '<p data-ke-size="size16">&nbsp;</p>'

      title_up = unit.select_one('#_topItems2 > tr> th > a')
      chart_up_url = 'https://finance.naver.com'+title_up['href']
      chart_up_raw = requests.get(chart_up_url)
      chart_up_html = BeautifulSoup(chart_up_raw.text,'lxml')
      chart_up = chart_up_html.select_one('#img_chart_area')
      chart_up = chart_up['src']
      chart_up_day = chart_up.replace('area','candle')  #일봉
      chart_up_week = chart_up_day.replace('day','week') #주봉
      chart_up_month = chart_up_day.replace('day','month')#월봉

      self.contents_html = self.contents_html + '<p data-ke-size="size16">일봉 그래프</p>'
      
      self.contents_html = self.contents_html + '<p><img src="' + chart_up_day + '" alt="'+'일봉'+'" /></p>'
      self.contents_html = self.contents_html + '<p data-ke-size="size16">&nbsp;</p>'
      self.contents_html = self.contents_html + '<p data-ke-size="size16">주봉 그래프</p>'
      self.contents_html = self.contents_html + '<p><img src="' + chart_up_week + '" alt="'+'주봉'+'" /></p>'
      self.contents_html = self.contents_html + '<p data-ke-size="size16">&nbsp;</p>'
      self.contents_html = self.contents_html + '<p data-ke-size="size16">월봉 그래프</p>'
      self.contents_html = self.contents_html + '<p><img src="' + chart_up_month + '" alt="'+'월봉'+'" /></p>'
      self.contents_html = self.contents_html + '<p data-ke-size="size16">&nbsp;</p>'
      self.contents_html = self.contents_html + '<p data-ke-size="size16">&nbsp;</p>'
      #print('일봉:',chart_up_day)
      #print('주봉:',chart_up_week)
      #print('월봉:',chart_up_month)
    self.contents_html = self.contents_html + '<br />'

    return self.contents_html

  def get_tags(self):
    return self.tags

  def gen_units_down(self):
    self.contents_html = self.contents_html + '<br />'
    self.contents_html = '<h2 data-ke-size="size26">'+self.today+'일자 하한가 목록</h2>'
    
    #print('금일 하한가 종목')
    #print()
    
    for unit in self.units_down[:5]:
      self.title_down = unit.select_one('#_topItems3 > tr> th > a').text
      price_down = unit.select_one('#_topItems3 > tr> td')
      down = unit.select_one('#_topItems3 > tr > td:nth-child(3)').text
      percent_down = unit.select_one('#_topItems3 > tr> td:nth-child(4)')
      
      down = down.replace('하한가', '↓')
      
      news_down = 'https://search.naver.com/search.naver?sm=tab_hty.top&where=news&query='+self.title_down
      raw2 = requests.get(news_down)
      html2= BeautifulSoup(raw2.text,'lxml')
      news_down_box = html2.find('div',{'class':'group_news'})
      news_down_list = news_down_box.find_all('div',{'class':'news_area'}) # 박스
      
      #print('종목명:',self.title_down)
      self.tags = self.tags + ','+self.title_down
      #print('주당 가격:',price_down.text+'원')
      #print('전날 대비 가격 변동:',down)
      #print('전날 대비 등락 :',percent_down.text)

      self.contents_html = self.contents_html + '<p data-ke-size="size16">종목명:&nbsp;<span style="color: #006dd7;">'+self.title_down+'</span> <br />'
      self.contents_html = self.contents_html + '주당&nbsp;가격:&nbsp;<span style="color: #006dd7;">'+price_down.text+'원</span> <br />'
      self.contents_html = self.contents_html + '전날&nbsp;대비&nbsp;가격&nbsp;변동:&nbsp;<span style="color: #006dd7;">&uarr;&nbsp;'+down+'</span> <br />'
      self.contents_html = self.contents_html + '전날&nbsp;대비&nbsp;등락&nbsp;:&nbsp;&nbsp;&nbsp;<span style="color: #006dd7;">+'+percent_down.text+'</span> <br />'
      
      #print('관련 뉴스 기사')
      self.contents_html = self.contents_html + '관련&nbsp;뉴스&nbsp;기사 <br />'
      
      for new in news_down_list[:3]:
          new_title_down = new.find('a',{'class' : 'news_tit'})
          #print('뉴스:',new_title_down.text)
          #self.contents_html = self.contents_html + '뉴스&nbsp;이름:&nbsp;' + new_title_down.text + '<br />'
          
          link_down = new.find('a',{'class' : 'api_txt_lines dsc_txt_wrap'})

          new_down = link_down['href']
          #self.contents_html = self.contents_html + new_down + '<br />'

          self.contents_html = self.contents_html + '뉴스:&nbsp;<a href="' + new_down + '" target="_blank" rel="noopener">' + new_title_down.text + '</a><br />'
          
          #print(new_down)

      self.contents_html = self.contents_html + '</p>'
      #print()
      self.contents_html = self.contents_html + '<p data-ke-size="size16">&nbsp;</p>'

      title_down = unit.select_one('#_topItems3 > tr> th > a')
      chart_down_url = 'https://finance.naver.com'+title_down['href']
      chart_down_raw = requests.get(chart_down_url)
      chart_down_html = BeautifulSoup(chart_down_raw.text,'lxml')
      chart_down = chart_down_html.select_one('#img_chart_area')
      chart_down = chart_down['src']
      chart_down_day = chart_down.replace('area','candle')  #일봉
      chart_down_week = chart_down_day.replace('day','week') #주봉
      chart_down_month = chart_down_day.replace('day','month')#월봉

      self.contents_html = self.contents_html + '<p data-ke-size="size16">일봉 그래프</p>'
      
      self.contents_html = self.contents_html + '<p><img src="' + chart_down_day + '" alt="'+'일봉'+'" /></p>'
      self.contents_html = self.contents_html + '<p data-ke-size="size16">&nbsp;</p>'
      self.contents_html = self.contents_html + '<p data-ke-size="size16">주봉 그래프</p>'
      self.contents_html = self.contents_html + '<p><img src="' + chart_down_week + '" alt="'+'주봉'+'" /></p>'
      self.contents_html = self.contents_html + '<p data-ke-size="size16">&nbsp;</p>'
      self.contents_html = self.contents_html + '<p data-ke-size="size16">월봉 그래프</p>'
      self.contents_html = self.contents_html + '<p><img src="' + chart_down_month + '" alt="'+'월봉'+'" /></p>'
      self.contents_html = self.contents_html + '<p data-ke-size="size16">&nbsp;</p>'
      self.contents_html = self.contents_html + '<p data-ke-size="size16">&nbsp;</p>'
      #print('일봉:',chart_down_day)
      #print('주봉:',chart_down_week)
      #print('월봉:',chart_down_month)
    self.contents_html = self.contents_html + '<br />'

    return self.contents_html

