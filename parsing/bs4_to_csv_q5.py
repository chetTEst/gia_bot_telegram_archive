import sqlite3
import requests
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from bs4 import BeautifulSoup
import time
#f=open('q5.csv','w')
font = ImageFont.truetype(font='Times.dfont',size=20, index=0, encoding='')


headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }

def unpack_line(line_1):
    line_1 = line_1.replace('\'','')
    els = line_1.split(';')
    # выделяем имя, емейл, адрес и телефон
    file_u=els[2]
    text1_u=els[3]
    text2_u = els[4]
    right_answer_u = els[5]
    wrong_answer_u = els[6]
    memorial_u = els[7]
    return file_u, text1_u, text2_u, right_answer_u, wrong_answer_u, memorial_u

def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text

def parse_data_bs(filename):
    i=1
    k=1
    results = []
    answer=[]
    text = read_file(filename)
    soup = BeautifulSoup(text)
    question_list=soup.find('div', {'class': 'prob_list'})
    items = question_list.find_all('div', {'class': 'prob_view'})
    for item in items:
        texts_p=item.find('div',{'class':'pbody'})
        #текст вопроса
        if k<37:
            text1=texts_p.next.text
        texts=texts_p.find_all('p',{'class':'left_margin'})
        if k<37:
            try:
                text2=texts[1].text
            except BaseException:
                pass
        else:
            try:
                text2=texts[2].text
                text1=texts[1].text
            except BaseException:
                pass
        texts.reverse()
        #варианты ответа
        try:
            answer.append(texts[3].text[3:].replace(',','.'))
            answer.append(texts[2].text[3:].replace(',','.'))
            answer.append(texts[1].text[3:].replace(',','.'))
            answer.append(texts[0].text[3:].replace(',','.'))
        except BaseException:
            pass
        text_ra=item.find('div',{'class':'answer'})
        #номер правильного ответа
        try:
            ra = int(text_ra.next.text[-1])
        except IndexError:
            ra=0
        try:
            right_answer=answer[ra-1]
            del answer[ra-1]
        except BaseException:
            pass

        wrong_answer=','.join(answer)
        url_tag=item.find('img')
        try:
            url_tag['src']
            url_img='https://inf-oge.sdamgia.ru'+str(url_tag['src'])
        except BaseException:
            url_img='http://jhkjhkjhsdf.tu'
        try:
            img =requests.get(url_img, headers = headers)
            if img.status_code==200:
                print ('OK:200')
                with open('img/z5/'+str(k)+'.png','wb') as imgfile:
                    print ('imgfile.write')
                    imgfile.write(img.content)
        except BaseException:
            url_img='None file'
        table=texts_p.find('table')
        trs=table.find_all('tr')
        img_c = Image.new("RGB", (802, 228))
        base_img=Image.open('img/base_5.png')
        inter_img=Image.open('img/z5/'+str(k)+'.png')
        w, h = inter_img.size
        img_c.paste(base_img, (0, 0))
        w=int(w*1.5)
        h=int(h*1.5)
        size= (w,h)
        inter_img=inter_img.resize(size)
        img_c.paste(inter_img, (560, 10))
        draw = ImageDraw.Draw(img_c)
        # добавляем текст
        tds=trs[1].find_all('td')
        x=115
        y=57
        for i in range(1,5):
            try:
                draw.text((x,y), tds[i].text, (0,0,0), font)
            except BaseException:
                pass
            x+=102
        tds=trs[2].find_all('td')
        x=115
        y=98
        for i in range(1,5):
            try:
                draw.text((x,y), tds[i].text, (0,0,0), font)
            except BaseException:
                pass
            x+=102
        img_c.save('img/z5/'+str(k)+'to_in_one'+'.png', 'PNG')
        img_c.close()
        base_img.close()
        inter_img.close()
        print('img save')
        memorial_div=item.find('div',{'class':'nobreak solution'})
        memorial_p=memorial_div.find_all('p')
        memorial=''
        j=0
        for memorial_text in memorial_p:
            if j==len(memorial_p)-2:
                break
            memorial_try=str(memorial_text)
            try:
                memorial_try=memorial_try.replace('<b>Пояснение.</b>','')
            except BaseException:
                pass
            try:
                memorial_try=memorial_try.replace('<p class=\"left_margin\">','')
            except BaseException:
                pass
            try:
                memorial_try=memorial_try.replace('</p>','')
            except BaseException:
                pass
            try:
                memorial_try=memorial_try.replace('<center>','')
            except BaseException:
                pass
            try:
                memorial_try=memorial_try.replace('</center>','')
            except BaseException:
                pass
            try:
                memorial_try=memorial_try.replace('<sup>','^')
            except BaseException:
                pass
            try:
                memorial_try=memorial_try.replace('</sup>','')
            except BaseException:
                pass
            try:
                memorial_try=memorial_try.replace('<p>','')
            except BaseException:
                pass
            try:
                memorial_try=memorial_try.replace('<i>','')
            except BaseException:
                pass
            try:
                memorial_try=memorial_try.replace('</i>','')
            except BaseException:
                pass
            j+=1
            memorial=memorial+memorial_try+' '
        memorial=memorial[memorial.find('у:')+3:]
        memorial=memorial.replace('\n\n','\n')
        memorial=memorial.replace(';','.')
        memorial=memorial.replace('\n',' ')
        memorial=memorial.replace('  ',' ')
        wrong_answer=wrong_answer.replace(' ,',',')
        wrong_answer=wrong_answer.replace(', ',',')
        text1=text1[:text1.find('1)')]
        if url_img!='None file':
            url_img='img/z5/'+str(k)+'to_in_one'+'.png'
        f.write(str(k)+';'+str(ra)+';'+url_img+';'+text1+';'+text2+';'+right_answer+';'+wrong_answer+';'+memorial+'\n')
        i=i+1
        k+=1
        print (k)
        answer.clear()
        #time.sleep(1)
#parse_data_bs('test5.html')
#f.close()
f=open('q5.csv','r')
lines = f.readlines()
db = sqlite3.connect('inf9gia.db')
cursor = db.cursor()
sql="""DROP TABLE IF EXISTS `question5`"""
cursor.execute(sql)
db.commit()
sql="""CREATE TABLE IF NOT EXISTS `question5` (
    `id`    INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    `file`  TEXT,
    `text1` TEXT,
    `text2` TEXT,
    `right_answer`  TEXT,
    `wrong_answer`  TEXT,
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
    file1, text1, text2, right_answer, wrong_answer, memorial = unpack_line(str(line))
    print (unpack_line(line))
    # подставляем эти данные в SQL-запрос
    sql = """INSERT INTO question5(file, text1, text2, right_answer, wrong_answer, memorial)
    VALUES ('%(file)s','%(text1)s','%(text2)s', '%(right_answer)s', '%(wrong_answer)s', '%(memorial)s')
    """%{"file":file1,"text1":text1,"text2":text2, "right_answer":right_answer, "wrong_answer":wrong_answer, "memorial":memorial}
    # исполняем SQL-запрос
    cursor.execute(sql)
    # применяем изменения к базе данных
    db.commit()
 
# закрываем соединение с базой данных
db.close()
# закрываем файл
f.close()
