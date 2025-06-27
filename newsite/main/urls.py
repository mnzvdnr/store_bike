from django.urls import path
from . import views

urlpatterns = [
    path('set',  views.set),
    path('delete_co',  views.delete_co),
    path('index', views.index, name='home'),
    path('', views.set),
    path('katalog', views.katalog, name='katalog'),
    path('basket', views.basket, name='basket'),
    path('dobasket', views.dobasket, name='dobasket'),
    path('auto', views.auto, name='auto'),
    path("postuser/", views.postuser),
    path('kabinet', views.kabinet, name='kabinet'),
    path("change/", views.change),
    path("exit", views.exit, name='exit'),
    path("order", views.order, name='order'),
    path("doorder/", views.doorder, name='doorder'),
    path("doauto/", views.doauto, name='doauto'),
    path("reg/", views.reg, name='reg'),
    path("doreg/", views.doreg),

]