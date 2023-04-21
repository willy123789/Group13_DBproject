from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import *
import imp, random, os, string
from werkzeug.utils import secure_filename
from flask import current_app

UPLOAD_FOLDER = 'static/lens'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

manager_l = Blueprint('manager_l', __name__, template_folder='../templates')

def config():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    config = current_app.config['UPLOAD_FOLDER'] 
    return config

@manager_l.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('manager_l.lensManager'))

@manager_l.route('/lensManager', methods=['GET', 'POST'])
def lensManager():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'delete' in request.values:
        lid = request.values.get('delete')
        # data = Record.delete_check(cmid)
        
        # if(data != None):
        #     flash('failed')
        # else:
        data = Lens.get_lens(lid)
        Lens.delete_lens(lid)
        
    elif 'edit_l' in request.values:
        lid = request.values.get('edit_l')
        return redirect(url_for('manager_l.edit_l', lid=lid))
    
    lens_data = lens()
    return render_template('lensManager.html', lens_data = lens_data, user=current_user.name)

def lens():
    lens_row = Lens.get_all_lens()
    lens_data = []
    for i in lens_row:
        lens = {
            '鏡頭編號': i[0],
            '鏡頭型號': i[6],
            '鏡頭名稱': i[1],
            '鏡頭光圈': i[3],
            '鏡頭焦段': i[4],
            '鏡頭品牌': i[2],
            '鏡頭價格': i[5],
        }
        lens_data.append(lens)
    return lens_data

@manager_l.route('/lens_add', methods=['GET', 'POST'])
def lens_add():
    if request.method == 'POST':
        data = ""
        while(data != None):
            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            lid = en + number
            data = Lens.get_lens(lid)

        model = request.values.get('model')
        name = request.values.get('name')
        aperture = request.values.get('aperture')
        focal_lenth = request.values.get('focal_lenth')
        brand = request.values.get('brand')
        price = request.values.get('price')

        if (len(name) < 1 or len(price) < 1):
            return redirect(url_for('manager_l.lensManager'))
        
        Lens.add_lens(
            {
             'lid' : lid,
             'model' : model,
             'name' : name,
             'aperture' : aperture,
             'focal_lenth' : focal_lenth,
             'brand' : brand,
             'price' : price,
             }
        )

        return redirect(url_for('manager_l.lensManager'))

    return render_template('lensManager.html')

@manager_l.route('/edit_l', methods=['GET', 'POST'])
@login_required
def edit_l():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('camerastore'))

    if request.method == 'POST':
        Lens.update_lens(
            {
            'lid' : request.values.get('lid'),
            'model' : request.values.get('model'),
            'name' : request.values.get('name'),
            'aperture' : request.values.get('aperture'),
            'focal_lenth' : request.values.get('focal_lenth'),
            'brand' : request.values.get('brand'),
            'price' : request.values.get('price')
            }
        )
        
        return redirect(url_for('manager_l.lensManager'))

    else:
        lens = show_info()
        return render_template('edit_l.html', data=lens)


def show_info():
    lid = request.args['lid']
    data = Lens.get_lens(lid)
    model = data[6]
    name = data[1]
    aperture = data[3]
    focal_lenth = data[4]
    brand = data[2]
    price = data[5]

    lens = {
        '鏡頭編號': lid,
        '鏡頭型號': model,
        '鏡頭名稱': name,
        '鏡頭光圈': aperture,
        '鏡頭焦段': focal_lenth,
        '鏡頭品牌': brand,
        '鏡頭價格': price,
        
    }
    return lens


@manager_l.route('/orderManager', methods=['GET', 'POST'])
@login_required
def orderManager():
    if request.method == 'POST':
        pass
    else:
        order_row = Order_List.get_order()
        order_data = []
        for i in order_row:
            order = {
                '訂單編號': i[0],
                '訂購人': i[1],
                '訂單總價': i[2],
                '訂單時間': i[3]
            }
            order_data.append(order)
            
        orderdetail_row = Order_List.get_orderdetail()
        order_detail = []

        for j in orderdetail_row:
            orderdetail = {
                '訂單編號': j[0],
                '商品名稱': j[1],
                '商品單價': j[2],
                '訂購數量': j[3]
            }
            order_detail.append(orderdetail)

    return render_template('orderManager.html', orderData = order_data, orderDetail = order_detail, user=current_user.name)

