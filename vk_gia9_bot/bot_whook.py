# -*- coding: utf-8 -*-
'''
Телеграмм бот версии 0.18 для подготовки к ГИА по информатике
Бот написан учителем информатики Четверовым Алексеем Владимировичем
Бот основан на уроках по созданию музыкальной викторины https://www.gitbook.com/book/groosha/telegram-bot-lessons/details
Использована библиотека pyTelegramBotAPI https://github.com/eternnoir/pyTelegramBotAPI
В качестве источника данных для заданий используется база данных SQLLight
Информация о пользователях сохраняется в формете ключ-запись в отдельном файле
Этот файл основной программы бота
'''
import config 
import telebot
from telebot import types
from SQLighter import SQLighter
import utils
import random
import os
from flask import Flask, request
from multiprocessing import Process
from time import time,sleep
import apiai, json

server = Flask(__name__)

bot = telebot.TeleBot(config.token)
TOKEN=config.token

utils.count_rows()
random.seed()

debug_mode=config.debug

#Отправка сообщений по таймеру
def check_send_messages():
    while True:
        if debug_mode==1: print ('check time GO!')
        user_for_check=utils.check_time_user()
        user_for_check=list(user_for_check)
        for user_g in user_for_check:
            time_os=int(time())
            if debug_mode==1: print ('time_os = ',time_os)
            last_time=int(user_g[42])
            if debug_mode==1: print ('last_time = ',last_time)
            if debug_mode==1: print ('abs(time_os-last_time) = ',abs(time_os-last_time))
            if abs(time_os-last_time)>15*60*60 and time_os%86400//3600>12 and time_os%86400//3600<16:
                number_result=list(user_g)
                q_n=1
                question_result=0
                for i in range (6,41,2):
                    if number_result[i+1]-number_result[i]<question_result and number_result[i+1]-number_result[i]<6:
                        question_result=number_result[i+1]-number_result[i]
                        question_number=q_n
                    q_n+=1
                bot.send_message(user_g[1],'Привет, не пора ли подготовится к экзамену? Рекомендую начать с задания номер '+str(question_number))
                utils.update_time(user_g[1])
                if debug_mode==1: print ('set new time for '+user_g[1])
            else:
                if debug_mode==1: print ('time OK for '+user_g[1])
            sleep(1)
        # ваш код проверки времени и отправки сообщений по таймеру
        # пауза между проверками, чтобы не загружать процессор
        sleep(360)

# а теперь запускаем проверку в отдельном потоке

@bot.message_handler(commands=['result'])
def result_game(message):
    if utils.chek_user(message.chat.id):
        bot.send_message(message.chat.id,'Произвожу подсчет.....')
        if utils.check_result(message.chat.id):
            img_f = open('img/users/'+str(message.chat.id)+'_result'+'.png', 'rb')
            bot.send_photo(message.chat.id, img_f)
            img_f.close()
            bot.send_message(message.chat.id,'Твой результат представлен на картинке выше')
    else:
        bot.send_message(message.chat.id, 'Информации о вас нет в моей базе данных! Я обнавленная версия бота! Наберите команду старт или /start')

@bot.message_handler(commands=['stat'])
def stat_game(message):
    if utils.chek_user(message.chat.id):
        bot.send_message(message.chat.id,'Произвожу подсчет.....')
        if utils.check_stat(message.chat.id):
            img_f = open('img/users/'+str(message.chat.id)+'_stat'+'.png', 'rb')
            bot.send_photo(message.chat.id, img_f)
            img_f.close()
            bot.send_message(message.chat.id,'Статистика по заданиям представлена на картинке выше')
    else:
        bot.send_message(message.chat.id, 'Информации о вас нет в моей базе данных! Я обнавленная версия бота! Наберите команду старт или /start')

@bot.message_handler(commands=['help'])
def help_game(message):
    bot.send_message(message.chat.id,config.help_massage_intro)
    bot.send_message(message.chat.id,'Вот какие команды я знаю:')
    bot.send_message(message.chat.id,config.help_massage)

@bot.message_handler(commands=['game'])
def new_game(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
    markup.row('/1', '/2', '/3', '/4', '/5', '/6')
    markup.row('/7', '/8', '/9', '/10', '/11', '/12')
    markup.row('/13', '/14', '/15', '/16', '/17', '/18')
    bot.send_message(message.chat.id, "Выбери номер задания для тренировки:", reply_markup=markup)

@bot.message_handler(commands=['1','2','3','4','5','6'])
def game_1_6(message,number_q='not'):
    if number_q=='not':
        #получаем сообщение пользователя
        message_namber=message.text
        #разбиваем сообщение на части, делитель - символ /
        answer_number=message_namber.split('/')
        if debug_mode==1: print ('Массив с номером вопроса, когда команда',answer_number)
    else:
        answer_number=['',str(number_q)]
        if debug_mode==1: print ('массив данных о номере вопроса когда ИИ',answer_number)
    #keyboard_hider = types.ReplyKeyboardRemove()
    db_worker = SQLighter(config.database_name)
    # Получаем случайную строку из БД
    if debug_mode==1: print ('answer_number[1]=',answer_number[1])
    row = db_worker.select_single(random.randint(1, utils.get_rows_count(answer_number[1])),answer_number[1])
    # Отсоединяемся от БД
    db_worker.close()
    # Формируем разметку
    markup = utils.generate_markup(row[4], row[5],answer_number[1])
    if answer_number[1]=='3' or answer_number[1]=='5':
        # Отправляем вводную часть вопроса
        bot.send_message(message.chat.id,row[2])
        # Отправляем картинку
        img_f = open(row[1], 'rb')
        bot.send_photo(message.chat.id, img_f)
        img_f.close()
    if answer_number[1]=='4' or answer_number[1]=='6':
        # Отправляем вводную часть вопроса с форматированием
        bot.send_message(message.chat.id,row[2],parse_mode='HTML')
        # Отправляем основную часть вопроса с форматированием
        bot.send_message(message.chat.id, row[1],parse_mode='HTML')
    # Отправляем вопрос и заменяем кдавиатуру на варианты ответа
    bot.send_message(message.chat.id,row[3],reply_markup=markup)

    # Включаем "игровой режим"... ждем ответа от пользователя
    utils.set_user_game(message.chat.id, row[4],row[6],answer_number[1])

    

@bot.message_handler(commands=['7','8','11','12','14','15','16','17','18'])
def game_7_18_not_9_10(message,number_q='not'):
    if number_q=='not':
        #получаем сообщение пользователя
        message_namber=message.text
        #разбиваем сообщение на части, делитель - символ /
        answer_number=message_namber.split('/')
        if debug_mode==1: print ('Массив с номером вопроса, когда команда',answer_number)
    else:
        answer_number=['',str(number_q)]
        if debug_mode==1: print ('массив данных о номере вопроса когда ИИ',answer_number)
    # Подключаемся к БД
    db_worker = SQLighter(config.database_name)
    # Получаем случайную строку из БД по номеру таблицы взятую из сообщения answer_number
    row = db_worker.select_single(random.randint(1, utils.get_rows_count(answer_number[1])),answer_number[1])
    # Отсоединяемся от БД
    db_worker.close()
    if answer_number[1]=='7':
        # Отправляем вводную часть вопроса
        bot.send_message(message.chat.id,row[2])
        # Отправляем картинку
        bot.send_photo(message.chat.id, row[1])
    elif answer_number[1]=='12':
        # Отправляем вводную часть вопроса
        bot.send_message(message.chat.id,row[2])
        # Отправляем картинку
        img_f = open(row[1], 'rb')
        bot.send_photo(message.chat.id, img_f)
        img_f.close()
    elif answer_number[1]=='8':
        # Отправляем вводную часть вопроса с форматированием
        bot.send_message(message.chat.id,row[2])
        # Отправляем основную часть вопроса
        bot.send_message(message.chat.id, row[1],parse_mode='HTML')
    elif answer_number[1]=='11' or answer_number[1]=='18':
        img_f = open(row[1], 'rb')
        bot.send_photo(message.chat.id, img_f)
        img_f.close()
    # Отправляем вопрос
    bot.send_message(message.chat.id,row[3])
    # Включаем "игровой режим"... ждем ответа от пользователя
    utils.set_user_game(message.chat.id, row[4],row[5],answer_number[1])
    # Отсоединяемся от БД
    db_worker.close()

@bot.message_handler(commands=['9']) #добавить 10
def game_9(message,number_q='not'):
    if number_q=='not':
        #получаем сообщение пользователя
        message_namber=message.text
        #разбиваем сообщение на части, делитель - символ /
        answer_number=message_namber.split('/')
        if debug_mode==1: print ('Массив с номером вопроса, когда команда',answer_number)
    else:
        answer_number=['',str(number_q)]
        if debug_mode==1: print ('массив данных о номере вопроса когда ИИ',answer_number)
    code=utils.set_user_code_get(message.chat.id)
    if not code or code=='':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        markup.row('/schoolalgorithm')
        markup.row('/basic', '/pascal')
        markup.row('/python')
        bot.send_message(message.chat.id, 'ВНИМАНИЕ! Не выбран предпочитаемый язык программирования!\nВыбери предпочитаемый язык программирования:\n * schoolalgorithm - Алгоритмический язык (КУМИР)\n * basic - бейсик\n * pascal - Паскаль\n * Pyhon - Пайтон (Питон)', reply_markup=markup)
    else:
        # Подключаемся к БД
        db_worker = SQLighter(config.database_name)
        # Получаем случайную строку из БД по номеру таблицы взятую из сообщения answer_number
        row = db_worker.select_single(random.randint(1, utils.get_rows_count(answer_number[1])),answer_number[1])
        #Отсоединяемся от БД
        db_worker.close()
        #Генерируем значение пременной для дополнительного сообщения:
        chat_message ={
        '2':'Алгоритмический язык',
        '3':'BASIC',
        '4':'Pascal',
        '5':'Python'
        }
        #генерируем случайные числа для шаблона программы из базы данных
        s=random.randint(1,10)-1
        s1=random.randint(1,5)
        if row[6]=='mult' or row[6]=='aprog':

            r=random.randint(1,3)
        else:
            r=random.randint(4,9)
        if row[6]=='aprog':
            k1=random.randint(2,3)
        else:
            k1=random.randint(4,9)
        #сохраняем в переменную текст шаюблона из базы данных
        result_code=row[int(code)]
        #заменяем данные в шаблоне
        result_code=result_code.replace('{s}',str(s))
        result_code=result_code.replace('{k1}',str(k1))
        result_code=result_code.replace('{k2}',str(k1+r))
        result_code=result_code.replace('{s1}',str(s1))
        # Отправляем вводную часть вопроса
        bot.send_message(message.chat.id,row[1])
        # Отправляем основную часть вопроса c форматированием
        bot.send_message(message.chat.id, '<pre>'+result_code+'</pre>',parse_mode='HTML')
        # Отправляем дополнительное сообщение
        bot.send_message(message.chat.id,'Текст программы приведён на языке программирования: '+chat_message[code])
        #сохраняем в переменную текст шаюблона пояснения из базы данных
        result_memorial=row[7]
        #заеняем данные в шаблоне
        result_memorial=result_memorial.replace('{s}',str(s))
        result_memorial=result_memorial.replace('{k1}',str(k1))
        result_memorial=result_memorial.replace('{k2}',str(k1+r))
        result_memorial=result_memorial.replace('{s1}',str(s1))
        result_memorial=result_memorial.replace('{r}',str(r+1))
        result_memorial=result_memorial.replace('{answer}',utils.generate_right_answer_9(row[6],s,s1,r,k1))
        # Включаем "игровой режим"... ждем ответа от пользователя
        utils.set_user_game(message.chat.id, utils.generate_right_answer_9(row[6],s,s1,r,k1),result_memorial,answer_number[1])

@bot.message_handler(commands=['10'])
def game_10(message,number_q='not'):
    if number_q=='not':
        #получаем сообщение пользователя
        message_namber=message.text
        #разбиваем сообщение на части, делитель - символ /
        answer_number=message_namber.split('/')
        if debug_mode==1: print ('Массив с номером вопроса, когда команда',answer_number)
    else:
        answer_number=['',str(number_q)]
        if debug_mode==1: print ('массив данных о номере вопроса когда ИИ',answer_number)
    code=utils.set_user_code_get(message.chat.id)
    if not code or code=='':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True,one_time_keyboard=True)
        markup.row('/schoolalgorithm')
        markup.row('/basic', '/pascal')
        markup.row('/python')
        bot.send_message(message.chat.id, 'ВНИМАНИЕ! Не выбран предпочитаемый язык программирования!\nВыбери предпочитаемый язык программирования:\n * shoolAlgorithm - Алгоритмический язык (КУМИР)\n * basic - бейсик\n * pascal - Паскаль\n * Pyhon - Пайтон (Питон)', reply_markup=markup)
    else:
        # Подключаемся к БД
        db_worker = SQLighter(config.database_name)
        # Получаем случайную строку из БД по номеру таблицы взятую из сообщения answer_number
        row = db_worker.select_single(random.randint(1, utils.get_rows_count(answer_number[1])),answer_number[1])
        #Отсоединяемся от БД
        db_worker.close()
        #Генерируем значение пременной для дополнительного сообщения:
        chat_message ={
        '2':'Алгоритмический язык',
        '3':'BASIC',
        '4':'Pascal',
        '5':'Pyhon'
        }
        #генерируем случайные числа для шаблона программы из базы данных
        Dat=[random.randint(10, 20) for i in range(10)]
        #Генерируем вспомогательное число для сравнения или подсчета
        t=random.randint(10, 20)
        #сохраняем в переменную текст шаюблона из базы данных
        result_code=row[int(code)]
        #заменяем данные в шаблоне
        for i in range(10):
            result_code=result_code.replace('{dat'+str(int(i))+'}',str(Dat[i]))
        result_code=result_code.replace('{t}',str(t))
        # Отправляем вводную часть вопроса
        bot.send_message(message.chat.id,row[1])
        # Отправляем основную часть вопроса c форматированием
        bot.send_message(message.chat.id, '<pre>'+result_code+'</pre>',parse_mode='HTML')
        # Отправляем дополнительное сообщение
        bot.send_message(message.chat.id,'Текст программы приведён на языке программирования: '+chat_message[code])
        #сохраняем в переменную текст шаюблона пояснения из базы данных
        result_memorial=row[7]
        #заеняем данные в шаблоне
        result_memorial=result_memorial.replace('{t}',str(t))
        result_memorial=result_memorial.replace('{answer}',utils.generate_right_answer_10(row[6],Dat,t))
        # Включаем "игровой режим"... ждем ответа от пользователя
        utils.set_user_game(message.chat.id, utils.generate_right_answer_10(row[6],Dat,t),result_memorial,answer_number[1])

@bot.message_handler(commands=['13'])
def game_13(message,number_q='not'):
    if number_q=='not':
        #получаем сообщение пользователя
        message_namber=message.text
        #разбиваем сообщение на части, делитель - символ /
        answer_number=message_namber.split('/')
        if debug_mode==1: print ('Массив с номером вопроса, когда команда',answer_number)
    else:
        answer_number=['',str(number_q)]
        if debug_mode==1: print ('массив данных о номере вопроса когда ИИ',answer_number)
    base1=random.randint(0,3)
    if base1==0 or base1==1 or base1==2:
        base2=3
    elif base1==3:
        base2=random.randint(0,2)
    chislo=random.randint(101,255)
    base_text1 =['двоичное','восьмеричное','шестнадцатеричное','десятичное']
    base_number=[2,8,16,10]
    base_text2 =['двоичную','восьмеричную','шестнадцатеричную','десятичную']
    text_mesaage='Переведите '+base_text1[base1]+' число '+utils.convert_base(chislo,base_number[base1],10)+' в '+base_text2[base2]+' систему счисления.'
    ra=utils.convert_base(chislo,base_number[base2],10)
    # Отправляем вопрос
    bot.send_message(message.chat.id,text_mesaage)
    # Включаем "игровой режим"... ждем ответа от пользователя
    utils.set_user_game(message.chat.id, ra,'Не понял как решать? я могу обяснить.',answer_number[1])

@bot.message_handler(commands=['schoolalgorithm','basic','pascal','python'])
def game_1_18_9(message):
    #убрать клавиатуру 
    keyboard_hider = types.ReplyKeyboardRemove()
    #получаем сообщение пользователя
    message_namber=message.text
    #разбиваем сообщение на части, делитель - символ /
    answer_number=message_namber.split('/')
    if answer_number[1]=='schoolalgorithm':
        code='2'
        chat_message='Алгоритмический язык'
    elif answer_number[1]=='basic':
        code='3'
        chat_message='BASIC'
    elif answer_number[1]=='pascal':
        code='4'
        chat_message='Pascal'
    elif answer_number[1]=='python':
        code='5'
        chat_message='Pyhon'
    if utils.set_user_code(message.chat.id,code):
        bot.send_message(message.chat.id,'Вы установили в качестве основного языка: '+chat_message+'\nНаберите команду /9 или /10 для получения задания.',reply_markup=keyboard_hider)
    else:
        bot.send_message(message.chat.id, 'Информации о вас нет в моей базе данных! Я обнавленная версия бота! Наберите команду старт или /start')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def check_answer(message):
    #убрать клавиатуру 
    keyboard_hider = types.ReplyKeyboardRemove()
    # Если функция возвращает None -> Человек не в игре
    answer = utils.get_answer_for_user(message.chat.id)
    # Как Вы помните, answer может быть либо текст, либо None
    if not answer:
        request = apiai.ApiAI(config.token_ai).text_request() # Токен API к Dialogflow
        request.lang = 'ru' # На каком языке будет послан запрос
        request.session_id = message.chat.id # ID Сессии диалога (нужно, чтобы потом учить бота)
        request.query = message.text # Посылаем запрос к ИИ с сообщением от юзера
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        try:
            action = responseJson['result']['metadata']['intentName']
        except KeyError:
            action=None
        try:
            response = responseJson['result']['fulfillment']['speech']
        except KeyError:
            response=None
        if debug_mode==1: print ('not answer responseJson= ',responseJson)
        if debug_mode==1: print ('not answer action= ',action)
        if debug_mode==1: print ('not answer response= ', response)
        if  not action:
            bot.send_message(message.chat.id, response)
        else:
            if action=='bot.question':
                n_q=responseJson['result']['parameters']['question']
                try:
                    if 1<=int(n_q)<=6:
                        game_1_6(message,n_q)
                    elif n_q=='7' or n_q=='8' or n_q=='11' or n_q=='12' or int(n_q)>13 and int(n_q)<19:
                        game_7_18_not_9_10(message,n_q)
                    elif n_q=='9':
                        game_9(message,n_q)
                    elif n_q=='10':
                        game_10(message,n_q)
                    elif n_q=='13':
                        game_13(message,n_q)
                except ValueError:
                    if debug_mode==1: print ('ValueError для n_q! n_q=',n_q)
                    bot.send_message(message.chat.id, response)
            elif action=='bot.explanation':
                n_q=responseJson['result']['parameters']['explanation']
                if n_q:
                    bot.send_message(message.chat.id,utils.url_explanation(n_q))
                else:
                    bot.send_message(message.chat.id, response)
            elif action=='Default Welcome Intent':
                utils.start_bot(message.chat.id,message.chat.first_name,message.chat.last_name,message.chat.username)
                bot.send_message(message.chat.id, response)
            elif action=='bot.help':
                help_game(message)
            elif action=='bot.result':
                result_game(message)
            elif action=='bot.stat':
                stat_game(message)
            elif action=='bot.random':
                n_q=str(random.randint(1,18))
                try:
                    if 1<=int(n_q)<=6:
                        game_1_6(message,n_q)
                    elif n_q=='7' or n_q=='8' or n_q=='11' or n_q=='12' or int(n_q)>13 and int(n_q)<19:
                        game_7_18_not_9_10(message,n_q)
                    elif n_q=='9':
                        game_9(message,n_q)
                    elif n_q=='10':
                        game_10(message,n_q)
                    elif n_q=='13':
                        game_13(message,n_q)
                except ValueError:
                    if debug_mode==1: print ('ValueError для n_q! n_q=',n_q)
                    bot.send_message(message.chat.id, response)
            else:
                bot.send_message(message.chat.id, response)
        if debug_mode==1: print ('responseJson= ',responseJson)
        if debug_mode==1: print ('action= ',action)
        if debug_mode==1: print ('response= ', response)
    else:
        # Убирем клавиатуру с вариантами ответа.
        #keyboard_hider = types.ReplyKeyboardRemove() reply_markup=keyboard_hider
        # Если ответ правильный/неправильный
        if message.text == answer.upper() or message.text == answer.lower() or message.text == answer.title() or message.text == answer:
            bot.send_message(message.chat.id, 'Верно!')
            answer_game_1=1
            answer_game_0=0
        else:
            bot.send_message(message.chat.id, 'Увы, Вы ошиблись!')
            bot.send_message(message.chat.id, 'Пояснения:\n'+utils.finish_user_game_memorial(message.chat.id))
            answer_game_1=0
            answer_game_0=1
        # Сохраняем счет пользователя в базу данных (игра закончена)
        bot.send_message(message.chat.id,'Произвожу подсчет результатов........')
        utils.finish_user_game(message.chat.id,answer_game_1,answer_game_0)
        bot.send_message(message.chat.id, utils.finish_user_game_count(message.chat.id),reply_markup=keyboard_hider)

@bot.message_handler(commands=['start'])
def start_game(message):
    start_massage=('Приветсвую дорогой друг!\n'
    'Если ты желаешь подготовится к ГИА по информатике, то ты пришел по адресу.\n')
    bot.send_message(message.chat.id,start_massage)
    bot.send_message(message.chat.id,config.help_massage)
    utils.start_bot(message.chat.id,message.chat.first_name,message.chat.last_name,message.chat.username)

p1 = Process(target=check_send_messages, args=())
p1.start()

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://ancient-woodland-35882.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
    utils.count_rows()
    random.seed()