from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime, timedelta

class contents_generator:
  def __init__(self):
    self.pytrends = TrendReq(hl='ko-KR', tz=540)
    self.contents = ''
    self.tags = ''
    now = datetime.now()
    self.end_dt = now.strftime("%Y-%m-%d")
    self.start_dt = (now - timedelta(days=7)).strftime("%Y-%m-%d")

  def gen_trend(self):
    df = self.pytrends.trending_searches(pn='south_korea')
    return df

  def gen_tags(self,keyword):
    kw_list = [keyword]
    self.pytrends.build_payload(kw_list, timeframe=self.start_dt + ' ' + self.end_dt, geo="KR")
    df = self.pytrends.related_queries()

    result_top = pd.concat([df[kw]['top'] for kw in kw_list], axis=0)
    result_top = result_top.sort_values(by='value',ascending=False).reset_index(drop=True)

    tags = ''
    tags_size=1

  
    if len(result_top) > 9:
      tags_size = 10
    else:
      tags_size = len(result_top)

    for i in result_top['query']:
      tags += i
      if tags_size == 0:
        break
      elif tags_size == 1:
        tags_size -= 1
      else:
        tags_size -= 1
        tags = tags + ','
    
    self.tags=tags

    return self.tags
