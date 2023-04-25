import oracledb
from link import *
from typing import Optional

class DB():
    def connect():
        cursor = connection.cursor()
        return cursor

    def prepare(sql):
        cursor = DB.connect()
        cursor.prepare(sql)
        return cursor

    def execute(cursor, sql):
        cursor.execute(sql)
        return cursor

    # def execute_input(cursor, sql, input):
    def execute_input(cursor,input):
        cursor.execute(None, input)
        return cursor

    def fetchall(cursor):
        return cursor.fetchall()

    def fetchone(cursor):
        return cursor.fetchone()

    def commit():
        connection.commit()

class Member():
    
    def get_member(account):
        sql = "SELECT ACCOUNT, PASSWORD, MID, IDENTITY, MNAME FROM MEMBER WHERE ACCOUNT = :id"
        return DB.fetchall(DB.execute_input(DB.prepare(sql),{'id':account}))

    def get_all_account():
        sql = "SELECT * FROM MEMBER"
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def create_account(input):
        # sql = "INSERT INTO MEMBER(MNAME, MID, MPASSWORD, ADDRESS, TEL) VALUES (:name, :account, :password, :address, :tel)"
        sql = "INSERT INTO MEMBER(MNAME, ACCOUNT, PASSWORD,IDENTITY) VALUES (:name,:account,:password, :identity )"
        DB.execute_input(DB.prepare(sql),input)
        DB.commit()

    def get_role(userid):
        sql = 'SELECT IDENTITY, MNAME FROM MEMBER WHERE MID = :id '
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'id':userid}))

    def delete_account(name):
        sql = "DELETE FROM MEMBER WHERE MNAME = :name"
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
    def delete_camera(tno, cmid):
        sql = "DELETE FROM RECORD WHERE TNO = :tno AND CMID = :cmid"
        DB.execute_input(DB.prepare(sql), {'tno':tno, 'cmid':cmid})
        DB.commit()


class Cart():
    def check(user_id):
        sql = 'SELECT * FROM CART, RECORD WHERE CART.MID = :id AND CART.TNO = RECORD.TNO'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))
        
    def get_cart(user_id):
        sql = 'SELECT * FROM CART WHERE MID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))

    def add_cart(user_id, time):
        sql = 'INSERT INTO CART VALUES (:id, :time, cart_tno_seq.nextval)'
        DB.execute_input( DB.prepare(sql), {'id': user_id, 'time':time})
        DB.commit()

    def clear_cart(user_id):
        sql = 'DELETE FROM CART WHERE MID = :id '
        DB.execute_input( DB.prepare(sql), {'id': user_id})
        DB.commit()

class Camera():
    def count():
        sql = 'SELECT COUNT(*) FROM CAMERA'
        return DB.fetchone(DB.execute(DB.connect(), sql))
    
    def get_camera(cmid):
        sql = 'SELECT * FROM CAMERA WHERE CMID = :cmid'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'cmid': cmid}))
    
    def get_camera_bybrand(brand):
        sql = 'SELECT * FROM CAMERA WHERE CMBRAND = :brand'
        return DB.fetchall(DB.execute_input(DB.prepare(sql), {'brand': brand}))
    
    def get_cmaera_sort(method):
        if method == 'price_asce':
            sql = 'SELECT * FROM CAMERA ORDER BY CAST(CPRICE as NUMBER) asc'
            return DB.fetchall(DB.execute(DB.connect(), sql))
        elif method == 'price_desc':
            sql = 'SELECT * FROM CAMERA ORDER BY CAST(CPRICE as NUMBER) desc'
            return DB.fetchall(DB.execute(DB.connect(), sql))
        elif method == 'pixel_asce':
            sql = 'SELECT * FROM CAMERA ORDER BY CAST(PIXEL as NUMBER) asc'
            return DB.fetchall(DB.execute(DB.connect(), sql))
        elif method == 'pixel_desc':
            sql = 'SELECT * FROM CAMERA ORDER BY CAST(PIXEL as NUMBER) desc'
            return DB.fetchall(DB.execute(DB.connect(), sql))

    
    def get_all_camera():
        sql = 'SELECT * FROM CAMERA'
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def get_model(cmid):
        sql = 'SELECT CMODEL FROM CAMERA WHERE CMID = :cmid'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'cmid': cmid}))[0]
    
    def get_name(cmid):
        sql = 'SELECT CMNAME FROM CAMERA WHERE CMID = :cmid'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'cmid': cmid}))[0]
    
    def add_camera(input):
        sql = 'INSERT INTO CAMERA(CMID,CMODEL,CMNAME,PIXEL,CMBRAND,CPRICE) VALUES (:cmid,:model,:name,:pixel,:brand,:price) '
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def delete_camera(cmid):
        sql = 'DELETE FROM CAMERA WHERE CMID = :cmid'
        DB.execute_input(DB.prepare(sql), {'cmid': cmid})
        DB.commit()

    def update_camera(input):
        sql = 'UPDATE CAMERA SET CMODEL = :model, CMNAME = :name, PIXEL = :pixel, CMBRAND = :brand, CPRICE = :price WHERE CMID = :cmid'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

class Lens():
    def count():
        sql = 'SELECT COUNT(*) FROM LENS'
        return DB.fetchone(DB.execute(DB.connect(), sql))
    
    def get_lens(lid):
        sql = 'SELECT * FROM LENS WHERE LID = :lid'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'lid': lid}))
    
    def get_all_lens():
        sql = 'SELECT * FROM LENS'
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def get_model(lid):
        sql = 'SELECT LMODEL FROM LENS WHERE LID = :lid'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'lid': lid}))[0]
    
    def get_name(lid):
        sql = 'SELECT LNAME FROM LENS WHERE LID = :lid'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'lid': lid}))[0]
    
    def add_lens(input):
        sql = 'INSERT INTO LENS(LID,LNAME,LMODEL,LBRAND,APERTURE,FOCAL_LENTH,LPRICE) VALUES (:lid,:name,:model,:brand,:aperture,:focal_lenth,:price) '
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def delete_lens(lid):
        sql = 'DELETE FROM LENS WHERE LID = :lid'
        DB.execute_input(DB.prepare(sql), {'lid': lid})
        DB.commit()

    def update_lens(input):
        sql = 'UPDATE LENS SET LNAME = :name, LMODEL = :model, LBRAND = :brand, APERTURE = :aperture, FOCAL_LENTH = :focal_lenth, LPRICE = :price WHERE LID = :lid'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()
    
class Brand():
    def get_all_brand():
        sql = 'SELECT * FROM BRAND'
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def get_all_brand_name():
        sql = 'SELECT BNAME FROM BRAND'
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def get_brand(bname):
        sql = 'SELECT * FROM BRAND WHERE BNAME = :bname'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'bname': bname}))
    
    def get_addr(bname):
        sql = 'SELECT BADDR FROM BRAND WHERE BNAME = :bname'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'bname': bname}))
    
    def get_desc(bname):
        sql = 'SELECT BDESC FROM BRAND WHERE BNAME = :bname'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'bname': bname}))
    
    def add_brand(input):
        sql = 'INSERT INTO BRAND VALUES (:name,:desc,:addr)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def update_brand(input):
        sql = 'UPDATE BRAND SET BDESC = :desc, BADDR = :addr WHERE BNAME = :name'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def delete_brand(bname):
        sql = 'DELETE FROM BRAND WHERE BNAME = :bname'
        DB.execute_input(DB.prepare(sql), {'bname': bname})
        DB.commit()
        
class Cart():
    def check(user_id):
        sql = 'SELECT * FROM CART, RECORD WHERE CART.MID = :id AND CART.TNO = RECORD.TNO'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))
    
    def get_cart(user_id):
        sql = 'SELECT * FROM CART WHERE MID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': user_id}))
    
    def add_cart(user_id, time):
        sql = 'INSERT INTO CART(MID,CARTTIME,TNO) VALUES (:id, :time, cart_tno_seq.nextval)'
        DB.execute_input( DB.prepare(sql), {'id': user_id, 'time':time})
        DB.commit()

    def clear_cart(user_id):
        sql = 'DELETE FROM CART WHERE MID = :id '
        DB.execute_input( DB.prepare(sql), {'id': user_id})
        DB.commit()

class Record():
    def get_total_money(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO=:tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'tno': tno}))[0]

    def check_camera(cmid, tno):
        sql = 'SELECT * FROM RECORD WHERE CMID = :id and TNO = :tno'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': cmid, 'tno':tno}))

    def get_price(cmid):
        sql = 'SELECT PRICE FROM CAMERA WHERE CMID = :id'
        return DB.fetchone(DB.execute_input(DB.prepare(sql), {'id': cmid}))[0]

    def add_camera(input):
        sql = 'INSERT INTO RECORD(CMID, TNO, AMOUNT, SALEPRICE, TOTAL) VALUES (:id, :tno, 1, :price, :total)'
        DB.execute_input( DB.prepare(sql), input)
        DB.commit()

    def get_record(tno):
        sql = 'SELECT * FROM RECORD WHERE TNO = :id'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'id': tno}))

    def get_amount(tno, cmid):
        sql = 'SELECT AMOUNT FROM RECORD WHERE TNO = :id and CMID=:cmid'
        return DB.fetchone( DB.execute_input( DB.prepare(sql) , {'id': tno, 'cmid':cmid}) )[0]
    
    def update_camera(input):
        sql = 'UPDATE RECORD SET AMOUNT=:amount, TOTAL=:total WHERE CMID=:cmid and TNO=:tno'
        DB.execute_input(DB.prepare(sql), input)

    def delete_check(cmid):
        sql = 'SELECT * FROM RECORD WHERE CMID=:cmid'
        return DB.fetchone(DB.execute_input( DB.prepare(sql), {'cmid':cmid}))

    def get_total(tno):
        sql = 'SELECT SUM(TOTAL) FROM RECORD WHERE TNO = :id'
        return DB.fetchall(DB.execute_input( DB.prepare(sql), {'id':tno}))[0]

class Order_List():
    def add_order(input):
        sql = 'INSERT INTO ORDER_C VALUES (null, :mid, TO_DATE(:time, :format ), :total, :tno)'
        DB.execute_input(DB.prepare(sql), input)
        DB.commit()

    def get_order():
        sql = 'SELECT OID, MNAME, PRICE, ORDERTIME FROM ORDER_C NATURAL JOIN MEMBER ORDER BY ORDERTIME DESC'
        return DB.fetchall(DB.execute(DB.connect(), sql))
    
    def get_orderdetail():
        sql = 'SELECT O.OID, C.CMNAME, R.SALEPRICE, R.AMOUNT FROM ORDER_C O, RECORD R, CAMERA C WHERE O.TNO = R.TNO AND R.CMID = C.CMID GROUP BY O.MID, O.ORDERTIME, C.CMNAME, R.SALEPRICE, R.AMOUNT, O.OID ORDER BY O.ORDERTIME DESC'
        return DB.fetchall(DB.execute(DB.connect(), sql))


# 暫定
class Analysis():
    def month_price(i):
        sql = 'SELECT EXTRACT(MONTH FROM ORDERTIME), SUM(PRICE) FROM ORDER_C WHERE EXTRACT(MONTH FROM ORDERTIME)=:mon GROUP BY EXTRACT(MONTH FROM ORDERTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql) , {"mon": i}))

    def month_count(i):
        sql = 'SELECT EXTRACT(MONTH FROM ORDERTIME), COUNT(OID) FROM ORDER_C WHERE EXTRACT(MONTH FROM ORDERTIME)=:mon GROUP BY EXTRACT(MONTH FROM ORDERTIME)'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {"mon": i}))
    
    def category_sale():
        sql = 'SELECT SUM(TOTAL), CMBRAND FROM(SELECT * FROM CAMERA,RECORD WHERE CAMERA.CMID = RECORD.CMID) GROUP BY CMBRAND'
        return DB.fetchall( DB.execute( DB.connect(), sql))

    def member_sale():
        sql = 'SELECT SUM(PRICE), MEMBER.MID, MEMBER.MNAME FROM ORDER_C, MEMBER WHERE ORDER_C.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity GROUP BY MEMBER.MID, MEMBER.MNAME ORDER BY SUM(PRICE) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'user'}))

    def member_sale_count():
        sql = 'SELECT COUNT(*), MEMBER.MID, MEMBER.MNAME FROM ORDER_C, MEMBER WHERE ORDER_C.MID = MEMBER.MID AND MEMBER.IDENTITY = :identity GROUP BY MEMBER.MID, MEMBER.MNAME ORDER BY COUNT(*) DESC'
        return DB.fetchall( DB.execute_input( DB.prepare(sql), {'identity':'user'}))