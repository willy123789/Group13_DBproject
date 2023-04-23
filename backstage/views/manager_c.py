from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import *
import imp, random, os, string
from werkzeug.utils import secure_filename
from flask import current_app

UPLOAD_FOLDER = 'static/camera'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

manager_c = Blueprint('manager_c', __name__, template_folder='../templates')

def config():
    current_app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    config = current_app.config['UPLOAD_FOLDER'] 
    return config

@manager_c.route('/', methods=['GET', 'POST'])
@login_required
def home():
    return redirect(url_for('manager_c.cameraManager'))

@manager_c.route('/cameraManager', methods=['GET', 'POST'])
@login_required
def cameraManager():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('index'))
        
    if 'delete' in request.values:
        cmid = request.values.get('delete')
        # data = Record.delete_check(cmid)
        
        # if(data != None):
        #     flash('failed')
        # else:
        data = Camera.get_camera(cmid)
        Camera.delete_camera(cmid)
    
    elif 'edit' in request.values:
        cmid = request.values.get('edit')
        return redirect(url_for('manager_c.edit', cmid=cmid))
    
    camera_data = camera()
    return render_template('cameraManager.html', camera_data = camera_data, user=current_user.name)

def camera():
    camera_row = Camera.get_all_camera()
    camera_data = []
    for i in camera_row:
        camera = {
            '相機編號': i[0],
            '相機型號': i[1],
            '相機名稱': i[2],
            '相機畫素': i[3],
            '相機品牌': i[4],
            '相機價格': i[5],
        }
        camera_data.append(camera)
    return camera_data

@manager_c.route('/camera_add', methods=['GET', 'POST'])
def camera_add():
    if request.method == 'POST':
        data = ""
        while(data != None):
            number = str(random.randrange( 10000, 99999))
            en = random.choice(string.ascii_letters)
            cmid = en + number
            data = Camera.get_camera(cmid)

        model = request.values.get('model')
        name = request.values.get('name')
        pixel = request.values.get('pixel')
        brand = request.values.get('brand')
        price = request.values.get('price')

        if (len(name) < 1 or len(price) < 1):
            return redirect(url_for('manager_c.cameraManager'))
        
        Camera.add_camera(
            {
             'cmid' : cmid,
             'model' : model,
             'name' : name,
             'pixel' : pixel,
             'brand' : brand,
             'price' : price,
             }
        )

        return redirect(url_for('manager_c.cameraManager'))

    return render_template('cameraManager.html')

@manager_c.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'GET':
        if(current_user.role == 'user'):
            flash('No permission')
            return redirect(url_for('camerastore'))

    if request.method == 'POST':
        Camera.update_camera(
            {
            'cmid' : request.values.get('cmid'),
            'model' : request.values.get('model'),
            'name' : request.values.get('name'),
            'pixel' : request.values.get('pixel'),
            'brand' : request.values.get('brand'),
            'price' : request.values.get('price')
            }
        )
        
        return redirect(url_for('manager_c.cameraManager'))

    else:
        camera = show_info()
        return render_template('edit.html', data=camera)


def show_info():
    cmid = request.args['cmid']
    data = Camera.get_camera(cmid)
    model = data[1]
    name = data[2]
    pixel = data[3]
    brand = data[4]
    price = data[5]

    camera = {
        '相機編號': cmid,
        '相機型號': model,
        '相機名稱': name,
        '相機畫素': pixel,
        '相機品牌': brand,
        '相機價格': price,
        
    }
    return camera


@manager_c.route('/orderManager', methods=['GET', 'POST'])
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
                '相機名稱': j[1],
                '相機單價': j[2],
                '訂購數量': j[3]
            }
            order_detail.append(orderdetail)

    return render_template('orderManager.html', orderData = order_data, orderDetail = order_detail, user=current_user.name)

