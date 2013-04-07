from flask import Flask, request, session, redirect, render_template, url_for
from flask.ext.pymongo import PyMongo
from models import User, List, Item
from helpers import authorized, ObjectIDConverter
from bs4 import BeautifulSoup
from base64 import b64encode
import json
import models
import urllib2

app = Flask(__name__)
app.url_map.converters['ObjectID'] = ObjectIDConverter
app.secret_key = '\x93Y\xc3 o^$\x03\xfa\x9c\xbe\xa9x\x9dR\x94\xcd\xd9k\x9e\x9e#\x94\xca'
# mongodb connections
app.debug = True
app.config[
    'MONGO_URI'] = 'mongodb://heroku_app14582889:s69s9ag2v3qrbe0grhvfoem3mg@ds037387.mongolab.com:37387/heroku_app14582889'
mongo = PyMongo(app, config_prefix='MONGO')
# functions needed


@app.route('/product_parse', methods=['POST'])
@authorized
def parse_amazon_item():
    url = request.form['amazon_url']
    page = urllib2.urlopen(url).read()
    soup = BeautifulSoup(page)
    image_url = soup.select("#main-image")[0]['src']
    name = soup.select("#btAsinTitle")[0].text
    descript = soup.select(".productDescriptionWrapper")[0].text[:160] + "..."
    obj = {'name': name, 'image_url': image_url, 'desription': descript}
    return json.dumps(obj)


@app.route('/new_list', methods=['POST'])
@authorized
def make_list():
    new_list = List()
    new_list.name = request.form['name']
    new_list.type = request.form['type']
    new_list.list_url = ''
    new_list.owner_email = session['user']['email']
    lists = mongo.db.lists
    list_id = lists.insert(new_list.__dict__)
    encoded = b64encode(list_id.__str__())
    url = 'http://lit-ravine-8874.herokuapp.com/list/' + encoded
    mongo.db.lists.update({'_id': list_id}, {'$set': {'list_url': url}})
    return redirect(url_for('user_lists'))


@app.route('/list/<ObjectID:listid>/remove')
@authorized
def rem_list(listid):
    print listid
    success = mongo.db.lists.remove({'_id': listid})
    return success


@app.route('/list/<ObjectID:listid>/new_item', methods=['POST'])
@authorized
def add_item(listid):
    new_item = Item()
    new_item.name = request.form['name']
    new_item.image_url = request.form['type']
    new_item.link = request.form['link']
    new_item.note = request.form['notes']
    s_list = mongo.db.lists.find_one({'_id': listid})
    item_count = s_list['item_count']
    new_item.id = item_count
    if item_count == 0:
        mongo.db.lists.update({'_id': listid}, {'$set': {'default_image': new_item.image_url}})
    item_count += 1
    mongo.db.lists.update({'_id': listid}, {'$push': {'items': new_item.__dict__}})
    mongo.db.lists.update({'_id': listid}, {'$set': {'item_count': item_count}})
    return 'update made!'


# currently broken and don't know why...
@app.route('/list/<ObjectID:listid>/<item_id>')
@authorized
def remove_item(listid, item_id):
    mongo.db.lists.update({'_id': listid}, {'$pull': {'items': {'id': item_id}}})
    return 'removal done!'


@app.route('/list/<ObjectID:listid>', methods=['GET'])
def get_list(listid):
    single_list = mongo.db.lists.find_one({'_id': listid})

    return render_template('entries.html', one_list=single_list)
    # return render_template('single_list.html', single_list=single_list)


@app.route('/user/lists')
@authorized
def user_lists():
    user = session['user']
    lists = mongo.db.lists.find({'owner_email': user['email']})
    return render_template('profile.html', lists=lists, username=session['user'])


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = mongo.db.users.find_one({'email': email,
                                        'password': password})
        if user == None:
            error = 'Invalid username/password'
            session.pop('signed_in', None)
        else:
            session['signed_in'] = True
            session['user'] = user
            return redirect(url_for('user_lists'))
    # the code below this is executed if the request method
    # was GET or the credentials were invalid
    return '...!'


@app.route('/logout')
def logout():
    session.pop('signed_in', None)
    return redirect(url_for('hello_world'))


@app.route('/register', methods=['POST'])
def register_user():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['fullname']
        if mongo.db.users.find_one({'email': email}) == None:
            users = mongo.db.users
            user_id = users.insert({'email': email, 'password': password, 'fullname': name})
            return redirect(url_for('hello_world'))
        else:
            return redirect(url_for('hello_world'))


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/testforms')
def test_forms():
    return render_template('testForms.html')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
