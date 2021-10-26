# -*- coding: utf-8 -*-
import MySQLdb

class MySQL:

    def __init__(self, host_d,pas_d,user_d,d):
        self.connection = MySQLdb.connect(host_d,pas_d,user_d,d)
        self.connection.set_character_set('utf8')
        self.cursor = self.connection.cursor()
        self.cursor.execute('SET NAMES utf8;')
        self.cursor.execute('SET CHARACTER SET utf8;')
        self.cursor.execute('SET character_set_connection=utf8;')

    def get_user(self,chat_id):
        """ Получить данные пользователя """
        with self.connection:
            self.cursor.execute("SELECT * FROM question WHERE chat_id="+str(chat_id)+";")
            return self.cursor.fetchone()

    def get_all_user(self):
        """ Получить данные пользователя """
        with self.connection:
            self.cursor.execute("SELECT * FROM question;")
            return self.cursor.fetchall()

    def update_question_result(self, chat_id, question_number,result,type_q):
        """записываем результат в базу данных"""
        with self.connection:
            self.cursor.execute("UPDATE question SET z"+str(question_number)+"_"+type_q+"="+str(result)+" WHERE chat_id = "+str(chat_id)+";")
            self.connection.commit()

    def update_time(self, chat_id, time_q):
        """записываем результат в базу данных"""
        with self.connection:
            self.cursor.execute("UPDATE question SET last_time=\'"+str(time_q)+"\' WHERE chat_id = "+str(chat_id)+";")
            self.connection.commit()

    def get_question_result(self,chat_id,question_number):
        """ Получить данные пользователя """
        with self.connection:
            self.cursor.execute("SELECT z"+question_number+"_0,z"+question_number+"_1 FROM question WHERE chat_id="+str(chat_id)+";")
            return self.cursor.fetchone()

    def insert_user(self, chat_id,first_name='',last_name='',username=''):
        """добавление пользователя в базу данных"""
        with self.connection:
            sql="""INSERT INTO question(chat_id,first_name,last_name,username)
                VALUES ('%(chat_id)s','%(first_name)s','%(last_name)s','%(username)s');
                """%{"chat_id":str(chat_id),"first_name":first_name,"last_name":last_name,"username":username}
            self.cursor.execute(sql)
            self.connection.commit()

    def update_code(self, chat_id,code):
        """записываем результат в базу данных"""
        with self.connection:
            self.cursor.execute("UPDATE question SET code="+str(code)+" WHERE chat_id = "+str(chat_id)+";")
            self.connection.commit()

    def get_explanation(self,question_number):
        """ Получить данные пользователя """
        with self.connection:
            self.cursor.execute("SELECT url FROM explanation WHERE id="+str(question_number)+";")
            return self.cursor.fetchone()


    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()