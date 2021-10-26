import sqlite3
import requests
from bs4 import BeautifulSoup
#f=open('q11.csv','w')

headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'
      }

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
    text2_u = els[2]
    right_answer_u = els[3]
    right_answer_u=right_answer_u.replace(' ','')
    memorial_u = els[4]
    memorial_u=memorial_u.replace(' {n}','{n}')
    memorial_u=memorial_u.replace('{n} {n}','{n}')
    memorial_u=memorial_u.replace('{n}{n}','{n}')
    memorial_u=memorial_u.replace('{n}','\n')
    memorial_u=memorial_u.replace('  ',' ')
    return file_u, text2_u, right_answer_u, memorial_u

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
        text2=texts_p.next.text
        text_ra=item.find('div',{'class':'answer'})
        #номер правильного ответа
        right_answer = text_ra.next.text
        right_answer = right_answer[right_answer.find(':')+1:]

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
                with open('img/z11/'+str(i)+'.png','wb') as imgfile:
                    imgfile.write(img.content)
        except BaseException:
            url_img='None file'
        memorial_div=item.find('div',{'class':'nobreak solution'})
        memorial_p=memorial_div.find_all('p')
        memorial=''
        n=0
        for memorial_text in memorial_p:
            memorial=memorial+memorial_text.text+'{n}'
            n+=1
        memorial=memorial.replace('\n\n','\n')
        memorial=memorial.replace(';','.')
        memorial=memorial.replace('\n',' ')
        memorial=memorial.replace('  ',' ')
        if url_img!='None file':
            url_img='img/z11/'+str(i)+'.png'
        f.write(str(i)+';'+url_img+';'+text2+';'+right_answer+';'+memorial+'\n')
        i+=1
        answer.clear()
#parse_data_bs('test11.html')
#f.close()
f=open('q11.csv','r')
lines = f.readlines()
db = sqlite3.connect('inf9gia.db')
cursor = db.cursor()
sql="""DROP TABLE IF EXISTS `question11`"""
cursor.execute(sql)
db.commit()
sql="""CREATE TABLE IF NOT EXISTS `question11` (
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
    file1, text2, right_answer, memorial = unpack_line(str(line))
    print (unpack_line(line))
    # подставляем эти данные в SQL-запрос
    sql = """INSERT INTO question11(file, text2, right_answer, memorial)
    VALUES ('%(file)s','%(text2)s', '%(right_answer)s', '%(memorial)s')
    """%{"file":file1,"text2":text2, "right_answer":right_answer, "memorial":memorial}
    # исполняем SQL-запрос
    cursor.execute(sql)
    # применяем изменения к базе данных
    db.commit()
 
# закрываем соединение с базой данных
db.close()
# закрываем файл
f.close()'''
