import sqlite3
from bs4 import BeautifulSoup
#f=open('q8.csv','w')

def unpack_line(line_1):
    line_1 = line_1.replace('\'','')
    els = line_1.split(';')
    # выделяем имя, емейл, адрес и телефон
    file_u=els[1]
    file_u=file_u.replace(' {n}','{n}')
    file_u=file_u.replace('{n} {n}','{n}')
    file_u=file_u.replace('{n}{n}','{n}')
    file_u=file_u.replace('{n}','\n')
    file_u=file_u.replace('  ',' ')
    text1_u=els[2]
    text2_u = els[3]
    right_answer_u = els[4]
    right_answer_u=right_answer_u.replace(' ','')
    memorial_u = els[5]
    memorial_u=memorial_u.replace('{n}','\n')
    return file_u, text1_u, text2_u, right_answer_u, memorial_u

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
        if i<41:
            try:
                text1=texts[0].text
                text2=texts[1].text
            except BaseException:
                pass
        else:
            try:
                text1=texts[0].text+' '+texts[1].text
                text2=texts[2].text
            except BaseException:
                pass
        
        file_text=texts_p.find_all('p')
        file_p=''
        m=0
        #print (len(file_text))
        len_file_text=len(file_text)-1
        for file_p_text in file_text:
            if i<41:
                if m!=0 and m<len_file_text:
                    try:
                        print (str(m)+'   '+str(len_file_text))
                        file_p=file_p+file_p_text.text+'{n}'
                    except BaseException:
                        pass
            else:
                if m>2 and m<len_file_text:
                    try:
                        print (str(m)+'   '+str(len_file_text))
                        file_p=file_p+file_p_text.text+'{n}'
                    except BaseException:
                        pass

            m+=1
        text_ra=item.find('div',{'class':'answer'})
        #номер правильного ответа
        right_answer = text_ra.next.text
        right_answer = right_answer[right_answer.find(':')+1:]
        memorial_div=item.find('div',{'class':'nobreak solution'})
        memorial_p=memorial_div.find_all('p')
        memorial=''
        n=0
        for memorial_text in memorial_p:
            if n==len(memorial_p)-2 and i>37:
                break
            memorial=memorial+memorial_text.text+'{n}'
            n+=1
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
        file_p=file_p
        memorial=memorial.replace('\n\n','\n')
        memorial=memorial.replace(';','.')
        memorial=memorial.replace('\n',' ')
        memorial=memorial.replace('  ',' ')
        f.write(str(i)+';'+'<b>'+file_p+'</b>'+';'+text1+';'+text2+';'+right_answer+';'+memorial+'\n')
        i+=1
        answer.clear()
#parse_data_bs('test8.html')
#f.close()
f=open('q8.csv','r')
lines = f.readlines()
db = sqlite3.connect('inf9gia.db')
cursor = db.cursor()
sql="""DROP TABLE IF EXISTS `question8`"""
cursor.execute(sql)
db.commit()
sql="""CREATE TABLE IF NOT EXISTS `question8` (
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
    # если в строе присутствует емейл (определяем по наличию "@")
    # извлекаем данные из строки
    file1, text1, text2, right_answer, memorial = unpack_line(str(line))
    # подставляем эти данные в SQL-запрос
    sql = """INSERT INTO question8(file, text1, text2, right_answer, memorial)
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
