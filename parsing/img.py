'''
Эта программа демонстрирует работу с загрузкой изображения по URL
'''
import requests
#Формирование хедера для "Обмана" сервера и маскировки под обычный браузер
headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }
#Получение изображения по URL
img =requests.get('https://inf-oge.sdamgia.ru/get_file?id=2699', headers = headers)
#Если изобрадение существует и сайте вернул сообщение ОК
if img.status_code==200:
	print ('OK:200')
	with open('img/z3/1.png','wb') as imgfile:
		#Сохраняем изображение
		imgfile.write(img.content)