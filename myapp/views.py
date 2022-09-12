import http
from django.shortcuts import render
from django.http import HttpResponse 
from django.shortcuts import redirect
from .forms import *
import re
import pymysql

# Create your views here.
def cover(requests):
    return render(requests,'cover.html',locals())

def commonDataForTemplate(requests):
    account=requests.session['account']
    return {account}

def strCheckspecialsymbol(string):
    ptn="\W"
    if re.search(ptn,string):
        return True
    else:
        return False

def strChecknumber(string):
    ptn="\D"
    if re.search(ptn,string):
        return True
    else:
        return False

def strChecklen(string,minimum,maximum):
    if len(string)<minimum or len(string)>maximum:
        return [False]
    else:
        return [True]

def customer(requests):
    if requests.method=='GET':
        return render(requests,'customer.html')
    else:
        account=requests.POST.get('account')
        password=requests.POST.get('password')
        db=pymysql.connect(host='127.0.0.1',user='user',password='ghfdjk8743',database='project.1')
        cursor=db.cursor()
        sql="select account,password from customer where account='{}'".format(account) 
        cursor.execute(sql)
        data=cursor.fetchone()
        create="CREATE TABLE {account}(id int(10) NOT NULL AUTO_INCREMENT PRIMARY KEY,dish char(50),price int(4),number int(4),total int(5));".format(account=account)
        cursor.execute(create)
        db.commit()
        db.close()
        if data==None:
            return HttpResponse('帳號不存在')
        elif data[1]!=password:
            return HttpResponse("密碼不正確")
        else:
            requests.session['account']=account
            return redirect("/order/")

def logout(requests):
    account=commonDataForTemplate(requests)
    account=str(account)
    account=account.strip('{')
    account=account.strip('}')
    account=account.strip("'")    
    db=pymysql.connect(host='127.0.0.1',user='user',password='ghfdjk8743',database='project.1')
    cursor=db.cursor()
    drop="DROP TABLE {account};".format(account=account)
    cursor.execute(drop)
    db.commit()
    db.close()
    return render(requests,'customer.html')

def customerupdate(requests):
    if requests.method=='GET':
        userdata=customerupdateform()
        return render(requests,'customerupdate.html',{'userdata':userdata})
    elif requests.method=='POST':
        account=requests.POST.get('account')
        password=requests.POST.get('password')
        errMsg=[]
        if strCheckspecialsymbol(account):
            return HttpResponse('帳號不能有特殊符號')
        checklen=strChecklen(account,5,10)
        if not checklen[0]:
            return HttpResponse('長度問題')
        if len(errMsg)!=0:
            initial_dict = {
            "account" : account,"password" : password   }
            userdata = customerupdateform(initial = initial_dict)
            return render(requests,"customerupdate.html",{'userdata':userdata,'errMsg':errMsg})

        db=pymysql.connect(host='127.0.0.1',user='user',password='ghfdjk8743',database='project.1')
        cursor=db.cursor()
        sql="select * from customer where account='{}'".format(account)
        cursor.execute(sql)
        db.commit()
        if cursor.fetchone():
            return HttpResponse("帳號已存在，請另改帳號")
        sql="insert into customer (account,password)values('{}','{}')".format(account,password)
        cursor.execute(sql)
        db.commit() 
        return redirect("/customer/")
def dishupdate(requests):
    if requests.method=='GET':
        dishupdate=dishupdateform()
        return render(requests,'dishupdate.html',{'dishupdate':dishupdate})
    elif requests.method=='POST':
        dish=requests.POST.get('dish')
        price=requests.POST.get('price')
        errMsg=[]
        if strCheckspecialsymbol(dish):
            return HttpResponse('帳號不能有特殊符號')
        if strChecknumber(price):
            return HttpResponse('不能有特殊符號')
        checklen=strChecklen(price,0,4)
        if not checklen[0]:
            return HttpResponse('長度問題')
        if len(errMsg)!=0:
            initial_dict = {
            "dish" : dish,"price" : price   }
            dishupdate = dishupdateform(initial = initial_dict)
            return render(requests,"dishupdate.html",{'dishupdate':dishupdate,'errMsg':errMsg})

        db=pymysql.connect(host='127.0.0.1',user='user',password='ghfdjk8743',database='project.1')
        cursor=db.cursor()
        sql="select * from orders where dish='{}'".format(dish)
        cursor.execute(sql)
        db.commit()
        if cursor.fetchone():
            return HttpResponse("商品已存在")
        sql="insert into orders (dish,price)values('{}','{}')".format(dish,price)
        cursor.execute(sql)
        db.commit()    
        return redirect("/dishupdate/")

def order(requests):
    db=pymysql.connect(host='127.0.0.1',user='user',password='ghfdjk8743',database='project.1')
    cursor=db.cursor()
    sql="select * from orders"
    cursor.execute(sql)
    db.commit()
    data=cursor.fetchall()
    db.close()
    dish=[]
    for i in range(len(data)):
            dish.append(data[i])
    account=commonDataForTemplate(requests)
    return render(requests,'order.html',{'dish':dish,'account':account})

def appendcart(requests):
    if requests.method=='GET':
        dish=requests.GET.get('dish')
        price=requests.GET.get('price')
        number=requests.GET.get('number')
        account=commonDataForTemplate(requests)
        account=str(account)
        account=account.strip('{')
        account=account.strip('}')
        account=account.strip("'")
        price=int(price)
        number=int(number)
        total=number*price
        db=pymysql.connect(host='127.0.0.1',user='user',password='ghfdjk8743',database='project.1')
        cursor=db.cursor()
        sql="insert into {} (dish,price,number,total)values('{}','{}','{}','{}')".format(account,dish,price,number,total)
        cursor.execute(sql)
        db.commit()    
    return redirect("/order/")

def delete(requests):
    id=requests.GET.get('id')
    account=commonDataForTemplate(requests)
    account=str(account)
    account=account.strip('{')
    account=account.strip('}')
    account=account.strip("'")
    db=pymysql.connect(host='127.0.0.1',user='user',password='ghfdjk8743',database='project.1')
    cursor=db.cursor()
    list="delete from {} where id='{}'".format(account,id)
    cursor.execute(list)
    db.commit()
    db.close()
    return redirect("/cart/")

def cart(requests):
    if requests.method=='GET':
        account=commonDataForTemplate(requests)
        account=str(account)
        account=account.strip('{')
        account=account.strip('}')
        account=account.strip("'")
        db=pymysql.connect(host='127.0.0.1',user='user',password='ghfdjk8743',database='project.1')
        cursor=db.cursor()
        list="select * from {}".format(account)
        cursor.execute(list)
        db.commit()
        list=cursor.fetchall()
        db.close()
        totallist=[]
        for i in range(len(list)):
            totallist.append(list[i])
        return render(requests,'cart.html',{'account':account,'totallist':totallist})

def submit(requests):
    account=commonDataForTemplate(requests)
    account=str(account)
    account=account.strip('{')
    account=account.strip('}')
    account=account.strip("'")
    # id=requests.GET.get('id')
    # dish=requests.GET.get('dish')
    # price=requests.GET.get('price')
    # number=requests.GET.get('number')
    # total=requests.GET.get('total')
    db=pymysql.connect(host='127.0.0.1',user='user',password='ghfdjk8743',database='project.1')
    cursor=db.cursor()
    list="select id,dish,price,number,total from {}".format(account)
    cursor.execute(list)
    db.commit()
    list=cursor.fetchall()
    # return HttpResponse(list[0][0])
    for i in list:
        
        sql="insert into orderlist (account,dish,price,number,total)values('{}','{}','{}','{}','{}')".format(account,i[1],i[2],i[3],i[4])
        cursor.execute(sql)
        db.commit()
    db.close()    
    return render(requests,'cover.html',{'account':account})

def orderlist(requests):
    db=pymysql.connect(host='127.0.0.1',user='user',password='ghfdjk8743',database='project.1')
    cursor=db.cursor()
    sql="select * from orderlist"
    cursor.execute(sql)
    db.commit()
    data=cursor.fetchall()
    db.close()
    orderlist=[]
    for i in range(len(data)):
            orderlist.append(data[i])
    return render(requests,'orderlist.html',{'orderlist':orderlist})

def complete(requests):
    id=requests.GET.get('id')
    db=pymysql.connect(host='127.0.0.1',user='user',password='ghfdjk8743',database='project.1')
    cursor=db.cursor()
    sql="DELETE FROM orderlist where id='{}'".format(id)
    cursor.execute(sql)
    db.commit()
    db.close()
    return redirect("/orderlist/")
    