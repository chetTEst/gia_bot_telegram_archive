import sqlite3
from bs4 import BeautifulSoup
#f=open('q4.csv','w')

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
    results = []
    answer=[]
    text = read_file(filename)
    soup = BeautifulSoup(text)
    question_list=soup.find('div', {'class': 'prob_list'})
    items = question_list.find_all('div', {'class': 'prob_view'})
    for item in items:
        texts_p=item.find('div',{'class':'pbody'})
        #текст вопроса
        texts=texts_p.find_all('p',{'class':'left_margin'})
        try:
            text1=str(texts[0])
            text2=str(texts[1])
        except BaseException:
            pass
        file_text=texts_p.find('center')
        try:
            file_p=str(file_text.next)
        except BaseException:
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
        del answer[ra-1]
        wrong_answer=','.join(answer)
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
            try:
                memorial_try=memorial_try.replace('<b>','')
            except BaseException:
                pass
            try:
                memorial_try=memorial_try.replace('</b>','')
            except BaseException:
                pass
            j+=1
            memorial=memorial+memorial_try+' '
        try:
            text1=text1.replace('<p class=\"left_margin\">','')
        except BaseException:
            pass
        try:
            text1=text1.replace('</p>','')
        except BaseException:
            pass
        try:
            text2=text2.replace('<p class=\"left_margin\">','')
        except BaseException:
            pass
        try:
            text2=text2.replace('</p>','')
        except BaseException:
            pass
        try:
            file_p=file_p.replace('<p>','')
        except BaseException:
            pass
        try:
            file_p=file_p.replace('</p>','')
        except BaseException:
            pass
        try:
            text1=text1.replace('<!--auto generated from answers--','')
        except BaseException:
            pass
        try:
            text2=text2.replace('<!--auto generated from answers-->','')
        except BaseException:
            pass
        
        memorial=memorial.replace('\n\n','\n')
        memorial=memorial.replace(';','.')
        memorial=memorial.replace('\n',' ')
        memorial=memorial.replace('  ',' ')
        wrong_answer=wrong_answer.replace(' ,',',')
        wrong_answer=wrong_answer.replace(', ',',')
        text1=text1[:text1.find('1)')]
        f.write(str(i)+';'+str(ra)+';'+file_p+';'+text1+';'+text2+';'+right_answer+';'+wrong_answer+';'+memorial+'\n')
        i+=1
        answer.clear()
#parse_data_bs('test4.html')
#f.close()
f=open('q4.csv','r')
lines = f.readlines()
db = sqlite3.connect('inf9gia.db')
cursor = db.cursor()
sql="""DROP TABLE IF EXISTS `question4`"""
cursor.execute(sql)
db.commit()
sql="""CREATE TABLE IF NOT EXISTS `question4` (
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
    # если в строе присутствует емейл (определяем по наличию "@")
    # извлекаем данные из строки
    unpack_line_array=unpack_line(str(line))
    file1, text1, text2, right_answer, wrong_answer, memorial = unpack_line(str(line))
    # подставляем эти данные в SQL-запрос
    sql = """INSERT INTO question4(file, text1, text2, right_answer, wrong_answer, memorial)
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
