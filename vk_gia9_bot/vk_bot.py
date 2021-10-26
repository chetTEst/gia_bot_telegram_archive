# -*- coding: utf-8 -*-
from flask import Flask, request, json
import vkapi as bot
import config 
from SQLighter import SQLighter
import utils
import random
import os
from multiprocessing import Process
from time import time,sleep
import apiai

app = Flask(__name__)

utils.count_rows()
random.seed()

debug_mode=config.debug

def check_send_messages():
    while True:
        if debug_mode==1: print ('check time GO!')
        user_for_check=utils.check_time_user()
        user_for_check=list(user_for_check)
        for user_g in user_for_check:
            if user_g[43]!=0:
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
                    bot.send_message(user_g[43],'Привет, не пора ли подготовится к экзамену? Рекомендую начать с задания номер '+str(question_number))
                    utils.update_time(user_g[43])
                    if debug_mode==1: print ('set new time for '+user_g[1])
                else:
                    if debug_mode==1: print ('time OK for '+user_g[1])
                sleep(1)
        # ваш код проверки времени и отправки сообщений по таймеру
        # пауза между проверками, чтобы не загружать процессор
        sleep(360)

def result_game(user_id):
    if utils.chek_user(user_id):
        bot.send_message(user_id,'Произвожу подсчет.....')
        if utils.check_result(user_id):
            img_f = open('img/users/'+str(user_id)+'_result'+'.png', 'rb')
            bot.send_photo(user_id, img_f)
            img_f.close()
            bot.send_message(user_id,'Твой результат представлен на картинке выше')
    else:
        bot.send_message(user_id, 'Информации о вас нет в моей базе данных! Я обнавленная версия бота! Наберите команду старт или /start')

def stat_game(user_id):
    if utils.chek_user(user_id):
        bot.send_message(user_id,'Произвожу подсчет.....')
        if utils.check_stat(user_id):
            img_f = open('img/users/'+str(user_id)+'_stat'+'.png', 'rb')
            bot.send_photo(user_id, img_f)
            img_f.close()
            bot.send_message(user_id,'Статистика по заданиям представлена на картинке выше')
    else:
        bot.send_message(user_id, 'Информации о вас нет в моей базе данных! Я обнавленная версия бота! Наберите команду старт или /start')

def help_game(user_id):
    bot.send_message(user_id,config.help_massage_intro)
    bot.send_message(user_id,'Вот какие команды я знаю:')
    bot.send_message(user_id,config.help_massage)

def game_1_6(chat_id,number_q='not'):
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



@app.route('/', methods=['POST'])
def processing():
    #Распаковываем json из пришедшего GET-запроса
    data = json.loads(request.data)
    user_id=data['object']['user_id']
    message_text=data['object']['user_id']
    #Вконтакте в своих запросах всегда отправляет поле типа
    if 'type' not in data.keys():
        return 'not vk',200
    if data['type'] == 'confirmation':
        return config.confirmation_token,200
    elif data['type'] == 'message_new':
        bot.send_message(user_id,message)
        # Сообщение о том, что обработка прошла успешно
        return 'ok',200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))