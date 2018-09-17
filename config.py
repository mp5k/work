# coding: utf-8
import ssl
import os

class BaseConfig(object) :
    PORT = 443 #bluemix will be set automatically
    HOST = '0.0.0.0'
    SECRET_KEY = os.urandom(24)
    DEBUG = False
    ASSISTANT_VERSION = '2018-07-13'
    ASSISTANT_USERNAME = 'XXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
    ASSISTANT_PASSWORD = 'XXXXXXXXXXXX'
    PROTOCOL = ssl.PROTOCOL_TLS
    SERVER_CERT = ''
    SERVER_KEY =''
    CONFIDENCE = 0.19 #確信度の足切り

class RuleConciergeConfig(BaseConfig) :
    ASSISTANT_WORKSPACE = 'XXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'

class DebugConfig(RuleConciergeConfig) :
    DEBUG = True
    PORT = 8383
    PROTOCOL = ssl.PROTOCOL_TLS
    SERVER_CERT = './instance/cert.crt'
    SERVER_KEY ='./instance/server_secret.key'



