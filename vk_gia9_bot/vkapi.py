# -*- coding: utf-8 -*-
import vk
import json
from config import token,gid,token,app_token,debug
import requests


session = vk.Session(access_token=token)
#session = vk.AuthSession(6456799,'alexu-che@yandex.ru','xtndthujfff123',scope='photos')
api = vk.API(session, v=5.74)



def send_message(user_id, message, attachment="",tkn=token):
    api.messages.send(access_token=tkn, user_id=str(user_id), message=message, attachment=attachment)

def user_get(user_id):
    data=api.users.get(user_ids=user_id,fields='domain')[0]
    return data['first_name'], data['last_name'],data['domain']

def upload_photo_album(filename,album_id,tkn=app_token,group_id=gid):
    upload_url = api.photos.getUploadServer(group_id=group_id,album_id=album_id,access_token=tkn)['upload_url']
    request = requests.post(upload_url, files={'photo': open(filename, "rb")})
    params = {'album_id':album_id,
        'group_id':group_id,
        'server': request.json()['server'],
        'photos_list': request.json()['photos_list'],
        'aid': request.json()['aid'],
        'hash': request.json()['hash']}
    photo_id = api.photos.save(**params)[0]['id']
    return photo_id

def send_photo (user_id,filename,tkn=token,group_id=gid):
    upload_url = api.photos.getMessagesUploadServer(peer_id=str(user_id))['upload_url']
    if debug==1: print ('upload_url=',upload_url)
    request = requests.post(upload_url, files={'photo': open(filename, "rb")})
    if debug==1: print ('request=',request)
    params = {'server': request.json()['server'],
        'photo': request.json()['photo'],
        'hash': request.json()['hash']}
    photo_id = api.photos.saveMessagesPhoto(**params)[0]['id']
    send_message(user_id,'','photo'+str(user_id)+'_'+str(photo_id))