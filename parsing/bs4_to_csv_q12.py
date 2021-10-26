import sqlite3
import requests
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from bs4 import BeautifulSoup
import time
#f=open('q12.csv','w')
font = ImageFont.truetype(font='Times.dfont',size=14, index=0, encoding='')


headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }

def unpack_line(line_1):
    line_1 = line_1.replace('\'','')
    els = line_1.split(';')
    # выделяем имя, емейл, адрес и телефон
    file_u=els[1]
    text1_u=els[2]
    text2_u = els[3]
    right_answer_u = els[4]
    memorial_u = els[5]
    memorial_u=memorial_u.replace(' {n}','{n}')
    memorial_u=memorial_u.replace('{n} {n}','{n}')
    memorial_u=memorial_u.replace('{n}{n}','{n}')
    memorial_u=memorial_u.replace('{n}','\n')
    memorial_u=memorial_u.replace('  ',' ')
    text2_u=text2_u.replace(' {n}','{n}')
    text2_u=text2_u.replace('{n} {n}','{n}')
    text2_u=text2_u.replace('{n}{n}','{n}')
    text2_u=text2_u.replace('{n}','\n')
    text2_u=text2_u.replace('  ',' ')
    right_answer_u=right_answer_u.replace(' ','')
    right_answer_u=right_answer_u.replace(' ','')
    right_answer_u=right_answer_u.replace(' ','')
    return file_u, text1_u, text2_u, right_answer_u, memorial_u

def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text

def parse_data_bs(filename):
    k=1
    results = []
    answer=[]
    text = read_file(filename)
    soup = BeautifulSoup(text)
    question_list=soup.find('div', {'class': 'prob_list'})
    items = question_list.find_all('div', {'class': 'prob_view'})
    for item in items:
        if k==34:
            break
        texts_p=item.find('div',{'class':'pbody'})
        #текст вопроса
        if k<34:
            text1=texts_p.next.text
        texts=texts_p.find_all('p',{'class':'left_margin'})
        text2=''
        for i in range(1,len(texts)):
            text2=text2+texts[i].text+'{n}'
        text_ra=item.find('div',{'class':'answer'})
        #номер правильного ответа
        right_answer = text_ra.next.text
        right_answer = right_answer[right_answer.find(':')+1:]

        table=texts_p.find('table')
        trs=table.find_all('tr')
        img_c = Image.new("RGB", (630, 438))
        base_img=Image.open('img/base_12.png')
        img_c.paste(base_img, (0, 0))
        draw = ImageDraw.Draw(img_c)
        # добавляем текст
        tds_i=1
        for tds in trs:
            if tds_i==1:
                tds_for=tds.find_all('th')
                x=14
                y=19
                for i in range(0,4):
                    try:
                        draw.text((x,y), tds_for[i].text, (0,0,0), font)
                    except BaseException:
                        pass
                    x+=160
            else:
                tds_for=tds.find_all('td')
                x=14
                if tds_i==2:
                    y=52
                for i in range(0,4):
                    try:
                        draw.text((x,y), tds_for[i].text, (0,0,0), font)
                    except BaseException:
                        pass
                    x+=160
            y+=24
            tds_i+=1
        img_c.save('img/z12/'+str(k)+'.png', 'PNG')
        img_c.close()
        base_img.close()
        memorial_div=item.find('div',{'class':'nobreak solution'})
        memorial_p=memorial_div.find_all('p')
        memorial=''
        for memorial_text in memorial_p:
            memorial=memorial+memorial_text.text+'{n}'
        memorial=memorial.replace('\n\n','\n')
        memorial=memorial.replace(';','.')
        memorial=memorial.replace('\n',' ')
        memorial=memorial.replace('  ',' ')
        url_img='img/z12/'+str(k)+'.png'
        f.write(str(k)+';'+url_img+';'+text1+';'+text2+';'+right_answer+';'+memorial+'\n')
        k+=1
        answer.clear()
        #time.sleep(1)
#parse_data_bs('test12.html')
#f.close()
f=open('q12.csv','r')
lines = f.readlines()
db = sqlite3.connect('inf9gia.db')
cursor = db.cursor()
sql="""DROP TABLE IF EXISTS `question12`"""
cursor.execute(sql)
db.commit()
sql="""CREATE TABLE IF NOT EXISTS `question12` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    `file`  TEXT,
    `text1` TEXT,
    `text2` TEXT,
    `right_answer`  TEXT,
    `memorial`  TEXT
)"""
cursor.execute(sql)
db.commit()
for line in lines:
    print (line)
    # если в строе присутствует емейл (определяем по наличию "@")
    # извлекаем данные из строки
    unpack_line_array=unpack_line(str(line))
    print (unpack_line_array)
    file1, text1, text2, right_answer, memorial = unpack_line(str(line))
    print (unpack_line(line))
    # подставляем эти данные в SQL-запрос
    sql = """INSERT INTO question12(file, text1, text2, right_answer, memorial)
    VALUES ('%(file)s','%(text1)s','%(text2)s', '%(right_answer)s', '%(memorial)s')
    """%{"file":file1,"text1":text1,"text2":text2, "right_answer":right_answer, "memorial":memorial}
    # исполняем SQL-запрос
    cursor.execute(sql)
    # применяем изменения к базе данных
    db.commit()
 
# закрываем соединение с базой данных
db.close()
# закрываем файл
f.close()