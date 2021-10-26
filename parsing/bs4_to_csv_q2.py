import sqlite3
from bs4 import BeautifulSoup
#f=open('q2.csv','w')

def unpack_line(line_1):
    line_1 = line_1.replace('\'','')
    els = line_1.split(';')
    # выделяем имя, емейл, адрес и телефон
    text2_u = els[2]
    right_answer_u = els[3]
    wrong_answer_u = els[4]
    memorial_u = els[5]
    right_answer_u=right_answer_u.replace(' ','')
    memorial_u=memorial_u.replace(' {n}','{n}')
    memorial_u=memorial_u.replace('{n} {n}','{n}')
    memorial_u=memorial_u.replace('{n}{n}','{n}')
    memorial_u=memorial_u.replace('{n}','\n')
    memorial_u=memorial_u.replace('  ',' ')
    return text2_u, right_answer_u, wrong_answer_u, memorial_u

def read_file(filename):
    with open(filename) as input_file:
        text = input_file.read()
    return text

def parse_data_bs(filename):
    i=1
    results = []
    answer=[]
    text = read_file(filename)
    soup = BeautifulSoup(text)
    question_list=soup.find('div', {'class': 'prob_list'})
    items = question_list.find_all('div', {'class': 'prob_view'})
    for item in items:
        texts_p=item.find('div',{'class':'pbody'})
        #текст вопроса
        text1=texts_p.next.text
        texts=texts_p.find_all('p')
        try:
            text1=text1+' '+texts[1].text
        except AttributeError:
            pass
        try:
            text1=text1+' '+texts[2].text
        except AttributeError:
            pass
        texts.reverse()
        #варианты ответа
        answer.append(texts[3].text[3:].replace(',','.'))
        answer.append(texts[2].text[3:].replace(',','.'))
        answer.append(texts[1].text[3:].replace(',','.'))
        answer.append(texts[0].text[3:].replace(',','.'))
        text_ra=item.find('div',{'class':'answer'})
        #номер правильного ответа
        try:
            ra = int(text_ra.next.text[-1])
        except IndexError:
            ra=0
        right_answer=answer[ra-1]
        memorial_answer=[answer[0],answer[1],answer[2],answer[3]]
        del answer[ra-1]
        wrong_answer=','.join(answer)
        memorial_div=item.find('div',{'class':'nobreak solution'})
        memorial_p=memorial_div.find_all('p')
        memorial=''
        for memorial_text in memorial_p:
            memorial=memorial+memorial_text.text+'{n}'
        memorial=memorial.replace('\n\n','\n')
        memorial=memorial.replace(';','.')
        memorial=memorial.replace('\n','{n}')
        memorial=memorial.replace('  ',' ')
        memorial=memorial.replace('1)',memorial_answer[0]+' - ')
        memorial=memorial.replace('2)',memorial_answer[1]+' - ')
        memorial=memorial.replace('3)',memorial_answer[2]+' - ')
        memorial=memorial.replace('4)',memorial_answer[3]+' - ')
        wrong_answer=wrong_answer.replace(' ,',',')
        wrong_answer=wrong_answer.replace(', ',',')
        text1=text1[:text1.find('1)')]
        f.write(str(i)+';'+str(ra)+';'+text1+';'+right_answer+';'+wrong_answer+';'+memorial+'\n')
        i+=1
        answer.clear()
#parse_data_bs('test2.html')
#f.close()
f=open('q2.csv','r')
lines = f.readlines()
db = sqlite3.connect('inf9gia.db')
cursor = db.cursor()
sql="""DROP TABLE IF EXISTS `question2`"""
cursor.execute(sql)
db.commit()
sql="""CREATE TABLE IF NOT EXISTS `question2` (
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
    text2, right_answer, wrong_answer, memorial = unpack_line(str(line))
    print (unpack_line(line))
    # подставляем эти данные в SQL-запрос
    sql = """INSERT INTO question2(text2, right_answer, wrong_answer, memorial)
    VALUES ('%(text2)s', '%(right_answer)s', '%(wrong_answer)s', '%(memorial)s')
    """%{"text2":text2, "right_answer":right_answer, "wrong_answer":wrong_answer, "memorial":memorial}
    # исполняем SQL-запрос
    cursor.execute(sql)
    # применяем изменения к базе данных
    db.commit()
 
# закрываем соединение с базой данных
db.close()
# закрываем файл
f.close()
