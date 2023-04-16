from uploader import uploader
from contents_generator import contents_generator
from stock_contents_generator import stock_contents_generator
from datetime import datetime, timedelta

if __name__ == '__main__':
  title = str(datetime.now().strftime("%Y-%m-%d")) + ' 종목분석, 상한가 및 하한가 종목 리스트'
  scg = stock_contents_generator()
  contents=scg.gen_contents_as_html()

  tistory = uploader(blog_name='',access_token='')
  tistory.upload_tistory(title=title, content=contents, visibility=3, category='', tags=scg.get_tags())

  
  
  

  


