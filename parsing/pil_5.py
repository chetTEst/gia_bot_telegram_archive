'''
Эта программа демоснтрирует создание изображения по таблице HTML
'''

#Импортируем библиотеку для парсинга HTML
from bs4 import BeautifulSoup
#Импортируем библиотеки для работы с изображениями
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
#Открываем файл с HTML

font = ImageFont.truetype(font='Times.dfont',size=25, index=0, encoding='')

f=open('123.html','r')
text=f.read()
soup = BeautifulSoup(text)
item=soup.find('div', {'class': 'pbody'})
table=item.find('tbody')
trs=table.find_all('tr')
img = Image.new("RGB", (802, 228))
base_img=Image.open('img/base_5.png')
inter_img=Image.open('img/z5/1.png')
w, h = inter_img.size
img.paste(base_img, (0, 0))
w=int(w*1.5)
h=int(h*1.5)
size= (w,h)
inter_img=inter_img.resize(size)
img.paste(inter_img, (560, 10))
draw = ImageDraw.Draw(img)
# добавляем текст
tds=trs[1].find_all('td')
x=115
y=57
for i in range(1,5):
	draw.text((x,y), tds[i].text, (0,0,0), font)
	x+=102
tds=trs[2].find_all('td')
x=115
y=98
for i in range(1,5):
	draw.text((x,y), tds[i].text, (0,0,0), font)
	x+=102
f.close()
img.save('test.png', 'PNG')


