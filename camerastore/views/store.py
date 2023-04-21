
import re
from typing_extensions import Self
from typing import Optional
from flask import Flask, request, template_rendered, Blueprint
from flask import url_for, redirect, flash
from flask import render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from numpy import identity, product
import random, string
from sqlalchemy import null
from link import *
import math
from base64 import b64encode
from api.api import *
from api.sql import Member,Cart, Camera

store = Blueprint('camerastore', __name__, template_folder='../templates')


@store.route('/', methods=['GET', 'POST'])
@login_required
def camerastore():
    result = Camera.count()
    count = math.ceil(result[0]/9)
    flag = 0
    
    

    if request.method == 'GET':
        if(current_user.role == 'manager'):
            flash('No permission')
            return redirect(url_for('manager_c.home'))

    if 'keyword' in request.args and 'page' in request.args:
        total = 0
        single = 1
        page = int(request.args['page'])
        start = (page - 1) * 9
        end = page * 9
        search = request.values.get('keyword')
        keyword = search
        
        cursor = DB.connect()
        cursor.prepare('SELECT * FROM CAMERA WHERE PNAME LIKE :search')
        cursor.execute(None, {'search': '%' + keyword + '%'})
        camera_row = cursor.fetchall()
        camera_data = []
        final_data = []
        
        for i in camera_row:
            camera = {
                '相機編號': i[0],
                '相機名稱': i[2],
                '相機價格': i[5]
            }
            camera_data.append(camera)
            total = total + 1
        
        if(len(camera_data) < end):
            end = len(camera_data)
            flag = 1
            
        for j in range(start, end):
            final_data.append(camera_data[j])
            
        count = math.ceil(total/9)
        
        return render_template('camerastore.html', single=single, keyword=search, camera_data=camera_data, user=current_user.name, page=1, flag=flag, count=count)    
    # return render_template('camerastore.html')
    
    elif 'cmid' in request.args:
        cmid = request.args['cmid']
        data = Camera.get_camera(cmid)
        
        brand = data[4]
        name = data[2]
        pixel = data[3]
        model = data[1]
        price = data[5]
        image = model+'.png'
        
        camera = {
        '相機編號': cmid,
        '相機型號': model,
        '相機名稱': name,
        '相機畫素': pixel,
        '相機品牌': brand,
        '相機價格': price,
        '相機圖片': image,
        }

        return render_template('camera.html', camera = camera, user=current_user.name)
    
    elif 'page' in request.args:
        page = int(request.args['page'])
        start = (page - 1) * 9
        end = page * 9
        
        camera_row = Camera.get_all_camera()
        camera_data = []
        final_data = []
            
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
            
        if(len(camera_data) < end):
            end = len(camera_data)
            flag = 1
            
        for j in range(start, end):
            final_data.append(camera_data[j])
        
        return render_template('camerastore.html', camera_data=final_data, user=current_user.name, page=page, flag=flag, count=count)    
    
    elif 'keyword' in request.args:
        single = 1
        search = request.values.get('keyword')
        keyword = search
        cursor = DB.connect()
        cursor.prepare('SELECT * FROM Camera WHERE CMNAME LIKE :search')
        cursor.execute(None, {'search': '%' + keyword + '%'})
        camera_row = cursor.fetchall()
        camera_data = []
        total = 0
        
        for i in camera_row:
            camera = {
                '相機編號': i[0],
                '相機名稱': i[2],
                '相機品牌': i[4],
                '相機價格': i[5]
            }

            camera_data.append(camera)
            total = total + 1
            
        if(len(camera_data) < 9):
            flag = 1
        
        count = math.ceil(total/9)    
        
        return render_template('camerastore.html', keyword=search, single=single, camera_data=camera_data, user=current_user.name, page=1, flag=flag, count=count)    
    
    else:
        camera_row = Camera.get_all_camera()
        camera_data = []
        temp = 0
        for i in camera_row:
            camera = {
                '相機編號': i[0],
                '相機名稱': i[2],
                '相機品牌': i[4],
                '相機價格': i[5]
            }
            if len(camera_data) < 9:
                camera_data.append(camera)
        
        return render_template('camerastore.html', camera_data=camera_data, user=current_user.name, page=1, flag=flag, count=count)

# 會員購物車
@store.route('/cart', methods=['GET', 'POST'])
@login_required # 使用者登入後才可以看
def cart():

    # 以防管理者誤闖
    if request.method == 'GET':
        if( current_user.role == 'manager'):
            flash('No permission')
            return redirect(url_for('manager.home'))

    # 回傳有 cmid 代表要 加商品
    if request.method == 'POST':
        
        if "cmid" in request.form :
            data = Cart.get_cart(current_user.id)
            
            if( data == None): #假如購物車裡面沒有他的資料
                time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                Cart.add_cart(current_user.id, time) # 幫他加一台購物車
                data = Cart.get_cart(current_user.id) 
                
            tno = data[2] # 取得交易編號
            cmid = request.values.get('cmid') # 使用者想要購買的東西
            # 檢查購物車裡面有沒有商品
            camera = Record.check_camera(cmid, tno)
            # 取得商品價錢
            price = Camera.get_camera(cmid)[2]

            # 如果購物車裡面沒有的話 把他加一個進去
            if(camera == None):
                Record.add_camera( {'id': tno, 'tno':cmid, 'price':price, 'total':price} )
            else:
                # 假如購物車裡面有的話，就多加一個進去
                amount = Record.get_amount(tno, cmid)
                total = (amount+1)*int(price)
                Record.update_camera({'amount':amount+1, 'tno':tno , 'cmid':cmid, 'total':total})

        elif "delete" in request.form :
            cmid = request.values.get('delete')
            tno = Cart.get_cart(current_user.id)[2]
            
            Member.delete_camera(tno, cmid)
            camera_data = only_cart()
        
        elif "user_edit" in request.form:
            change_order()  
            return redirect(url_for('camerastore.camerastore'))
        
        elif "buy" in request.form:
            change_order()
            return redirect(url_for('camerastore.order'))

        elif "order" in request.form:
            tno = Cart.get_cart(current_user.id)[2]
            total = Record.get_total_money(tno)
            Cart.clear_cart(current_user.id)

            time = str(datetime.now().strftime('%Y/%m/%d %H:%M:%S'))
            format = 'yyyy/mm/dd hh24:mi:ss'
            Order_List.add_order( {'mid': current_user.id, 'time':time, 'total':total, 'format':format, 'tno':tno} )

            return render_template('complete.html', user=current_user.name)

    camera_data = only_cart()
    
    if camera_data == 0:
        return render_template('empty.html', user=current_user.name)
    else:
        return render_template('cart.html', data=camera_data, user=current_user.name)


