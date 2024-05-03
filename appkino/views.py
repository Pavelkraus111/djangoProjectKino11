from django.shortcuts import render, redirect
from .models import *
import random

# Create your views here.
def index(req):
    film = modelKino.objects.all()
    actor = modelActor.objects.all()
    randomFilm = random.choice(film)
    data = {'film':film, 'actor':actor,'random':randomFilm}
    return render(req,'index.html',data)

from django.views import generic
class kinoList(generic.ListView):
    model = modelKino


class kinoDetail(generic.DetailView):
    model = modelKino


class actorList(generic.ListView):
    model = modelActor
    paginate_by = 3

class actorDetail(generic.DetailView):
    model = modelActor


class directorList(generic.ListView):
    model = modelDirector
    paginate_by = 5

class directorDetail(generic.DetailView):
    model = modelDirector

from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

def registr(req):
    # forma = UserCreationForm()
    print(1)
    if req.POST:
        print(2)
        forma = formRegistr(req.POST)#Форма регистрации проверка
        if forma.is_valid():#проверка пройдена
            print(3)
            #Собираем данные
            k1 = forma.cleaned_data.get('username')
            k2 = forma.cleaned_data.get('password1')
            k3 = forma.cleaned_data.get('email')
            k4 = forma.cleaned_data.get('first_name')
            k5 = forma.cleaned_data.get('last_name')
            User.objects.create_user(username=k1,password=k2)#новая строка в таблице
            user = User.objects.get(username=k1)#находим пользователя
            #заполняем данные
            user.email = k3
            user.last_name = k5
            user.first_name = k4
            user.save()#сохраняем
            modelProfile.objects.create(balance=1000,podpiska_id=1,user_id=user.id)
            login(req,user)#Вход пользователя на сайт
            return redirect('home')#на главную стр. перемещаемся
    else:
        forma = formRegistr()#форма регистрации
    data = {'form':forma}
    return render(req,'registration/registration.html',data)
def profile(req):


    return render(req,'kabinet.html')
###############################################################
# def profileChange(req):
#     forma = formPodpiska
#     data = {'form':forma}
#     if req.POST:
#         k1 = req.POST.get('item')
#         user = User.objects.get(id= req.user.id)
#         user.modelprofile.podpiska_id = k1
#         user.modelprofile.save()
#         return redirect('kabinet')
#     return render(req,'kabinet.html',data)
def profileChange(req):
    forma = formPodpiska
    data = {'form':forma}
    if req.POST:
        k1 = req.POST.get('item')
        user = User.objects.get(id= req.user.id)
        user.modelprofile.podpiska_id = k1
        user.modelprofile.save()
        # Получаем стоимость выбранной подписки
        podpiska_cost = get_podpiska_cost(int(k1))

        # Вычитаем стоимость подписки из баланса пользователя
        current_balance = user.modelprofile.balance
        new_balance = current_balance - podpiska_cost
        user.modelprofile.balance = new_balance
        user.modelprofile.save()

        return redirect('kabinet')
    return render(req,'kabinet.html',data)
def get_podpiska_cost(podpiska_id):
    cost = {
        1: 0,
        2: 300,
        3: 1000,
        #  варианты подписки и их стоимость
    }[podpiska_id]
    return cost


#################################################################
def otziv(req, kinoid):
    print(1)
    if req.POST:#Загружается форма отзыва

        k1 = req.POST.get('text')
        k2 = req.user.id #Кто написал отзыв
        k3 = req.user.username
        print(k1,k2,k3)
        film = modelKino.objects.get(id=kinoid) #Находим фильм на который отзыв написал
        modelOtziv.objects.create(text=k1, user_id=k2, film_id=kinoid)#Записывает отзыв в таблицу БД
        
        return redirect('onekino', film.genre, film.id)#Обновляем ту же страницу
    return redirect('home')
