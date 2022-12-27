from flask import Flask, Response, session, jsonify, request, render_template
import os.path
import sqlite3
import datetime
import shutil
from flask import send_file
import json
import threading
import requests
import time

con = sqlite3.connect('story.db', check_same_thread=False)
c = con.cursor()


c.execute("CREATE TABLE IF NOT EXISTS stroy_group (no INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, type INTEGER, content TEXT, regdate date, UNIQUE(name))")

c.execute("CREATE TABLE IF NOT EXISTS user (no INTEGER PRIMARY KEY AUTOINCREMENT, id TEXT, password TEXT, stroy_group_name TEXT, name TEXT, phone TEXT, regdate date, UNIQUE(id))")

c.execute("CREATE TABLE IF NOT EXISTS story (no INTEGER PRIMARY KEY AUTOINCREMENT, user_no INTEGER, user_id TEXT, title TEXT, story_group_name TEXT, content TEXT, usespecial INTEGER, regdate date)")
c.execute("CREATE TABLE IF NOT EXISTS story_version (no INTEGER PRIMARY KEY AUTOINCREMENT, user_no INTEGER, story_no INTEGER, version TEXT, content TEXT, localpath TEXT, regdate date)")
c.execute("CREATE TABLE IF NOT EXISTS story_version_file (story_version_no INTEGER, path TEXT, hash text)")

c.execute("CREATE TABLE IF NOT EXISTS story_version_content (no INTEGER PRIMARY KEY AUTOINCREMENT, user_no INTEGER, story_no INTEGER, version_no INTEGER, content TEXT, regdate date)")


c.execute("CREATE TABLE IF NOT EXISTS git (no INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, content TEXT, regdate date, UNIQUE(name))")


c.execute("INSERT OR IGNORE INTO stroy_group(name, type, content, regdate) VALUES('동화콘텐츠제공자', 1, '동화 콘텐츠를 제공하는 자', '2022-07-05')")
c.execute("INSERT OR IGNORE INTO stroy_group(name, type, content, regdate) VALUES('부산도서관', 2, '부산 도서관용 컨텐츠', '2022-07-05')")
c.execute("INSERT OR IGNORE INTO stroy_group(name, type, content, regdate) VALUES('대전도서관', 2, '대전 도서관용 컨텐츠', '2022-07-05')")
c.execute("INSERT OR IGNORE INTO stroy_group(name, type, content, regdate) VALUES('서울도서관', 2, '서울 도서관용 컨텐츠', '2022-07-05')")

c.execute("INSERT OR IGNORE INTO stroy_group(name, type, content, regdate) VALUES('부산도서관 콘텐츠 개발자 그룹', 1, '부산도서관 콘텐츠 개발자 그룹', '2022-07-05')")
c.execute("INSERT OR IGNORE INTO stroy_group(name, type, content, regdate) VALUES('대전도서관 콘텐츠 개발자 그룹', 1, '대전도서관 콘텐츠 개발자 그룹', '2022-07-05')")

c.execute("INSERT OR IGNORE INTO user(id, password, stroy_group_name, name, phone, regdate) VALUES('edy100', 'edy100', '동화콘텐츠제공자', '이길동', '010-2567-8301', '2022-07-05')")
c.execute("INSERT OR IGNORE INTO user(id, password, stroy_group_name, name, phone, regdate) VALUES('edy200', 'edy200', '부산도서관', '홍길동', '010-2567-8301', '2022-07-05')")
c.execute("INSERT OR IGNORE INTO user(id, password, stroy_group_name, name, phone, regdate) VALUES('edy300', 'edy300', '대전도서관', '김길동', '010-2567-8301','2022-07-05')")
c.execute("INSERT OR IGNORE INTO user(id, password, stroy_group_name, name, phone, regdate) VALUES('edy400', 'edy400', '서울도서관', '박길동', '010-2567-8301','2022-07-05')")

c.execute("INSERT OR IGNORE INTO user(id, password, stroy_group_name, name, phone, regdate) VALUES('edy400', 'edy400', '서울도서관', '박길동', '010-2567-8301','2022-07-05')")
c.execute("INSERT OR IGNORE INTO user(id, password, stroy_group_name, name, phone, regdate) VALUES('edy400', 'edy400', '서울도서관', '박길동', '010-2567-8301','2022-07-05')")

c.execute("INSERT OR IGNORE INTO user(id, password, stroy_group_name, name, phone, regdate) VALUES('edy500', 'edy500', '부산도서관 콘텐츠 개발자 그룹', '저길동', '010-2567-8301','2022-07-05')")


c.execute("INSERT OR IGNORE INTO git(name, content, regdate) VALUES('Microsoft Airsim simulator', 'https://github.com/microsoft/AirSim.git', '2022-07-05')")
c.execute("INSERT OR IGNORE INTO git(name, content, regdate) VALUES('ShaderConductor is a tool designed for cross-compiling HLSL to other shading languages', 'https://github.com/EpicGames/ShaderConductor.git', '2022-07-05')")
c.execute("INSERT OR IGNORE INTO git(name, content, regdate) VALUES('Docker Compose v2', 'https://github.com/docker/compose.git', '2022-07-05')")


con.commit()

lock = threading.Lock()

app = Flask(__name__)

app.secret_key = 'story_session_key'

app.config.from_object(__name__)

def root_dir():
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    ROOT_DIR = os.path.join(ROOT_DIR, 'files')
    return ROOT_DIR

print('root_dir : ', root_dir())

app.config['UPLOAD_FOLDER'] = root_dir()

def get_file(filename):
    try:
        src = os.path.join(root_dir(), filename)
        return src
    except IOError as exc:
        return str(exc), None

def row_to_dict(cursor: sqlite3.Cursor, row: sqlite3.Row) -> dict:
    data = {}
    for idx, col in enumerate(cursor.description):
        data[col[0]] = row[idx]
    return data

def createDir(dirname):
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

def removeDir(dirname):
    shutil.rmtree(dirname)

createDir(root_dir())

@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route("/userinfo")
def userinfo():
    return render_template('user.html')

    
@app.route("/groupinfo")
def groupinfo():
    return render_template('group.html')

@app.route("/gitinfo")
def gitinfo():
    return render_template('git.html')

@app.route("/gitdetailinfo")
def gitdetailinfo():
    return render_template('gitdetail.html')





@app.route("/login", methods=['POST'])
def user_loing():
    print(request.is_json)
    user_info = request.get_json()


    if 'id' not in user_info:
        return jsonify({'error': 'id is not exists.'}), 404

    if 'passwd' not in user_info:
        return jsonify({'error': 'passwd is not exists.'}), 404

    if user_info['id'] is None:
        return jsonify({'error': 'id value is None'}), 404

    if user_info['passwd'] is None:
        return jsonify({'error': 'passwd value is None'}), 404

    lock.acquire(True)

    r = c.execute("SELECT * FROM user where id='{0}' and password='{1}'".format(user_info['id'], user_info['passwd']))

    login = False
    for row in r :
        login = True
        d = row_to_dict(c, row)

        session['user_no'] = d['no']
        session['user_id'] = d['id']
        session['group'] = d['stroy_group_name']

        r = c.execute("SELECT * FROM stroy_group where name='{0}'".format(session['group']))

        for row in r :
            d = row_to_dict(c, row)
            session['group_type'] = d['type']

        


    
        

    lock.release()




    if login:
        return jsonify({'result': 'success', 'id':session['user_id'], 'group':session['group'], 'group_type' : session['group_type']}), 200
    else:
        return jsonify({'result': 'fail'}), 200


@app.route("/login", methods=['GET'])
def user_logout():

    session.pop('user_no')
    session.pop('user_id')
    session.pop('group')
    

    return jsonify({'result': 'success'}), 200


@app.route("/user", methods=['GET','POST','PUT','DELETE'])
def user():
    if request.method == 'GET':
        users = []
        lock.acquire(True)

        r = c.execute('SELECT * FROM user')
        for row in r :
            d = row_to_dict(c, row)
            users.append(d)

        lock.release()

        return jsonify(users), 200


@app.route("/group", methods=['GET','POST','PUT','DELETE'])
def group():

    if request.method == 'GET':

        stroy_group = []

        lock.acquire(True)

        r = c.execute('SELECT * FROM stroy_group')
        for row in r :
            d = row_to_dict(c, row)
            stroy_group.append(d)
        
        lock.release()
        return jsonify(stroy_group), 200
       

last_gits = None
last_ts = 0

@app.route("/git", methods=['GET','POST','PUT','DELETE'])
def git():
    global last_gits, last_ts

    if request.method == 'GET':
        gits = []
        no = 0
        lock.acquire(True)

        r = c.execute('SELECT * FROM git')
        for row in r :
            d = row_to_dict(c, row)
            d['no'] = no
            gits.append(d)
            no = no + 1

        lock.release()

        return jsonify(gits), 200
    elif request.method == 'POST':

        if request.json == None:
            return jsonify({'error': 'not json type'}), 403


        if 'name' not in request.json:
            return jsonify({'error': 'name is empty'}), 403
        
        if 'url' not in request.json:
            return jsonify({'error': 'url is empty'}), 403

        lock.acquire(True)

        c.execute("INSERT OR IGNORE INTO git(name, content, regdate) VALUES('{0}', '{1}', '{2}')".format(request.json['name'], request.json['url'], datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        con.commit()

        lock.release()

        last_gits = None
        last_ts = 0
        return jsonify({'result': 'success'}), 201
    elif request.method == 'PUT':
        last_gits = None
        last_ts = 0
    elif request.method == 'DELETE':
        last_gits = None
        last_ts = 0
        



@app.route("/gitdetail", methods=['GET'])
def gitdetail():
    global last_gits, last_ts

    if last_gits != None:
        ts = time.time()

        if ts - last_ts < 300:
            return jsonify(last_gits), 200

    gits = []

    headers = {'Accept': 'application/vnd.github+json',
        'Authorization': 'Bearer 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'}

    no = 1

    r = c.execute('SELECT * FROM git')
    for row in r :
        d = row_to_dict(c, row)

        content = d['content']

        r1 = content.split('/')

        if len(r1) >= 2:
            repo = r1[-1]
            owner = r1[-2]

            repo = repo.replace('.git','')

            response = requests.get("https://api.github.com/repos/{0}/{1}/branches".format(owner, repo), headers=headers)
            data = response.json()

            for d1 in data:
                d3 = {}
                d3['no'] = no
                d3['name'] = d['name']
                
                d3['regdate'] = d['regdate']

                d3['branch'] = d1['name']
                d3['sha'] = d1['commit']['sha']
                d3['url'] = d['content'].replace('.git','')+'/tree/'+d1['name']
                gits.append(d3)
                no = no + 1


        
    last_ts = time.time()
    last_gits = gits

    return jsonify(gits), 200
    

@app.route("/story", methods=['GET','POST','PUT','DELETE'])
def story():
   
    if 'user_id' not in session:
        return jsonify({'error': 'you must login. user_id'}), 403
    else:
        user_id = session['user_id']

    if 'user_no' not in session:
        return jsonify({'error': 'you must login. user_no'}), 403
    else:
        user_no = session['user_no']
    

    is_success = True


    if request.method == 'GET':
        stories = []

        s_username = None

        lock.acquire(True)
        
        try:
            if user_id == None:
                r = c.execute('SELECT * FROM story')
            else:
                r = c.execute("SELECT * FROM story where user_id = '{0}'".format(user_id))

            for row in r :
                d = row_to_dict(c, row)
                d['version'] = []
                stories.append(d)

            
            for story in stories:
                r1 = c.execute("SELECT * FROM story_version where story_no={0}".format(story['no']))

                for row1 in r1:
                    d1 = row_to_dict(c, row1)
                    story['version'].append(d1)

            for story in stories:
                for v in story['version']:
                    r1 = c.execute("SELECT * FROM story_version_content where version_no={0}".format(v['no']))
                    v['content'] = {}
                    for row1 in r1:
                        d1 = row_to_dict(c, row1)

                        cont = json.loads(d1['content'])
                        d1['content'] = cont
                        v['content'] = d1
                        break

        except Exception as e:
            print(e)
            is_success = False
        finally:
            lock.release()
               
        if is_success:
            return jsonify(stories)
        else:
            return jsonify({'result': 'fail'}), 500

    elif request.method == 'POST':
        title = request.args.get('title')
        group_name = request.args.get('group')
        usespecial = request.args.get('usespecial')
        content = request.data.decode('utf-8')

        lock.acquire(True)

        try:
            r = c.execute("SELECT * FROM story where title='{0}'".format(title))

            for row in r:
                lock.release()
                return jsonify({'error': 'title['+title+'] is already exists.'}), 406

            t = "INSERT INTO story(user_no, user_id, title, story_group_name, content, usespecial, regdate) VALUES({0}, '{1}', '{2}', '{3}', '{4}', {5}, '{6}')".format(user_no, user_id, title, group_name, content, usespecial, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            
            c.execute("INSERT INTO story(user_no, user_id, title, story_group_name, content, usespecial, regdate) VALUES({0}, '{1}', '{2}', '{3}', '{4}', {5}, '{6}')".format(user_no, user_id, title, group_name, content, usespecial, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) )
            con.commit()
        
        except Exception as e:
            print(e)
            is_success = False
        finally:
            lock.release()

        
        if is_success:
            return jsonify({'result': 'success'}), 201
        else:
            return jsonify({'result': 'fail'}), 500

    elif request.method == 'PUT':
        title = request.args.get('title')
        group_name = request.args.get('group')
        usespecial = request.args.get('usespecial')
        content = request.data.decode('utf-8')

        lock.acquire(True)

        try:

            r = c.execute("SELECT * FROM story where title='{0}'".format(title))

            if r.arraysize == 0:
                lock.release()
                return jsonify({'error': 'title['+title+'] is not exists.'}), 404

            for row in r:
                break

            d = row_to_dict(c, row)
            
            c.execute("UPDATE story set content='{0}', regdate='{1}', story_group_name='{2}', usespecial={3} where no = {4}".format(content, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), group_name, usespecial, d['no']) )
            con.commit()

        except Exception as e:
            print(e)
            is_success = False
        finally:
            lock.release()

        if is_success:
            return jsonify({'result': 'success'}), 201
        else:
            return jsonify({'result': 'fail'}), 500

    elif request.method == 'DELETE':

        is_success = True
        try:
            no = request.args.get('no')
            content = request.data.decode('utf-8')
            title = request.args.get('title')

            lock.acquire(True)

            r = c.execute("SELECT * FROM story where no='{0}'".format(no))

            if r.arraysize == 0:
                lock.release()
                return jsonify({'error': 'no['+no+'] is not exists.'}), 404

            for row in r:
                break

            r = c.execute("SELECT * FROM story_version where story_no='{0}'".format(no))

            for row in r:
                d = row_to_dict(c, row)
                removeDir(root_dir()+'/'+no)
            
            c.execute("DELETE from story where no = {0}".format(no) )
            con.commit()
            
        except Exception as e:
            print(e)
            is_success = False
        finally:
            lock.release()

        if is_success:
            return jsonify({'result': 'success'}), 201
        else:
            return jsonify({'result': 'fail'}), 500

@app.route("/story/<title>", methods=['GET'])
def programs(title):

    if 'user_id' not in session:
        return jsonify({'error': 'you must login. user_id'}), 403
    else:
        user_id = session['user_id']

    if 'user_no' not in session:
        return jsonify({'error': 'you must login. user_no'}), 403
    else:
        user_no = session['user_no']

    if request.method == 'GET':
        lock.acquire(True)

        r = c.execute("SELECT * FROM story where title='{0}'".format(title))

        for row in r :
            lock.release()
            return jsonify(row)

        lock.release()

        return jsonify({'error': 'title['+title+'] is already exists.'}), 406




@app.route("/story/<title>/<version>", methods=['GET','POST','PUT'])
def program_version(title, version):

    if 'user_id' not in session:
        return jsonify({'error': 'you must login. user_id'}), 403
    else:
        user_id = session['user_id']

    if 'user_no' not in session:
        return jsonify({'error': 'you must login. user_no'}), 403
    else:
        user_no = session['user_no']

    if request.method == 'GET':
        stories = []

       
        s_username = None

        lock.acquire(True)

        if user_id == None:
            r = c.execute('SELECT * FROM story')
        else:
            r = c.execute("SELECT * FROM story where user_id = '{0}'".format(user_id))

        for row in r :
            stories.append(row_to_dict(c, row))

        lock.release()
        
        return jsonify(stories)
    elif request.method == 'POST':

        localpath = request.args.get('localpath')

        lock.acquire(True)

        r = c.execute("SELECT * FROM story where title='{0}'".format(title))

        story = None
        for row in r :
            story = row_to_dict(c, row)
            break

        if story is None:
            lock.release()
            return jsonify({'error': 'title['+title+'] is not exists.'}), 404

        story_no = story['no']
        story_no_ = story['no']

        r = c.execute("SELECT * FROM story_version where story_no={0} and version='{1}'".format(story['no'], version))

        has = False
        for row in r :
            has = True
            break

        
        if has:
            up = "update story_version set content='{0}', regdate='{1}', localpath='{4}' where story_no={2} and version='{3}'".format('', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), story['no'], version, localpath)
            c.execute(up)
        else:
            c.execute("INSERT INTO story_version(user_no, story_no, version, content, localpath, regdate) VALUES({0}, '{1}', '{2}', '{3}', '{4}', '{5}')".format(user_no, story['no'], version, '', localpath, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) )
        
        con.commit()


        r = c.execute("SELECT * FROM story_version where story_no={0} and version='{1}'".format(story['no'], version))

        for row in r :
            story_version = row_to_dict(c, row)
            break

        lock.release()

        story_no = str(story_no)
        story_version_no_ = story_version['no']
        story_version_no = str(story_version['no'])

        createDir(root_dir()+'/'+story_no)
        createDir(root_dir()+'/'+story_no+'/'+story_version_no)

        content = request.data.decode('utf-8')
        storyfiles = json.loads(content)

        stories = []
        paths = []
        for s in storyfiles:
            paths.append(s['Path'])
            s.pop('FullPath')
            s.pop('Uploaded')

            stories.append(s)

        content = json.dumps(stories)

        
        
        lock.acquire(True)

        

        
        
        lock.release()

        remove_story_version_files = []
        

        if len(paths) > 0:
            lock.acquire(True)

            s = str(paths)[1:-1]
            q = "SELECT * FROM story_version_file where story_version_no={0} and path not in({1})".format(story_version['no'],s)
            r = c.execute(q)

            for row in r:
                story_version_file = row_to_dict(c, row)

                remove_story_version_files.append(story_version_file)
            lock.release()

                

        lock.acquire(True)
        for remove_f in remove_story_version_files:
            c.execute("delete from story_version_file where story_version_no={0} and hash = '{1}'".format(remove_f['story_version_no'], remove_f['hash']))
            remove_path = get_file(story_no+'/'+story_version_no+'/'+remove_f['path']).replace("\\","/")
            try:
                os.remove(remove_path)
            except:
                print('error remove file : ',remove_path)
            
        con.commit()

        

        r = c.execute("SELECT * FROM story_version_file where story_version_no={0}".format(story_version['no']))
        story_version_files = []

        udate_stories = []

        for row in r :
            story_version_file = row_to_dict(c, row)
            story_version_files.append(story_version_file)
        
        lock.release()

        for story in stories:
            is_found = False
            story['Uploaded'] = False
            story['story_no'] = story_no_
            story['story_version_no'] = story_version_no_
            for story_version_file in story_version_files:
                if story['Path'] == story_version_file['path']:
                    is_found = True
                    break

            if is_found:
                file_path = get_file(story_no+'/'+story_version_no+'/'+story_version_file['path']).replace("\\","/")
                if os.path.exists(file_path):
                    story['Uploaded'] = True

            
            udate_stories.append(story)

            
        return jsonify(udate_stories)
    
    if request.method == 'PUT':
        story_no = request.args.get('story_no')
        story_version_no = request.args.get('story_version_no')
        path = request.args.get('path')

        hash = request.args.get('hash')

        if request.data is not None:
            path_ = path.replace("\\","/")
            path_ = get_file(story_no+'/'+story_version_no+'/'+path_).replace("\\","/")
            
            os.makedirs(os.path.dirname(path_), exist_ok=True)

            newfile=open(path_,'wb')
            newfile.write(request.data)
            newfile.close()
            lock.acquire(True)
            c.execute("insert into story_version_file(story_version_no, path, hash) VALUES({0}, '{1}', '{2}')".format(story_version_no, path, hash))
            
            con.commit()
            lock.release()



        return jsonify({"result":"ok"})



@app.route("/story_content/<title>/<version>", methods=['GET','POST','PUT'])
def story_content(title, version):

    if 'user_id' not in session:
        return jsonify({'error': 'you must login. user_id'}), 403
    else:
        user_id = session['user_id']

    if 'user_no' not in session:
        return jsonify({'error': 'you must login. user_no'}), 403
    else:
        user_no = session['user_no']

    if request.method == 'GET':
        stories = []


        s_username = None

        lock.acquire(True)

        if user_id == None:
            r = c.execute('SELECT * FROM story')
        else:
            r = c.execute("SELECT * FROM story where user_id = '{0}'".format(user_id))

        for row in r :
            stories.append(row_to_dict(c, row))

        lock.release()
        
        return jsonify(stories)
    elif request.method == 'POST':

        lock.acquire(True)

        r = c.execute("SELECT * FROM story where title='{0}'".format(title))

        story = None
        for row in r :
            story = row_to_dict(c, row)
            break

        if story is None:
            lock.release()
            return jsonify({'error': 'title['+title+'] is not exists.'}), 404

        r = c.execute("SELECT * FROM story_version where story_no={0} and version='{1}'".format(story['no'], version))


        story_version = None
        for row in r:
            story_version = row_to_dict(c, row)
            break

        if story_version is None:
            c.execute("INSERT INTO story_version(user_no, story_no, version, content, localpath, regdate) VALUES({0}, '{1}', '{2}', '{3}', '{4}', '{5}')".format(user_no, story['no'], version, '', '', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) )
            con.commit()
            r = c.execute("SELECT * FROM story_version where story_no={0} and version='{1}'".format(story['no'], version))
            for row in r:
                story_version = row_to_dict(c, row)

        lock.release()


        content = request.data.decode('utf-8')

        lock.acquire(True)

        r = c.execute("SELECT * FROM story_version_content where story_no={0} and version_no='{1}'".format(story['no'], story_version['no']))

        story_version_content = None
        for row in r:
            story_version_content = row_to_dict(c, row)
            break

        if story_version_content is None:
            r = c.execute("insert into story_version_content(user_no, story_no, version_no, content, regdate) VALUES({0}, {1}, {2},'{3}', '{4}')".format(user_no, story['no'], story_version['no'], content, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")) )
        else:
            c.execute("UPDATE story_version_content set content='{0}', regdate='{1}' where no = {2}".format(content, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), story_version_content['no']) )

        lock.release()

        return jsonify({'result': 'success'}), 201

@app.route("/all_story", methods=['GET'])
def all_story():
    lock.acquire(True)

    r = c.execute("SELECT * FROM story")
    
    stories = []
    
    for row in r :
        d = row_to_dict(c, row)
        d['version'] = []
        stories.append(d)

    
    for story in stories:
        r1 = c.execute("SELECT * FROM story_version where story_no={0}".format(story['no']))

        for row1 in r1:
            d1 = row_to_dict(c, row1)
            story['version'].append(d1)

    for story in stories:
        for v in story['version']:
            r1 = c.execute("SELECT * FROM story_version_content where version_no={0}".format(v['no']))
            v['content'] = {}
            for row1 in r1:
                d1 = row_to_dict(c, row1)

                cont = json.loads(d1['content'])
                d1['content'] = cont
                v['content'] = d1
                break

    
    lock.release()

    return jsonify(stories)



@app.route("/all_story/<story_group_name>", methods=['GET'])
def all_story_by_type(story_group_name):
    lock.acquire(True)

    r = c.execute("SELECT * FROM story where story_group_name='{0}'".format(story_group_name))
    
    stories = []
    
    for row in r :
        d = row_to_dict(c, row)
        d['version'] = []
        stories.append(d)

    
    for story in stories:
        r1 = c.execute("SELECT * FROM story_version where story_no={0}".format(story['no']))

        for row1 in r1:
            d1 = row_to_dict(c, row1)
            story['version'].append(d1)

    for story in stories:
        for v in story['version']:
            r1 = c.execute("SELECT * FROM story_version_content where version_no={0}".format(v['no']))
            v['content'] = {}
            for row1 in r1:
                d1 = row_to_dict(c, row1)

                cont = json.loads(d1['content'])
                d1['content'] = cont
                v['content'] = d1
                break

    
    lock.release()

    return jsonify(stories)





@app.route("/story_version/<story_version_no>", methods=['GET'])
def story_version(story_version_no):
    r = c.execute("SELECT * FROM story_version_file where story_version_no={0}".format(story_version_no))
    story_files = []
    for row in r :
        d = row_to_dict(c, row)
        story_files.append(d)
    
    return jsonify(story_files)

@app.route('/download/<story_no>/<story_version_no>', methods=['GET'])
def download(story_no, story_version_no):
    path =  request.args.get('path')
    src = get_file(story_no+'/'+story_version_no+'/'+path.replace("\\","/"))
    return send_file(src, as_attachment=True)
    
if __name__ == '__main__':
      app.run(threaded=True, host='0.0.0.0', port=5003)
