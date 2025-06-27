from django.db import models

class Battery_capacity(models.Model):
    name_bc = models.CharField('Название', max_length=50)
    def __str__(self):
        return self.name_bc


class Power(models.Model):
    name_p = models.CharField('Название', max_length=50)
    def __str__(self):
        return self.name_p


class Biks(models.Model):
    id_pover = models.IntegerField('ID_p')
    id_bc = models.IntegerField('ID_bc')
    name_bike = models.CharField('Название', max_length=50)
    description_bike = models.TextField('Описание')
    photo = models.CharField('Каринка', max_length=250)
    price = models.IntegerField('Цена')
    def __str__(self):
        return self.name_bike

class Basket(models.Model):
    id_basket = models.CharField('COOKIE_ID_basket', max_length=25)
    id_bike = models.IntegerField('ID_bike')
    kolvo = models.IntegerField('Количество')
    def __str__(self):
        return self.id_basket

class Customer(models.Model):
    familiya = models.CharField('Фамилия', max_length=50)
    imya = models.CharField('Имя', max_length=50)
    adres = models.TextField('Адрес')
    login_cust = models.CharField('Логин', max_length=50)
    parol = models.CharField('Пароль', max_length=50)
    mail = models.CharField('Почта', max_length=50)
    phone = models.CharField('Номер телефона', max_length=12)
    podpiska = models.IntegerField('Подписка')

class Order(models.Model):
    id_order=models.CharField('Номер заказа', max_length=25)
    date_order = models.DateField('Дата заказа')
    id_cust = models.IntegerField('IDПокупателя', max_length=50)
    discount= models.IntegerField('ВариантДоставки')

class OrderList(models.Model):
    id_order=models.CharField('Номер заказа', max_length=25)
    id_bike = models.IntegerField('IDБайка', max_length=50)
    kolvo = models.IntegerField('Количество')

