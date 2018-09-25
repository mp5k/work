# coding: utf-8
import ssl
import os

class BaseConfig(object) :
    PORT = 443 #bluemix will be set automatically
    HOST = '0.0.0.0'
    SECRET_KEY = os.urandom(24)
    DEBUG = False
    ASSISTANT_VERSION = '2018-08-30'
    ASSISTANT_USERNAME = '0cb2ee89-74e8-4051-9edb-f27d163e9b38'
    ASSISTANT_PASSWORD = 'mtigwya1idgC'
    PROTOCOL = ssl.PROTOCOL_TLS
    SERVER_CERT = ''
    SERVER_KEY =''
    CONFIDENCE = 0.19 #確信度の足切り

class RuleConciergeConfig(BaseConfig) :
    ASSISTANT_WORKSPACE = '589ec8f3-a609-4260-b4e7-36c7f0b674f3'

class DebugConfig(RuleConciergeConfig) :
    DEBUG = True
    PORT = 8383
    PROTOCOL = ssl.PROTOCOL_TLS
    SERVER_CERT = './instance/cert.crt'
    SERVER_KEY ='./instance/server_secret.key'



