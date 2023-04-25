
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
from api.sql import Member,Cart, Camera, Record

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
        cursor.prepare('SELECT * FROM CAMERA WHERE CMNAME LIKE :search')
        cursor.execute(None, {'search': '%' + keyword + '%'})
        camera_row = cursor.fetchall()
        camera_data = []
        final_data = []
        
        for i in camera_row:
            camera = {
                '相機編號': i[0],
                '相機名稱': i[2],
                '相機價格': i[5],
                '相機圖片': i[1]+'.png',
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
    
    elif 'sort' in request.args:
        single = 1
        sort = request.values.get('sort')

        method = sort
        camera_row = Camera.get_cmaera_sort(method)
        camera_data = []
        total = 0
        
        for i in camera_row:
            camera = {
                '相機編號': i[0],
                '相機名稱': i[2],
                '相機品牌': i[4],
                '相機價格': i[5],
                '相機圖片': i[1]+'.png',
            }

            camera_data.append(camera)
            total = total + 1
            
        if(len(camera_data) < 9):
            flag = 1
        
        count = math.ceil(total/9)    
        
        return render_template('camerastore.html', method=sort, single=single, camera_data=camera_data, user=current_user.name, page=1, flag=flag, count=count)    




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
    
    elif 'brand' in request.args:
        single = 1
        brand = request.args['brand']
        camera_row = Camera.get_camera_bybrand(brand)
        camera_data = []
        total = 0
        for i in camera_row:
            camera = {
                '相機編號': i[0],
                '相機名稱': i[2],
                '相機品牌': i[4],
                '相機價格': i[5],
                '相機圖片': i[1]+'.png',
            }
            camera_data.append(camera)
            total = total + 1
            
        if(len(camera_data) < 9):
            flag = 1
        
        count = math.ceil(total/9) 

        return render_template('camerastore.html',single = single ,camera_data=camera_data, user=current_user.name, page=1, flag=flag, count=count)


    elif 'brand' in request.args and 'page' in request.args:
        total = 0
        single = 1
        page = int(request.args['page'])
        start = (page - 1) * 9
        end = page * 9

        brand = request.args['brand']
        camera_row = Camera.get_camera_bybrand(brand)
        camera_data = []
        for i in camera_row:
            camera = {
                '相機編號': i[0],
                '相機名稱': i[2],
                '相機品牌': i[4],
                '相機價格': i[5],
                '相機圖片': i[1]+'.png',
            }
            camera_data.append(camera)
            total = total + 1

        if(len(camera_data) < end):
            end = len(camera_data)
            flag = 1
            
        for j in range(start, end):
            final_data.append(camera_data[j])
            
        count = math.ceil(total/9)
            
        return render_template('camerastore.html',single = single ,camera_data=camera_data, user=current_user.name, page=1, flag=flag, count=count)

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
                '相機圖片': i[1]+'.png',
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
                '相機價格': i[5],
                '相機圖片': i[1]+'.png',
            }

            camera_data.append(camera)
            total = total + 1
            
        if(len(camera_data) < 9):
            flag = 1
        
        count = math.ceil(total/9)    
        
        return render_template('camerastore.html', keyword=search, single=single, camera_data=camera_data, user=current_user.name, page=1, flag=flag, count=count)    
    
    else:
        camera_row = Camera.get_all_camera()
        brand_row = Brand.get_all_brand()
        camera_data = []
        brand_data = []
        temp = 0
        for i in camera_row:
            camera = {
                '相機編號': i[0],
                '相機名稱': i[2],
                '相機品牌': i[4],
                '相機價格': i[5],
                '相機圖片': i[1]+'.png',
            }
            if len(camera_data) < 9:
                camera_data.append(camera)

        for i in brand_row:
            brand = {
                '品牌名稱': i[0],
            }
            brand_data.append(brand)
        
        return render_template('camerastore.html', camera_data=camera_data,brand_data=brand_data, user=current_user.name, page=1, flag=flag, count=count)

#lens_start
@store.route('/lensstore', methods=['GET', 'POST'])
@login_required
def lensstore():
    result = Lens.count()
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
        cursor.prepare('SELECT * FROM LENS WHERE LNAME LIKE :search')
        cursor.execute(None, {'search': '%' + keyword + '%'})
        lens_row = cursor.fetchall()
        lens_data = []
        final_data = []
        
        for i in lens_row:
            lens = {
                '鏡頭編號': i[0],
                '鏡頭名稱': i[1],
                '鏡頭價格': i[5],
                '鏡頭圖片': i[6]+'.png',
            }
            lens_data.append(lens)
            total = total + 1
        
        if(len(lens_data) < end):
            end = len(lens_data)
            flag = 1
            
        for j in range(start, end):
            final_data.append(lens_data[j])
            
        count = math.ceil(total/9)
        
        return render_template('lensstore.html', single=single, keyword=search, lens_data=lens_data, user=current_user.name, page=1, flag=flag, count=count)    
    # return render_template('lensstore.html')
    
    elif 'lid' in request.args:
        lid = request.args['lid']
        data = Lens.get_lens(lid)
        
        brand = data[2]
        name = data[1]
        aperture = data[3]
        focal_lenth = data[4]
        model = data[6]
        price = data[5]
        image = model+'.png'
        
        lens = {
        '鏡頭編號': lid,
        '鏡頭型號': model,
        '鏡頭品牌': brand,
        '鏡頭名稱': name,
        '鏡頭光圈': aperture,
        '鏡頭焦段': focal_lenth,
        '鏡頭價格': price,
        '鏡頭圖片': image,
        }

        return render_template('lens.html', lens = lens, user=current_user.name)
    
    elif 'page' in request.args:
        page = int(request.args['page'])
        start = (page - 1) * 9
        end = page * 9
        
        lens_row = Lens.get_all_lens()
        lens_data = []
        final_data = []
            
        for i in lens_row:
            lens = {
                '鏡頭編號': i[0],
                '鏡頭型號': i[6],
                '鏡頭品牌': i[2],
                '鏡頭名稱': i[1],
                '鏡頭光圈': i[3],
                '鏡頭焦段': i[4],
                '鏡頭價格': i[5],
                '鏡頭圖片': i[6]+'.png',
            }
            lens_data.append(lens)
            
        if(len(lens_data) < end):
            end = len(lens_data)
            flag = 1
            
        for j in range(start, end):
            final_data.append(lens_data[j])
        
        return render_template('lensstore.html', lens_data=final_data, user=current_user.name, page=page, flag=flag, count=count)    
    
    elif 'keyword' in request.args:
        single = 1
        search = request.values.get('keyword')
        keyword = search
        cursor = DB.connect()
        cursor.prepare('SELECT * FROM lens WHERE LNAME LIKE :search')
        cursor.execute(None, {'search': '%' + keyword + '%'})
        lens_row = cursor.fetchall()
        lens_data = []
        total = 0
        
        for i in lens_row:
            lens = {
                '鏡頭編號': i[0],
                '鏡頭名稱': i[1],
                '鏡頭品牌': i[2],
                '鏡頭價格': i[5],
                '鏡頭圖片': i[6]+'.png',
            }

            lens_data.append(lens)
            total = total + 1
            
        if(len(lens_data) < 9):
            flag = 1
        
        count = math.ceil(total/9)    
        
        return render_template('lensstore.html', keyword=search, single=single, lens_data=lens_data, user=current_user.name, page=1, flag=flag, count=count)    
    
    else:
        lens_row = Lens.get_all_lens()
        lens_data = []
        temp = 0
        for i in lens_row:
            lens = {
                '鏡頭編號': i[0],
                '鏡頭名稱': i[1],
                '鏡頭品牌': i[2],
                '鏡頭價格': i[5],
                '鏡頭圖片': i[6]+'.png',
            }
            if len(lens_data) < 9:
                lens_data.append(lens)
        
        return render_template('lensstore.html', lens_data=lens_data, user=current_user.name, page=1, flag=flag, count=count)





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
            cmid = request.values.get('cmid') # 使用者想要購買的相機
            lid = request.values.get('lid') # 使用者想要購買的鏡頭
            # 檢查購物車裡面有沒有商品
            camera = Record.check_camera(cmid, tno)
            # 取得商品價錢
            price = Camera.get_camera(cmid)[5]

            # 如果購物車裡面沒有的話 把他加一個進去
            if(camera == None):
                Record.add_camera( {'id': cmid, 'tno':tno, 'price':price, 'total':price} )
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
    
@store.route('/order')
def order():
    data = Cart.get_cart(current_user.id)
    tno = data[2]

    camera_row = Record.get_record(tno)
    camera_data = []

    for i in camera_row:
        cmname = Camera.get_name(i[1])
        camera = {
            '相機編號': i[1],
            '相機名稱': cmname,
            '相機價格': i[3],
            '數量': i[2]
        }
        camera_data.append(camera)
    
    total = Record.get_total(tno)[0]

    return render_template('order.html', data=camera_data, total=total, user=current_user.name)

def change_order():
    data = Cart.get_cart(current_user.id)
    tno = data[2] # 使用者有購物車了，購物車的交易編號是什麼
    camera_row = Record.get_record(data[2])

    for i in camera_row:
        
        # i[0]：交易編號 / i[1]：商品編號 / i[2]：數量 / i[3]：價格
        if int(request.form[i[1]]) != i[2]:
            Record.update_camera({
                'amount':request.form[i[1]],
                'cmid':i[1],
                'tno':tno,
                'total':int(request.form[i[1]])*int(i[3])
            })
            print('change')

    return 0

def only_cart():
    
    count = Cart.check(current_user.id)

    if(count == None):
        return 0
    
    data = Cart.get_cart(current_user.id)
    tno = data[2]
    camera_row = Record.get_record(tno)
    camera_data = []

    for i in camera_row:
        cmid = i[1]
        name = Camera.get_name(i[1])
        price = i[3]
        amount = i[2]
        
        camera = {
            '相機編號': cmid,
            '相機名稱': name,
            '相機價格': price,
            '數量': amount
        }
        camera_data.append(camera)
    
    return camera_data


# brand
@store.route('/brand_page', methods=['GET', 'POST'])
@login_required
def brand_page():
    if 'bname' in request.args:
        bname = request.args['bname']
        data = Brand.get_brand(bname)
        
        name = data[0]
        desc = data[1]
        addr = data[2]
        image = name+'.png'
        
        brand = {
        '品牌名稱': name,
        '品牌描述': desc,
        '品牌網址': addr,
        '品牌圖片': image,
        }

        return render_template('brand.html', brand = brand, user=current_user.name)
    
    else:
        return render_template('camerastore.html')
