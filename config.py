# coding: utf-8
import ssl
import os

class BaseConfig(object) :
    PORT = 443 #bluemix will be set automatically
    HOST = '0.0.0.0'
    SECRET_KEY = os.urandom(24)
    DEBUG = False
    ASSISTANT_VERSION = '2018-07-13'
    ASSISTANT_USERNAME = '58057b1d-6f4f-4e8f-ae6a-05a5eb7c8ba6'
    ASSISTANT_PASSWORD = 'RmDgN2rq2QJO'
    PROTOCOL = ssl.PROTOCOL_TLS
    SERVER_CERT = ''
    SERVER_KEY =''
    CONFIDENCE = 0.19 #確信度の足切り

class RuleConciergeConfig(BaseConfig) :
    ASSISTANT_WORKSPACE = 'f22900fa-fe38-4a1c-bf09-0bc3e0e68e04'

class DebugConfig(RuleConciergeConfig) :
    DEBUG = True
    PORT = 8383
    PROTOCOL = ssl.PROTOCOL_TLS
    SERVER_CERT = './instance/cert.crt'
    SERVER_KEY ='./instance/server_secret.key'



