import requests
import time

class uploader:
  def __init__(self, blog_name, access_token):
    self._blog_type = '1' #1 tistory 2 naver 3 google
    self._blog_name = blog_name
    self._access_token = access_token
    self._output_type = 'json'
    self._visibility = 0
    self.published = time.time()
    


  def upload_tistory(self, title, content, visibility, category, tags):
    url = 'https://www.tistory.com/apis/post/write'
    data = {'access_token':self._access_token,\
            'output':self._output_type,\
            'blogName':self._blog_name,\
            'title':title,\
            'content':content,\
            'visibility':visibility,\
            'category':category,\
            'published':self.published,\
            'tag':tags}

    requests.post(url,data=data)

