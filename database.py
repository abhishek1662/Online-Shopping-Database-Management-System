import streamlit as st
import mysql.connector
import pandas as pd

db = mysql.connector.connect(
    host='localhost',
    user='root',
    database='Online_Shopping'
)

c = db.cursor(buffered=True)
c.execute('CREATE DATABASE IF NOT EXISTS Online_Shopping')


# -----------------------------------------------------------------BUYER---------------------------------------------------------------------------
def create_cus():
    c.execute('CREATE TABLE IF NOT EXISTS customer(CId int AUTO_INCREMENT primary key,cName text,cPass text,cPhone varchar(10),cAdd text,DOB date,age varchar(3));')


def add_cus(name, password, phone, address, dob):
    c.execute('INSERT INTO customer(cName,cPass,cPhone,cAdd,DOB) values(%s,%s,%s,%s,%s)',
              (name, password, phone, address, dob))
    db.commit()


def login_cus(username, password):
    c.execute('SELECT * FROM customer where cName=%s and cPass=%s',
              (username, password))
    data = c.fetchall()
    return data


def view_cus(username, password):
    c.execute('SELECT * FROM customer WHERE cName=%s and cPass=%s',
              (username, password))
    data = c.fetchall()
    return data
# -----------------------------------------------------------------BUYER---------------------------------------------------------------------------


# -----------------------------------------------------------------SELLER--------------------------------------------------------------------------
def create_seller():
    c.execute(
        'CREATE TABLE IF NOT EXISTS seller(SId int AUTO_INCREMENT primary key,sName text,sPass text,sPhone varchar(10),sAdd text);')


def add_seller(name, password, phone, address):
    c.execute('INSERT INTO seller(sName,sPass,sPhone,sAdd) values(%s,%s,%s,%s)',
              (name, password, phone, address))
    db.commit()


def login_seller(username, password):
    c.execute('SELECT * FROM seller where sName=%s and sPass=%s',
              (username, password))
    data = c.fetchall()
    return data


def view_seller(username, password):
    c.execute('SELECT * FROM seller where sName=%s and sPass=%s',
              (username, password))
    data = c.fetchall()
    return data
# -----------------------------------------------------------------SELLER--------------------------------------------------------------------------


# -----------------------------------------------------------------CUS_PRO-------------------------------------------------------------------------
def view_pro():
    c.execute('SELECT PId,pName,cost,type,details,availability FROM product')
    data = c.fetchall()
    return data


def show_pro(pro_id):
    c.execute('SELECT * FROM product WHERE product.PId="{}"'.format(pro_id))
    data = c.fetchall()
    return data


def create_cart():
    c.execute('CREATE TABLE IF NOT EXISTS cart(cartId int primary key AUTO_INCREMENT,PId int,name text,quantity int,amount int,totalCost int,CId int,foreign key(PId) references product(PId) ON UPDATE CASCADE ON DELETE CASCADE,foreign key(CId) references customer(CId) ON UPDATE CASCADE ON DELETE CASCADE);')


def add_cart(pro_id, name, quantity, price, totalCost, cus_id):
    c.execute('INSERT INTO cart(PId,name,quantity,amount,totalCost,CId) values(%s,%s,%s,%s,%s,%s)',
              (pro_id, name, quantity, price, totalCost, cus_id))
    db.commit()


def view_cart(cus_id):
    c.execute(
        'SELECT cartId,PId,name,quantity,amount,totalCost FROM cart where cart.CId="{}"'.format(cus_id))
    data = c.fetchall()
    return data
# -----------------------------------------------------------------CUS_PRO-------------------------------------------------------------------------


# -----------------------------------------------------------------PRODUCT-------------------------------------------------------------------------
def create_pro():
    c.execute('CREATE TABLE IF NOT EXISTS product(PId int AUTO_INCREMENT primary key,pName text,cost int,type text,details text,availability int,SId int,FOREIGN KEY (SId) REFERENCES seller(SId) ON UPDATE CASCADE ON DELETE CASCADE);')


def add_pro(name, cost, type, details, availability, id):
    c.execute('INSERT INTO product(pName,cost,type,details,availability,SId) values(%s,%s,%s,%s,%s,%s)',
              (name, cost, type, details, availability, id))
    db.commit()


def view_pro1(seller_id):
    c.execute(
        'SELECT SId,PId,pName,cost,type,details,availability FROM product where product.SId="{}"'.format(seller_id))
    data = c.fetchall()
    return data


def delete_pro1(pro_id):
    c.execute('DELETE FROM product where PId="{}"'.format(pro_id))
    db.commit()

# ----------------------------------------FUNCTION CALL---------------------------------------


def getNumberofProducts(sel_id):
    c.execute('SELECT getNumberOfProducts({})'.format(sel_id))
    data = c.fetchall()
    return data
# ----------------------------------------FUNCTION CALL-----------------------------------------


# --------------------------------------MODIFICATION----------------------------------------
def maxSeller():
    c.execute('SELECT max_pro_by_cus()')
    data = c.fetchall()
    return data
# --------------------------------------MODIFICATION----------------------------------------


def view_PId():
    c.execute('SELECT PId FROM product')
    data = c.fetchall()
    return data


def view_pro2(id):
    c.execute(
        'SELECT pName,cost,type,details,availability FROM product where PId="{}"'.format(id))
    data = c.fetchall()
    return data


def update_pro(new_name, new_price, new_type, new_detail, avail, seller_id, pro_id):
    c.execute('UPDATE product SET pName=%s, cost=%s, type=%s, details=%s, availability=%s where SId=%s and PId=%s',
              (new_name, new_price, new_type, new_detail, avail, seller_id, pro_id))
    db.commit()
    c.execute('SELECT pName,cost,type,details FROM product')
    data = c.fetchall()
    # st.write(data)
    return data
# -----------------------------------------------------------------PRODUCT-------------------------------------------------------------------------


# ------------------------------------------------------------------CART---------------------------------------------------------------------------
def view_par_cart(pro_id):
    c.execute(
        'SELECT PId,name,quantity,amount,totalCost FROM cart WHERE cart.PId="{}"'.format(pro_id))
    data = c.fetchall()
    return data


def update_cart(new_quantity, new_cost, cart_id):
    c.execute('UPDATE cart SET quantity=%s, totalCost=%s where cartId=%s',
              (new_quantity, new_cost, cart_id))
    db.commit()
    # st.write(new_cost)
    # st.write(new_quantity)
    c.execute('SELECT PId,name,quantity,amount,totalCost from cart')
    data = c.fetchall()
    # st.write(data)
    return data


def delete_pro(pro_id):
    c.execute('DELETE FROM cart where cart.PId="{}"'.format(pro_id))
    db.commit()


def delete_cart(cus_id):
    c.execute('call backup_cart({})'.format(cus_id))
    c.execute('DELETE FROM cart where cart.CId="{}"'.format(cus_id))
    db.commit()
# ------------------------------------------------------------------CART---------------------------------------------------------------------------


# -----------------------------------------------------------------PAYMENT-------------------------------------------------------------------------
def create_pay():
    c.execute('CREATE TABLE IF NOT EXISTS PAYMENT(PayId int primary key AUTO_INCREMENT,paydate text,bank text,total int,CId int, foreign key(CId) references customer(CId))')


def add_pay(date, bank, total, cus_id):
    c.execute('INSERT INTO payment(paydate,bank,total,CId) values (%s,%s,%s,%s)',
              (date, bank, total, cus_id))
    db.commit()


def join(cus_id, pay_id):
    c.execute('SELECT cart.cartId,cart.name,cart.quantity,cart.amount,cart.totalCost,payment.PayId,payment.paydate FROM cart INNER JOIN payment on cart.CId = %s and payment.PayId=%s', (cus_id, pay_id))
    data = c.fetchall()
    return data


def display(cus_id):
    c.execute(
        'select sum(totalCost) as Total from cart where CId="{}"'.format(cus_id))
    data = c.fetchall()
    # st.write(data)
    return data


def view_pay(cus_id, pay_id):
    c.execute(
        'SELECT PayId,paydate,bank,total FROM payment WHERE CId=%s and PayId=%s', (cus_id, pay_id))
    data = c.fetchall()
    return data


def check_cart():
    c.execute('SELECT * from cart')
    data = c.fetchall()
    return data


def cart_pro():
    c.execute('SELECT product.PId,product.pName,product.availability,cart.quantity FROM cart INNER JOIN product where product.PId=cart.PId')
    data = c.fetchall()
    return data


def update_after_buy(avail, pro_id):
    c.execute(
        'UPDATE product SET availability=%s where PId=%s', (avail, pro_id))
    db.commit()


def payId(cus_id):
    c.execute('SELECT PayId from payment where CId="{}"'.format(cus_id))
    data = c.fetchall()
    return data


def backup_cart(cus_id):
    c.execute('SELECT cartId,PId,name,quantity,amount,totalCost FROM backup_cart_table where backup_cart_table.CId="{}"'.format(cus_id))
    data = c.fetchall()
    return data
# -----------------------------------------------------------------PAYMENT-------------------------------------------------------------------------
