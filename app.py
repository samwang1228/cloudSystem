# public module
import csv
from fileinput import filename
import json
from datetime import datetime
import sqlite3
import time
import subprocess
import pathlib
import random 
from flask import Flask, g, flash, url_for, redirect,  render_template, request, session, abort, redirect
from flask_login import LoginManager, UserMixin, LoginManager, login_user, logout_user, login_required, current_user
import os
from flask_ngrok import run_with_ngrok
import time
# from pip._vendor import cachecontrol
from functools import wraps
from werkzeug.middleware.proxy_fix import ProxyFix

# solve login status
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)

# import requests
# your model
# 取得目前檔案所在的資料夾
# 要使用current_user來記錄登入資訊
# current_user.get.id() 6796
SRC_PATH =  pathlib.Path(__file__).parent.absolute()
UPLOAD_FOLDER = os.path.join(SRC_PATH,  'static', 'uploads')
ALLOWED_EXTENSIONS = {'mp3'}
# rsplit('.', 1)[1]取得副檔名，1是只切一刀(兩等分),從'.'開始切故[0]為filename
id_db = 'user'
password_db = '123456'
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in  ALLOWED_EXTENSIONS
app = Flask(__name__)
# run_with_ngrok(app)
app.secret_key =  b'_5#y2L"F4Q8z\n\xec]/' 
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER          # 設置儲存上傳檔的資料夾 
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024  * 1024 * 1024 # 上傳檔最大16GB
# user=''
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message = ""
login_manager.login_message_category = "info"

SQLITE_DB_PATH = 'backend/SparkVideo.db'
SQLITE_DB_SCHEMA = 'backend/create_db.sql'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(SQLITE_DB_PATH)
        # Enable foreign key check
        db.execute("PRAGMA foreign_keys = ON")
    return db


def reset_db():
    with open(SQLITE_DB_SCHEMA, 'r') as f:
        create_db_sql = f.read()
    db = get_db()
    # Reset database
    # Note that CREATE/DROP table are *immediately* committed
    # even inside a transaction
    with db:
        db.execute("PRAGMA foreign_keys = OFF")
        db.execute("DROP TABLE IF EXISTS members")
        db.execute("PRAGMA foreign_keys = ON")
        db.executescript(create_db_sql)
        db.execute (
            'INSERT INTO members (account, password) VALUES ("user", "123456")'
        )

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

class User(UserMixin):
    pass

def to_json(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        get_fun = func(*args, **kwargs)
        return json.dumps(get_fun)

    return wrapper


def query_user(username):
    # user = UserAccounts.query.filter_by(UserName=username).first()
    if username == id_db:
        return True
    return False

@login_manager.user_loader
def user_loader(user_id):
    db = get_db()
    password = db.execute(
        'SELECT password FROM members WHERE account = ?', (user_id, )
    ).fetchall()

    if not password:
        return

    user = User()
    user.id = user_id
    return user

@login_manager.request_loader
def request_loader(request):

    user_id = request.form.get('ID')

    db = get_db()
    password = db.execute(
        'SELECT password FROM members WHERE account = ?', (user_id, )
    ).fetchall()

    if not password:
        return

    user = User()
    user.id = user_id
    
    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!

    return user if (request.form['password'] == password[0][0]) else None
 
@app.route('/')
#@login_required
def index():
    category=['Openpose','Yolo','Flow Chart','category','category','category']
    projectName=['運動員骨架抓取','辨識球員','相關技術','Project Name','Project Name','Project Name']
    className=['Openpose-Result','Yolo-Result','Flow-Chart','Project-Name','Project-Name','Project-Name']
    linkName=['Openpose Result','Yolo Result','Flow Chart','Project Name','Project Name','Project Name']
    user_id = session.get('user_id')
    
    return render_template('index.html',u=current_user.get_id(),projectName=projectName,category=category,className=className,linkName=linkName)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            abort(401)
        else:
            return function()
    return wrapper

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'GET':
        return render_template('register.html')

    user_id = request.form['ID']
    user_password = request.form['password']
    check_passowrd= request.form.get('checkpassword')

    if(user_password != check_passowrd):
        errorMsg='<span style="color:#35858B">__</span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>您輸入的密碼有誤'
        return render_template('register.html', errorMsg = errorMsg)

    db = get_db()

    try:
        with db:
            db.execute (
                'INSERT INTO members (account, password) VALUES (?, ?)',
                (user_id, user_password)
            )
    except sqlite3.IntegrityError:
        errorMsg='<span style="color:#35858B">__</span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>該帳號已有人使用'
        return render_template('register.html', errorMsg = errorMsg)
    filepath = os.path.join(SRC_PATH,  'static', 'uploads',user_id)
    os.makedirs(filepath, exist_ok=True)
    return redirect( url_for('index') )

@app.route('/login.html', methods=['GET', 'POST']) #登入
def login():
    btn_check=None
    if request.method == 'GET':
        return render_template("login.html")

    #使用帳號密碼登入
    try:
        btn_check=request.form["normal_btn"]
        
    except:
        btn_check=request.form["google_btn"]
    if(btn_check=='登入'):
        user_id = request.form['ID']
        user_password = request.form['password']
        db = get_db()
        password = db.execute(
            'SELECT password FROM members WHERE account = ?', (user_id, )
        ).fetchall()
        if not password:
            errorMsg='<span style="color:#35858B">__</span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>您輸入的帳號不存在'
            return render_template('login.html', errorMsg = errorMsg)
    
        password = password[0][0]
        
        if user_password != password:
            errorMsg='<span style="color:#35858B">__</span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>您輸入的帳號或密碼有誤'
            return render_template('login.html', errorMsg = errorMsg)

         
    if(btn_check=='使用google登入'):
        authorization_url, state = flow.authorization_url()  #asking the flow class for the authorization (login) url
        session["state"] = state
        return redirect(authorization_url)

    
    user = User()
    user.id = user_id 
    login_user(user)
    username = current_user.get_id()
    return render_template('user.html',user=username)

 
@app.route('/manager', methods=['GET', 'POST']) #登入  
def manager():
    user=current_user.get_id()
    if(user != 'user'):
        return redirect( url_for('index') )
    db = get_db()
    user_id = db.execute(
            'SELECT account FROM members '
        ).fetchall()
    password = db.execute(
            'SELECT password FROM members '
        ).fetchall()
    size = len(user_id)
    return render_template('manager.html',user=user,user_id=user_id,password=password,size=size)
 

@app.route("/user.html")
@login_required
def user():
    username = current_user.get_id()
    return render_template('user.html',user=username)

@app.route('/status')
def read_text():
    text=''
    # path = os.path.join('share','uploads','user','result')
    path='/share'
    obj = os.scandir(path)
    cnt=0
    # print("Files and Directories in '% s':" % path)
    for entry in obj :
        if(entry.name=='songs'):
            continue
        state = os.path.join(path , entry.name,'computing')
        output = os.path.join(path , entry.name ,'output.txt')
        inputfile = os.path.join(path , entry.name ,'input.mp3')
        lr=os.path.join(path,entry.name,'outputlyric.txt')
        melody=os.path.join(path,entry.name,'outputmelody.txt')
        text+=entry.name
        text+=' '
        if os.path.isfile(output) and os.path.isfile(melody) and os.path.isfile(melody):
            text+='3'
        elif os.path.isfile(state):
            text+='2'
        
        elif os.path.isfile(inputfile):
            text+='1'
        text+=' '
    return text

@app.route('/text')
def get_text():
    # path = os.path.join('share','uploads','user','result')
    path = '/share'
    obj = os.scandir(path)
    cnt=0
    tt=0
    # print("Files and Directories in '% s':" % path)
    for entry in obj :
        if(entry.name=='songs'):
            tt=0
        else:
            cnt+=1
    return render_template('test.html',size=cnt)

@app.route('/top')
def show_top():
    process = subprocess.Popen(['top', '-bn', '1', '-i', '-c'], stdout=subprocess.PIPE)
    output, error = process.communicate()
    top_output = output.decode('utf-8').split('\n')
    return render_template('cpu.html', top_output=top_output)


@app.route('/user.html', methods=['POST'])
@login_required
def upload_file():
    root=''
    info=[]
    filename=''
    lr=[]
    url=[]
    me=[]
    username = current_user.get_id()
    if 'filename' not in request.files:   # 如果表單的「檔案」欄位沒有'filename'
        flash('沒有上傳檔案')
        # return redirect(url_for('index'))

    file = request.files['filename']    # 取得上傳的檔案 
    if file.filename == '':           #  若上傳的檔名是空白的… 
        flash('請選擇要上傳的影像')   # 發出快閃訊息 
        # return redirect(url_for('index'))   # 令瀏覽器跳回首頁 
    if file and allowed_file(file.filename):   # 確認有檔案且副檔名在允許之列
        # filename = secure_filename(file.filename)  # 轉成「安全的檔名」 
        
        # filename = file.filename
        
        # filepath = os.path.join(SRC_PATH,  'share', 'uploads',username)
        t=time.time()
        r=random.randrange(0, 101, 2)
        filepath='/share/' + str(t)  +str(r)
        os.makedirs(filepath ,exist_ok=True)
        file.save(os.path.join(filepath, 'input.mp3'))
        #  result path
        # filepath = os.path.join(SRC_PATH,  'share', 'uploads',username,'result',filename.split('.')[0])
        # os.makedirs(filepath, exist_ok=True)
        info.clear()
        ryric=''
        filedir=filepath+'/output.txt'
        filename = 'output.txt'
        os.chmod(filepath, 0o777)
        os.chmod(filepath+'/input.mp3', 0o777)
        while(1):
            if(os.path.isfile(filepath +'/output.txt') and os.path.isfile(filepath +'/computing2')):
                break
        f = open(filedir,'r')
        # data=f.read()
        # info.append()
        cnt=0
        for line in f.readlines():
            cnt+=1
            print('--------',cnt,'---------')
            if(cnt>=4):
                ryric+=str(line)
            info.append(line)
        f.close
        filedir = filepath+'/outputlyric.txt'
        f = open(filedir,'r')
        for line in f.readlines():
            lr.append(line[0:line.find('https/')])
            url.append(line[line.find('http'):len(line)-1])
        # time.sleep(10)
        f.close
        picUrl=str(info[2])
        root=f'{filepath}\\' #影片的位置
        video_name=filename #影片的名字
        flash('檔案上傳完畢！')
        filedir = filepath + '/outputmelody.txt'
        f = open(filedir,'r')
        # 顯示頁面並傳入上傳的檔名
        for line in f.readlines():
            me.append(line)
        return render_template('user.html', user=username,filename=filename,name=info[1],songname=info[0],song=ryric,link=picUrl[6:len(picUrl)-1],size=len(url),url=url,lr=lr,me=me,size2=len(me))
        # return render_template('user.html', user=username,filename=filename,name=data,songname=filedir,song=data,link=data)
    else:
        errorMsg='<i class="bi bi-exclamation-triangle-fill"></i> 僅允許上傳mp4、mov影像檔'
        return render_template('user.html',errorMsg=errorMsg,user=username)  # 令瀏覽器跳回首頁

@app.errorhandler(413)
def page_not_found(e):
    errorMsg='<i class="bi bi-exclamation-triangle-fill"></i>僅允許上傳16GB的影像檔'
    return render_template('user.html',errorMsg=errorMsg)

@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', error = 'Not Found'), 404
    
@app.route('/logout')
def logout():
    user_id = current_user.get_id()
    logout_user()
    return redirect( url_for('index') )


if __name__ == '__main__':
    # app.run()
    app.run(debug = True,host = '0.0.0.0')

