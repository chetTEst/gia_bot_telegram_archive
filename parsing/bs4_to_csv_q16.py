import sqlite3
import requests
from bs4 import BeautifulSoup
import time
#f=open('q16.csv','w')

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }

def unpack_line(line_1):
    line_1 = line_1.replace('\'','')
    els = line_1.split(';')
    # выделяем имя, емейл, адрес и телефон
    text2_u=els[1]
    right_answer_u = els[2]
    memorial_u = els[3]
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
    text2_u=text2_u.replace('\t',' ')
    right_answer_u=right_answer_u.replace(' ','')
    right_answer_u=right_answer_u.replace(' ','')
    right_answer_u=right_answer_u.replace(' ','')
    return text2_u, right_answer_u, memorial_u

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
        texts_p=item.find('div',{'class':'pbody'})
        #текст вопроса
        texts=texts_p.find_all('p')
        text1=''
        for i in range(0,len(texts)):
            text1=text1+texts[i].text+'{n}'
        text_ra=item.find('div',{'class':'answer'})
        #номер правильного ответа
        right_answer = text_ra.next.text
        right_answer = right_answer[right_answer.find(':')+1:]

        memorial_div=item.find('div',{'class':'nobreak solution'})
        memorial_p=memorial_div.find_all('p')
        memorial=''
        for memorial_text in memorial_p:
            memorial=memorial+memorial_text.text+'{n}'
        memorial=memorial.replace('\n\n','\n')
        memorial=memorial.replace(';','.')
        memorial=memorial.replace('\n',' ')
        memorial=memorial.replace('  ',' ')
        text1=text1.replace(';','.')
        f.write(str(k)+';'+text1+';'+right_answer+';'+memorial+'\n')
        k+=1
        answer.clear()
        #time.sleep(1)
#parse_data_bs('test16.html')
#f.close()
f=open('q16.csv','r')
lines = f.readlines()
db = sqlite3.connect('inf9gia.db')
cursor = db.cursor()
sql="""DROP TABLE IF EXISTS `question16`"""
cursor.execute(sql)
db.commit()
sql="""CREATE TABLE IF NOT EXISTS `question16` (
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
    text2, right_answer, memorial = unpack_line(str(line))
    # подставляем эти данные в SQL-запрос
    sql = """INSERT INTO question16(text2, right_answer, memorial)
    VALUES ('%(text2)s', '%(right_answer)s', '%(memorial)s')
    """%{"text2":text2, "right_answer":right_answer, "memorial":memorial}
    # исполняем SQL-запрос
    cursor.execute(sql)
    # применяем изменения к базе данных
    db.commit()
 
# закрываем соединение с базой данных
db.close()
# закрываем файл
f.close()