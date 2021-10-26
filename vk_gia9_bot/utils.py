# -*- coding: utf-8 -*-
'''
Телеграмм бот версии 0.12 для подготовки к ГИА по информатике
Бот написан учителем информатики Четверовым Алексеем Владимировичем
Бот основан на уроках по созданию музыкальной викторины https://www.gitbook.com/book/groosha/telegram-bot-lessons/details
Использована библиотека pyTelegramBotAPI https://github.com/eternnoir/pyTelegramBotAPI
В качестве источника данных для заданий используется база данных SQLLight
Информация о пользователях сохраняется в формете ключ-запись в отдельном файле
Этот файл функций работы с базами данных и форматирования ответов
'''
import shelve
from telebot import types
from SQLighter import SQLighter
from config import shelve_name, database_name,host_db,pas_db,user_db,db_name,debug
from random import shuffle
from MySQL import MySQL
from time import time
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

def count_rows():
    """
    Данный метод считает общее количество строк в базе данных и сохраняет в хранилище.
    Потом из этого количества будем выбирать музыку.
    """
    db = SQLighter(database_name)
    rowsnum1 = db.count_rows('1')
    rowsnum2 = db.count_rows('2')
    rowsnum3 = db.count_rows('3')
    rowsnum4 = db.count_rows('4')
    rowsnum5 = db.count_rows('5')
    rowsnum6 = db.count_rows('6')
    rowsnum7 = db.count_rows('7')
    rowsnum8 = db.count_rows('8')
    rowsnum9 = db.count_rows('9')
    rowsnum10 = db.count_rows('10')
    rowsnum11 = db.count_rows('11')
    rowsnum12 = db.count_rows('12')
    rowsnum13=0
    rowsnum14 = db.count_rows('14')
    rowsnum15 = db.count_rows('15')
    rowsnum16 = db.count_rows('16')
    rowsnum17 = db.count_rows('17')
    rowsnum18 = db.count_rows('18')
    with shelve.open(shelve_name) as storage:
        storage['rows_count'] =[rowsnum1,rowsnum2,rowsnum3,rowsnum4,rowsnum5,rowsnum6,rowsnum7,rowsnum8,rowsnum9,rowsnum10,rowsnum11,rowsnum12,rowsnum13,rowsnum14,rowsnum15,rowsnum16,rowsnum17,rowsnum18]


def get_rows_count(table_number):
    """
    Получает из хранилища количество строк в БД
    :return: (int) Число строк
    """
    with shelve.open(shelve_name) as storage:
        rowsnum = storage['rows_count']
        if debug==1: print ('rowsnum = ',rowsnum)
        if debug==1: print ('table_number = ',int(table_number)-1)
        if debug==1: print ('table_number_rowsnum = ',rowsnum [int(table_number)-1])
    return rowsnum [int(table_number)-1]


def set_user_game(chat_id, estimated_answer,memorial,question_number):
    """
    Записываем юзера в игроки и запоминаем, что он должен ответить, и текущий счет.
    :param chat_id: id юзера
    :param estimated_answer: правильный ответ (из БД)
    """
    with shelve.open(shelve_name) as storage:
        storage[str(chat_id)] = [estimated_answer,memorial,question_number]

def start_bot(chat_id,first_name,last_name,username):
    """
    Добавление юзера в базу данных
    """
    db = MySQL(host_db,pas_db,user_db,db_name)
    user=db.get_user(chat_id)
    if not user:
        db.insert_user(chat_id,first_name,last_name,username)
        db.update_time(chat_id,str(int(time())))
        if debug==1: print ('добавлен пользователь')
    db.close()

def chek_user(chat_id):
    db = MySQL(host_db,pas_db,user_db,db_name)
    user=db.get_user(chat_id)
    db.close()
    if not user:
        return None
    else:
        return 1

def insert_user(chat_id,first_name,last_name,username):
    """
    Добавление юзера в базу данных
    """
    db = MySQL(host_db,pas_db,user_db,db_name)
    db.insert_user(chat_id,first_name,last_name,username)
    if debug==1: print ('добавлен пользователь')
    db.close()


def set_user_code_get(chat_id):
    """
    Получаем язык программирования юзера
    """
    db = MySQL(host_db,pas_db,user_db,db_name)
    code=db.get_user(chat_id)
    db.close()
    if debug==1: print('code=',code)
    if code:
        return code[5]
    else:
        return None


def set_user_code(chat_id,code):
    """
    Записываем юзера в игроки и запоминаем, язык программирования
    """
    if chek_user(chat_id):
        db = MySQL(host_db,pas_db,user_db,db_name)
        db.update_code(chat_id,code)
        db.close()
        return 1
    else:
        return None

def finish_user_game_memorial(chat_id):
    """
    Выводим подсказку для игрока
    """
    with shelve.open(shelve_name) as storage:
        data_user=storage[str(chat_id)]
        return data_user[1]

def finish_user_game(chat_id,answer_1,answer_0):
    """
    обновляем данные счета ответов"""
    with shelve.open(shelve_name) as storage:
        if chek_user(chat_id):
            data_user=storage[str(chat_id)]
            question_number=data_user[2]
            db = MySQL(host_db,pas_db,user_db,db_name)
            result_q=db.get_question_result(chat_id,question_number)
            result_q=list(result_q)
            result_q[0]+=answer_0
            result_q[1]+=answer_1
            db.update_question_result(chat_id,question_number,result_q[0],'0')
            db.update_question_result(chat_id,question_number,result_q[1],'1')
            result=db.get_user(chat_id)
            result_0=0
            result_1=0
            db.update_time(chat_id,str(int(time())))
            db.close()
            result=list(result)
            for i in range (6,41,2):
                result_0+=int(result[i])
                result_1+=int(result[i+1])
            storage[str(chat_id)]=['Ваш общий счет: ('+str(result_1)+') - ответили верно; ('+str(result_0)+') - ответили не верно.\nВ этом, '+str(question_number)+' задании вы ('+str(result_q[1])+') - ответили верно; ('+str(result_q[0])+') - ответили не верно.']
        else:
            storage[str(chat_id)]=['Информации о вас нет в моей базе данных! Я обнавленная версия бота! Наберите команду старт или /start для того чтобы воспользоваться всеми возможностями бота']

def update_time(chat_id):
    db = MySQL(host_db,pas_db,user_db,db_name)
    db.update_time(chat_id,str(int(time())))
    db.close()

def finish_user_game_count(chat_id):
    """
    выводим точный счет, удаляем игрока из списка играющих
    """
    with shelve.open(shelve_name) as storage:
        count=storage[str(chat_id)]
        del storage[str(chat_id)]
        return count[0]
        

def get_answer_for_user(chat_id):
    """
    Получаем правильный ответ для текущего юзера.
    В случае, если человек просто ввёл какие-то символы, не начав игру, возвращаем None
    :param chat_id: id юзера
    :return: (str) Правильный ответ / None
    """
    with shelve.open(shelve_name) as storage:
        try:
            answer = storage[str(chat_id)]
            return answer[0]
        # Если человек не играет, ничего не возвращаем
        except KeyError:
            return None

def generate_markup(right_answer, wrong_answers,answer_number):
    """
    Создаем кастомную клавиатуру для выбора ответа
    :param right_answer: Правильный ответ
    :param wrong_answers: Набор неправильных ответов
    :return: Объект кастомной клавиатуры
    """
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    # Склеиваем правильный ответ с неправильными
    all_answers = '{},{}'.format(right_answer, wrong_answers)
    # Создаем лист (массив) и записываем в него все элементы
    list_items = []
    for item in all_answers.split(','):
        list_items.append(item)
    # Хорошенько перемешаем все элементы
    shuffle(list_items)
    # Заполняем разметку перемешанными элементами
    if answer_number=='4' or answer_number=='6':
        markup.row(list_items[0])
        markup.row(list_items[1])
        markup.row(list_items[2])
        markup.row(list_items[3])
    else:
        markup.row(list_items[0],list_items[1])
        markup.row(list_items[2],list_items[3])
    return markup

# функция вычисления правильного ответа для 9-го задания.
def generate_right_answer_9(right_answer,s,s1,r,k1):
    if right_answer=='add':
        return str(int(s+s1*(r+1)))
    if right_answer=='mult':
        return str(int(s*pow(s1,(r+1))))
    if right_answer=='aprog':
        for k in range(k1, k1+r+1):
            s = s+s1*k
        return str(int(s))
    if right_answer=='sub':
        return str(int(s-s1*(r+1)))

#функция вычисления правильного ответа для 9-го задания.
def generate_right_answer_10(right_answer,list1,k):
    if right_answer=='count':
        return str(list1.count(k))
    if right_answer=='min':
        return str(min(list1))
    if right_answer=='max':
        return str(max(list1))
    if right_answer=='minindex':
        return str(list1.index(min(list1)))
    if right_answer=='maxindex':
        return str(list1.index(max(list1)))
    if right_answer=='more':
        m=0
        for j in range(10):
            if list1[j]>k:
                m=m+1
        return str(int(m))
    if right_answer=='less':
        m=0
        for j in range(10):
            if list1[j]>k:
                m=m+1
        return str(int(m))
    if right_answer=='summ':
        m=0
        for j in range(10):
            if list1[j]>k:
                m=m+list1[j]
        return str(int(m))
#Функция перевода из одной системы счисления в другую
def convert_base(num, to_base=10, from_base=10):
    # first convert to decimal number
    if isinstance(num, str):
        n = int(num, from_base)
    else:
        n = int(num)
    # now convert decimal to 'to_base' base
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if n < to_base:
        return alphabet[n]
    else:
        return convert_base(n // to_base, to_base) + alphabet[n % to_base]

def url_explanation(question_number):
    db = MySQL(host_db,pas_db,user_db,db_name)
    url=db.get_explanation(question_number)
    db.close()
    return url[0]

def check_time_user():
    db = MySQL(host_db,pas_db,user_db,db_name)
    all_user=db.get_all_user()
    db.close()
    return all_user

def check_result(chat_id):
    percent=0.0
    db = MySQL(host_db,pas_db,user_db,db_name)
    result=db.get_user(chat_id)
    db.close()
    result=list(result)
    for i in range (6,41,2):
        if debug==1: print('result[i+1]-result[i]=',result[i+1]-result[i])
        if result[i+1]-result[i]>0:
            percent=percent+result[i+1]-result[i]
    percent=percent/90
    if debug==1: print('percent=',percent)
    if percent<0:
        percent=0
    if percent<0.50:
        rgb=(160,0,0)
    elif 0.5<=percent<0.9:
        rgb=(230,230,0)
    elif percent>=0.9:
        rgb=(0,160,0)
    font = ImageFont.truetype(font='Times.dfont',size=140, index=0, encoding='')
    img=Image.new("RGB",(640,640),(255,255,255))
    draw=ImageDraw.Draw(img)
    draw.ellipse((9,9,631,631),outline=(220,220,220))
    draw.ellipse((71,71,569,569),outline=(220,220,220))
    draw.pieslice((10,10,630,630),-90,int(360*percent)-90,fill=rgb)
    draw.pieslice((70,70,570,570),-90,int(360*percent)-90,fill=(255,255,255))
    draw.text((200,270), str(int(percent*100))+'%', rgb, font)
    draw.ellipse((9,9,631,631),outline=(220,220,220))
    draw.ellipse((71,71,569,569),outline=(220,220,220))
    img.save('img/users/'+str(chat_id)+'_result'+'.png', 'PNG')
    img.close()
    return 1

def check_stat(chat_id):
    db = MySQL(host_db,pas_db,user_db,db_name)
    result=db.get_user(chat_id)
    db.close()
    x=63
    y=180
    img=Image.new("RGB",(640,360),(255,255,255))
    base_img=Image.open('img/gia_bot_stat.png')
    img.paste(base_img, (0, 0))
    draw = ImageDraw.Draw(img)
    result=list(result)
    for i in range (6,41,2):
        result_q=result[i+1]-result[i]
        if result_q>=0:
            if result_q>5:
                result_q=5
            draw.rectangle((x-16,30+((5-result_q)*30),x,y),fill=(0,160,0),outline=(220,220,220))
        else:
            if result_q<5*(-1):
                result_q=5*(-1)
            draw.rectangle((x-16,y,x,180+(((-1)*result_q)*30)),fill=(160,0,0),outline=(220,220,220))
        x+=33
    img.save('img/users/'+str(chat_id)+'_stat'+'.png', 'PNG')
    base_img.close()
    img.close()
    return 1

def check_result_f(chat_id):
    percent=0.0
    db = MySQL(host_db,pas_db,user_db,db_name)
    result=db.get_user(chat_id)
    db.close()
    result=list(result)
    for i in range (6,41,2):
        if debug==1: print('result[i+1]-result[i]=',result[i+1]-result[i])
        if result[i+1]-result[i]>0:
            percent=percent+result[i+1]-result[i]
    percent=percent/90
    if debug==1: print('percent=',percent)
    if percent<0:
        percent=0
    if percent<0.50:
        rgb=(160,0,0)
    elif 0.5<=percent<0.9:
        rgb=(230,230,0)
    elif percent>=0.9:
        rgb=(0,160,0)
    font = ImageFont.truetype(font='Times.dfont',size=140, index=0, encoding='')
    img=Image.new("RGB",(640,640),(255,255,255))
    draw=ImageDraw.Draw(img)
    draw.ellipse((9,9,631,631),outline=(220,220,220))
    draw.ellipse((71,71,569,569),outline=(220,220,220))
    draw.pieslice((10,10,630,630),-90,int(360*percent)-90,fill=rgb)
    draw.pieslice((70,70,570,570),-90,int(360*percent)-90,fill=(255,255,255))
    draw.text((200,270), str(int(percent*100))+'%', rgb, font)
    draw.ellipse((9,9,631,631),outline=(220,220,220))
    draw.ellipse((71,71,569,569),outline=(220,220,220))
    img.save('img/users/'+str(result[3])+str(chat_id)+'_result'+'.png', 'PNG')
    img.close()

def check_stat_f(chat_id):
    db = MySQL(host_db,pas_db,user_db,db_name)
    result=db.get_user(chat_id)
    db.close()
    x=63
    y=180
    img=Image.new("RGB",(640,360),(255,255,255))
    base_img=Image.open('img/gia_bot_stat.png')
    img.paste(base_img, (0, 0))
    draw = ImageDraw.Draw(img)
    result=list(result)
    for i in range (6,41,2):
        result_q=result[i+1]-result[i]
        if result_q>=0:
            if result_q>5:
                result_q=5
            draw.rectangle((x-16,30+((5-result_q)*30),x,y),fill=(0,160,0),outline=(220,220,220))
        else:
            if result_q<5*(-1):
                result_q=5*(-1)
            draw.rectangle((x-16,y,x,180+(((-1)*result_q)*30)),fill=(160,0,0),outline=(220,220,220))
        x+=33
    img.save('img/users/'+str(result[3])+str(chat_id)+'_stat'+'.png', 'PNG')
    base_img.close()
    img.close()



