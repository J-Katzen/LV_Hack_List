from flask import Flask, request, session, redirect, render_template, url_for
from flask.ext.pymongo import PyMongo
from models import User, List, Item
from helpers import authorized, ObjectIDConverter
import json
import models

app = Flask(__name__)
app.url_map.converters['ObjectID'] = ObjectIDConverter

# mongodb connections
app.config[
    'MONGO_URI'] = 'mongodb://heroku_app14582889:s69s9ag2v3qrbe0grhvfoem3mg@ds037387.mongolab.com:37387/heroku_app14582889'
mongo = PyMongo(app, config_prefix='MONGO')
# functions needed


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
        user = mongo.db.users.find_one({'username': request.form['username'],
                                        'password': request.form['password']})
        if user == None:
            error = 'Invalid username/password'
        else:
            session['signed_in'] = True
            session['user'] = user
    # the code below this is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('signed_in', None)
    return redirect(url_for('login'))


@app.route('/')
def hello_world():
    return 'hello world!'

if __name__ == '__main__':
    app.run()
