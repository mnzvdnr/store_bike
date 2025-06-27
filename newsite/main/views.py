import sqlite3
from django.shortcuts import render
from django.http import HttpResponse
from .models import Battery_capacity
from .models import Power
from .models import Biks
from .models import Basket
from .models import Customer
from .models import Order
from .models import OrderList
from django.db import models
import secrets
import string
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.contrib.sessions.backends.db import SessionStore
from datetime import date

def set(reqest):
    response = render(reqest, 'index.html')
    if 'cookie_basket' not in reqest.COOKIES:
        letters_and_digits = string.ascii_letters + string.digits
        key = ''.join(secrets.choice(letters_and_digits) for i in range(25))
        response.set_cookie('cookie_basket', key)
    return response

def delete_co(reqest):
    if reqest.COOKIES.get('cookie_basket'):
        response = HttpResponse(f"by")
        response.delete_cookie('cookie_basket')
    else:
        response = HttpResponse(f"их нет")
    return response

def index(reqest):
    return render(reqest, 'index.html')


def katalog(reqest):
    id_pover = reqest.GET.get("id_power")
    id_bc = reqest.GET.get("id_bc")
    type = reqest.GET.get("type")
    if type == "1":
        bc = Battery_capacity.objects.all()
        p = Power.objects.all()
        bike = Biks.objects.filter(id_pover=id_pover)
        data = {
            'bc': bc,
            'p': p,
            'bike': bike
        }
        return render(reqest, 'katalog.html', {'filter': data})
    if type == "2":
        bc = Battery_capacity.objects.all()
        p = Power.objects.all()
        bike = Biks.objects.filter(id_bc=id_bc)
        data = {
            'bc': bc,
            'p': p,
            'bike': bike
        }
        return render(reqest, 'katalog.html', {'filter': data})
    else:
        bc = Battery_capacity.objects.all()
        p = Power.objects.all()
        bike = Biks.objects.all()
        data = {
            'bc': bc,
            'p': p,
            'bike': bike
        }
        return render(reqest, 'katalog.html', {'filter': data})

def basket(reqest):
    id_basket=reqest.COOKIES.get("cookie_basket")
    baskets = Basket.objects.filter(id_basket=id_basket)
    if baskets.exists():
        count = baskets.annotate(count=models.Count('id')).values('count')[0]['count']
    else:
        count = "не найдено"
    if count == 0 or count == "не найдено":
        type = 0
        data = {
            'type': type
        }
        return render(reqest, 'basket.html', {'data': data})
    else:
        type=1
        strSQL1=Basket.objects.filter(id_basket= id_basket)
        strSQL2 = Biks.objects.none()
        for el in strSQL1:
            strSQL2 = strSQL2.union(Biks.objects.filter(id=el.id_bike))
        sum = 0
        for el2 in strSQL2:
            for el in strSQL1:
                if el2.id == el.id_bike:
                    sum = sum + el2.price * el.kolvo
        data ={
            'type': type,
            'strSQL1': strSQL1,
            'strSQL2': strSQL2,
            'sum': sum,
        }
    return render(reqest, 'basket.html', {'data': data})

def dobasket(reqest):
    id_bike = reqest.GET.get("id_bike")
    id_basket = reqest.COOKIES.get("cookie_basket")
    type = reqest.GET.get("type")

    if type == '1':
        strSQL = Basket.objects.filter(id_basket=id_basket, id_bike=id_bike)
        if strSQL.exists():
            count = strSQL.annotate(count=models.Count('id')).values('count')[0]['count']
        else:
            count = "не найдено"
        if count==0 or count == "не найдено":
            Basket.objects.create(id_bike=id_bike, id_basket=id_basket, kolvo=1)

        else:
            k= strSQL[0].kolvo
            strSQL.update(kolvo=k+1)
    elif type == '2':
        strSQL = Basket.objects.filter(id_basket=id_basket, id_bike=id_bike)
        k = strSQL[0].kolvo
        if k > 1:
            strSQL.update(kolvo=k - 1)
        else:
            strSQL.delete()
    elif type == '3':
        strSQL = Basket.objects.filter(id_basket=id_basket, id_bike=id_bike)
        strSQL.delete()

    elif type == '4':
        strSQL = Basket.objects.filter(id_basket=id_basket)
        strSQL.delete()

    # return render(reqest, 'basket.html')
    return redirect('basket')


def kabinet(reqest):
    sum=0
    session = SessionStore(session_key=reqest.session.session_key)
    if reqest.session['id'] != None:
        id_cust = reqest.session['id']
        strSQL = Customer.objects.filter(id=id_cust)
        if strSQL != None:
            strSQL1 = Order.objects.filter(id_cust=id_cust)
            strSQL2 = OrderList.objects.none()
            strSQL3 = Biks.objects.none()
            for el in strSQL1:
                strSQL2 = strSQL2.union(OrderList.objects.filter(id_order=el.id_order))
            for el in strSQL2:
                strSQL3 = strSQL3.union(Biks.objects.filter(id=el.id_bike))
            data = {
                'strSQL': strSQL[0],
                'strSQL1': strSQL1,
                'strSQL2': strSQL2,
                'strSQL3': strSQL3,
                'sum': sum,
            }
            return render(reqest, 'kabinet.html', {'data': data})
        else:
            id_cust = "Вы не авторизованы"
            return render(reqest, 'auto.html', {'message': id_cust})
    else:
        id_cust="Вы не авторизованы"
        return render(reqest, 'auto.html', {'message': id_cust})



@csrf_exempt
def change(reqest):
    id_cust = reqest.session['id']
    familiya = reqest.POST.get("familiya")
    imya = reqest.POST.get("imya")
    adres = reqest.POST.get("adres")
    mail = reqest.POST.get("mail")
    podpiska = reqest.POST.get("podpiska")
    if familiya != "" and imya != "" and adres != "" and mail != "":
        strSQL = Customer.objects.filter(id=id_cust)
        strSQL.update(familiya=familiya)
        strSQL.update(imya=imya)
        strSQL.update(adres=adres)
        if podpiska == None:
            strSQL.update(podpiska=0)
        else:
            strSQL.update(podpiska=podpiska)
        # message = "Изменение данных выполнено!"
        return redirect('kabinet')
    else:
        message = "Не все поля заполнены!"
    return render(reqest, 'kabinet.html', {'message': message})



def auto(reqest):
    session = SessionStore(session_key=reqest.session.session_key)
    if session.exists(reqest.session.session_key):
        return redirect('kabinet')
    else:
        message='вы не авторизованы'
    return render(reqest, 'auto.html', {'message': message})

@csrf_exempt
def postuser(reqest):
    if reqest.method == 'POST':
        parol = reqest.POST.get('parol')
        login_cust =reqest.POST.get("login_cust")
        type = reqest.POST.get("type")

    if type == '1':
        strSQL1 = Customer.objects.filter(login_cust=login_cust, parol=parol)
        if strSQL1.exists():
            reqest.session['id'] = strSQL1[0].id
            message = "Вы успешно авторизованы"
            # return render(reqest, 'auto.html', {'message': message})
            return redirect('kabinet')
        else:
            # message = "<tr><td><p><b>Такого логина / пароля не существует!</b></p><p>Возможно вы не <a href='reg'>ЗАРЕГЕСТРИРОВАНЫ</a></p></td></tr>";
            message="Такого логина / пароля не существует!"
            type = 0
            return render(reqest, 'auto.html', {'message': message, 'type': type})
    else:
            return render(reqest, 'auto.html')


def exit(reqest):
    reqest.session.flush()
    return redirect('home')

def order(reqest):
    id_basket= reqest.COOKIES.get("cookie_basket")
    strSQL = Basket.objects.filter(id_basket=id_basket)
    if strSQL.exists():
        count = strSQL.annotate(count=models.Count('id')).values('count')[0]['count']
    else:
        count = "не найдено"
    if count == 0 or count == "не найдено":
        message="Выша корзина пуста!"
    else:
        strSQL1 = Basket.objects.filter(id_basket=id_basket)
        strSQL2 = Biks.objects.none()
        for el in strSQL1:
            strSQL2 = strSQL2.union(Biks.objects.filter(id=el.id_bike))
        sum = 0
        for el2 in strSQL2:
            for el in strSQL1:
                if el2.id == el.id_bike:
                    sum = sum + el2.price * el.kolvo
        type=1
        data = {
            'type': type,
            'strSQL1': strSQL1,
            'strSQL2': strSQL2,
            'sum': sum,
        }
    return render(reqest, 'order.html', {'data': data})


@csrf_exempt
def doorder(reqest):
    session = SessionStore(session_key=reqest.session.session_key)
    if session.exists(reqest.session.session_key):
        id_basket = reqest.COOKIES.get("cookie_basket")
        id_cust = reqest.session['id']
        delivery = reqest.POST.get("delivery")
        strSQL = Basket.objects.filter(id_basket=id_basket)
        if strSQL.exists():
            count = strSQL.annotate(count=models.Count('id')).values('count')[0]['count']
        else:
            count = "не найдено"
        if count == 0 or count == "не найдено":
            message = "Ваша корзина пуста!!!"
            type= 0
        else:
            letters_and_digits = string.ascii_letters + string.digits
            id_order = ''.join(secrets.choice(letters_and_digits) for i in range(24))
            Order.objects.create(id_order=id_order, date_order=date.today().strftime("%Y-%m-%d"), id_cust=id_cust, discount=int(delivery))
            strSQL2 = Basket.objects.filter(id_basket=id_basket)
            for el in strSQL2:
                OrderList.objects.create(id_order=id_order, id_bike=el. id_bike, kolvo=el.kolvo)
            strSQL9 = Basket.objects.filter(id_basket=id_basket)
            strSQL9.delete()
            message = "ваш заказ отправлен"
            type=8
    else:
        message = "Вы не авторизованы!!!"
        type = 2
    return render(reqest, 'order.html', {'message': message, 'type': type})


@csrf_exempt
def reg(reqest):
    return render(reqest, 'reg.html')

@csrf_exempt
def doreg(reqest):
    if reqest.method == 'POST':
        familiya =reqest.POST.get("familiya")
        imya =reqest.POST.get("imya")
        adres =reqest.POST.get("adres")
        login_cust =reqest.POST.get("login_cust")
        parol=reqest.POST.get("parol")
        parol2 =reqest.POST.get("parol2")
        mail =reqest.POST.get("mail")
        phone =reqest.POST.get("phone")
        podpiska =reqest.POST.get("podpiska")
        phone=phone.replace("+", "")
        phone=phone.replace(" ", "")
        phone=phone.replace("(", "")
        phone=phone.replace(")", "")
        phone=phone.replace("-", "")

        if familiya != "" and imya != "" and phone != "" and mail != "" and adres != "" and login_cust != "" and parol != "" and parol2 != "":
            if parol != parol2:
                message = "Поля пароля и повтора пароля не совпадают!"
                data={
                    'message':message,
                    'familiya': familiya,
                    'imya': imya,
                    'adres':adres,
                    'login_cust': login_cust,
                    'mail': mail,
                    'phone': phone,
                    'podpiska':podpiska

                }
                return render(reqest, 'reg.html',{'data':data})
            if mail.find('@') == -1:
                 message = "E-mail указан неверно !"
                 data = {
                     'message': message,
                     'familiya': familiya,
                     'imya': imya,
                     'adres': adres,
                     'login_cust': login_cust,
                     'parol': parol,
                     'parol2': parol2,

                     'phone': phone,
                     'podpiska': podpiska

                 }
                 return render(reqest, 'reg.html', {'data': data})

            if len(phone) != 11 and phone.isdigit() == False:
                message="Номер телефона указан неверно"
                data = {
                    'message': message,
                    'familiya': familiya,
                    'imya': imya,
                    'adres': adres,
                    'login_cust': login_cust,
                    'parol': parol,
                    'parol2': parol2,
                    'mail': mail,
                    'podpiska': podpiska

                }
                return render(reqest, 'reg.html', {'data': data})
            strSQL= Customer.objects.filter(login_cust=login_cust)
            if strSQL.exists():
                message="Такой логин уже существует!"
                data = {
                    'message': message,
                    'familiya': familiya,
                    'imya': imya,
                    'adres': adres,
                    'parol': parol,
                    'parol2': parol2,
                    'mail': mail,
                    'phone': phone,
                    'podpiska': podpiska

                }
                return render(reqest, 'reg.html', {'data': data})
            if len(parol) < 6 or parol.isdigit():
                message="Пароль не удовлетворяет условиям безопасности. Пароль должен иметь более 6 символов и не должен состоятить только из цифр"
                data = {
                    'message': message,
                    'familiya': familiya,
                    'imya': imya,
                    'adres': adres,
                    'login_cust': login_cust,
                    'mail': mail,
                    'phone': phone,
                    'podpiska': podpiska

                }
                return render(reqest, 'reg.html', {'data': data})
            if podpiska != "1":
                podpiska="0"
            Customer.objects.create(familiya=familiya, imya=imya, adres=adres, mail=mail, phone=phone, login_cust=login_cust, parol=parol, podpiska=podpiska)
            message = "Вы успешно зарегестрированы!"
            strSQL2 = Customer.objects.filter(login_cust=login_cust, parol=parol)
            reqest.session['id'] = strSQL2[0].id
            return redirect('kabinet')

        else:
            message = "Не все поля заполнены!"
            data = {
                'message': message,
                'familiya': familiya,
                'imya': imya,
                'adres': adres,
                'parol': parol,
                'parol2': parol2,
                'login_cust': login_cust,
                'mail': mail,
                'phone': phone,
                'podpiska': podpiska

            }
            return render(reqest, 'reg.html', {'data': data})

@csrf_exempt
def doauto(reqest):
    return  render(reqest, 'auto.html')










