import imp
from flask import render_template, Blueprint, redirect, request, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from link import *
from api.sql import *

api = Blueprint('api', __name__, template_folder='./templates')

login_manager = LoginManager(api)
login_manager.login_view = 'api.login'
login_manager.login_message = "請先登入"

class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(userid):  
    user = User()
    user.id = userid
    data = Member.get_role(userid)
    try:
        user.role = data[0]
        user.name = data[1]
    except:
        pass
    return user

# print(user_loader(63))
print("######################")
camera_row = Camera.get_all_camera()
camera_data = []
final_data = []
print(camera_row)    
print("######################")

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

# print(camera_data)
for i in camera_data:
    print(i)
