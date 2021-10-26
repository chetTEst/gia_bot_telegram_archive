# -*- coding: utf-8 -*-
import requests
url = 'https://inf-oge.sdamgia.ru/test?theme=18' # url для второй страницы
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
r = requests.get(url, headers = headers)
with open('test18.html', 'w') as output_file:
	output_text=r.text.replace(u'\u00A0',' ')
	output_text=output_text.replace(u'\u2007',' ')
	output_text=output_text.replace('\xa0',' ')
	output_text=output_text.replace(u'\u202F',' ')
	output_text=output_text.replace(u'\u000A','')
	output_file.write(output_text.replace(u'\u00AD',''))
