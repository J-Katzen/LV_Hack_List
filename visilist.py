from flask import Flask, request, session, redirect, render_template, url_for
from flask.ext.pymongo import PyMongo
from models import User, List, Item
from helpers import authorized, ObjectIDConverter
from bs4 import BeautifulSoup
import json
import models
import urllib2

app = Flask(__name__)
app.url_map.converters['ObjectID'] = ObjectIDConverter

# mongodb connections
app.config[
    'MONGO_URI'] = 'mongodb://heroku_app14582889:s69s9ag2v3qrbe0grhvfoem3mg@ds037387.mongolab.com:37387/heroku_app14582889'
mongo = PyMongo(app, config_prefix='MONGO')
# functions needed


@app.route('/product_parse', methods=['POST'])
@authorized()
def parse_amazon_item():
    url = request.form['amazon_url']
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    image_url = soup.find(id="main-image")['src']
    name = soup.find(id="btAsinTitle").text
    descript = soup.find(id="postBodyPS").p.text[:160] + "..."
    obj = {'name': name, 'image_url': image_url, 'desription': descript}
    return json.dumps(obj)

@app.route('/new_list', methods=['POST'])
@authorized()
def make_list():
    new_list = List()
    new_list.name = request.form['name']
    new_list.type = request.form['type']
    new_list.list_url = ''
    lists = mongo.db.lists
    list_id = lists.insert(new_list.__dict__)
    return redirect(url_for('user_lists'))


@app.route('/list/<ObjectID:listid>/new_item', methods=['POST'])
@authorized()
def add_item(listid):
    new_item = Item()
    new_item.name = request.form['name']
    new_item.image_url = request.form['type']
    new_item.link = request.form['link']
    new_item.note = request.form['notes']
    s_list = mongo.db.users.find({'_id': listid})
    item_count = s_list.item_count
    new_item.id = item_count
    item_count += 1
    mongo.db.users.update({'_id': listid}, {'$push': {'items': new_item}})
    mongo.db.users.update({'_id': listid}, {'$set': {'item_count': item_count}})
    return redirect('/list/' + listid)


@authorized()
@app.route('/list/<ObjectID:listid>/<item_id>')
def remove_item(listid, item_id):
    s_list = mongo.db.users.update({'_id': listid},
                                   {'$pull': {'items': item_id}})


@app.route('/list/<ObjectID:listid>', methods=['GET'])
def get_list(listid):
    single_list = mongo.db.users.find_one({'_id': listid})
    return render_template('single_list.html', single_list=single_list)


@app.route('/user/lists')
@authorized()
def user_lists():
    user = session['user']
    lists = mongo.db.lists.find({'email': user.email})
    return render_template('user_lists.html', lists=lists)


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = mongo.db.users.find_one({'email': request.form['email'],
                                        'password': request.form['password']})
        if user == None:
            error = 'Invalid username/password'
            return error
        else:
            session['signed_in'] = True
            session['user'] = user
    # the code below this is executed if the request method
    # was GET or the credentials were invalid
    return 'Success!'


@app.route('/logout')
def logout():
    session.pop('signed_in', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if mongo.db.users.find_one({'email': email}) == None:
            users = mongo.db.users
            user_id = users.insert({'email': email, 'password': password})
            return 'success!'
        else:
            return 'fail!'


@app.route('/')
def hello_world():
    return 'hello world!'

if __name__ == '__main__':
    app.run()