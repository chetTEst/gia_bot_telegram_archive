# -*- coding: utf-8 -*-
from flask import Flask, request, json
from settings import *
import vkapi as bot
import config 
from SQLighter import SQLighter
import utils
import random
import os
from multiprocessing import Process
from time import time,sleep
import apiai
import sqlite3



utils.count_rows()
random.seed()
user_id=12155403
debug_mode=config.debug
bot.send_message(12155403,'Привет, я пулинг бот Жирно Тест программы')
#print (bot.upload_photo('img/z3/1.png',253533317))
#img_f = 'img/users/'+str(user_id)+'_stat'+'.png'
#bot.send_photo(user_id, img_f)

# а теперь запускаем проверку в отдельном потоке


'''if __name__ == "__main__":'''