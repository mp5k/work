# coding: utf-8

from flask import Flask, Response ,render_template ,\
                  request, abort, redirect,url_for
from flask_login import LoginManager,login_user, logout_user, login_required
from chatbot import Chatbot
from auth.user import User, UsersRepository
import os
import json
import ssl

app = Flask(__name__, instance_relative_config=True)

#read config
app.config.from_object('config.RuleConciergeConfig')
app.secret_key = app.config['SECRET_KEY']
DEBUG = app.config['DEBUG']

#ssl settings
if DEBUG:
    sslcontext = ssl.SSLContext(app.config['PROTOCOL'])
    sslcontext.load_cert_chain(app.config['SERVER_CERT'], app.config['SERVER_KEY'])

#login settings
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' #login_viewのroute
users_repository = UsersRepository()
users_repository.save_user(User(username='gss', password='0128', id=1))

@login_manager.user_loader
def load_user(user_id):
    """
    user loader for login manager
    """
    return users_repository.get_user_by_id(user_id)


#init chatbot instance
chatbot = Chatbot(
    version=app.config['ASSISTANT_VERSION'],
    username=app.config['ASSISTANT_USERNAME'],
    password=app.config['ASSISTANT_PASSWORD'],
    workspace_id=app.config['ASSISTANT_WORKSPACE'],
    debug = DEBUG
)

@app.route('/')
@app.route('/index')
@login_required
def index():
    """
    protected homepage
    """
    return render_template('botui.html')

@app.route('/send_message/<message>')
def send_message(message):
    """
    send message and receive response
    """
    global chatbot
    return json.dumps(chatbot.send(message,app.config['CONFIDENCE']))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        #TestMode----------------------------------------------
        workspaceid = request.form.get('workspaceid', '')
        global chatbot
        if len(workspaceid) > 0 :
            chatbot = Chatbot(
                version=app.config['ASSISTANT_VERSION'],
                username=app.config['ASSISTANT_USERNAME'],
                password=app.config['ASSISTANT_PASSWORD'],
                workspace_id=workspaceid,
                debug = DEBUG
            )
        else :
            chatbot = Chatbot(
                version=app.config['ASSISTANT_VERSION'],
                username=app.config['ASSISTANT_USERNAME'],
                password=app.config['ASSISTANT_PASSWORD'],
                workspace_id=app.config['ASSISTANT_WORKSPACE'],
                debug = DEBUG
            )
        #------------------------------------------------------
        
        registeredUser = users_repository.get_user(username)
        if registeredUser == None:
            return abort(401)
        print('Users '+ str(users_repository.users))
        print('Register user %s , password %s' % (registeredUser.username, registeredUser.password))
        if registeredUser != None and registeredUser.password == password:
            print('Logged in..')
            login_user(registeredUser)
            return redirect(url_for("index"))
        else:
            return abort(401)
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.errorhandler(401)
def page_not_found(e):
    """
    handle login failed
    """
    return Response('<p>ログインに失敗しました。</p>')

if __name__ == '__main__':
    port = int(os.getenv('PORT', app.config['PORT'])) #bluemix will be set automatically
    if DEBUG:
        app.run(host=app.config['HOST'], port=port,ssl_context=sslcontext, threaded=False, debug=True)
    else :
        app.run(host=app.config['HOST'], port=port, threaded=True)
