from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('login/', user_login, name="login" ),
    path('', user_register, name="register" ),
    path('home/', home, name="home" ),
    path('send_interest/<int:recipient_id>/', send_interest, name='send_interest'),
    path('received_interests/', received_interests, name='received_interests'),
    path('accept_interest/<int:interest_id>/', accept_interest, name='accept_interest'),
    path('reject_interest/<int:interest_id>/', reject_interest, name='reject_interest'),
    path('chat/<int:recipient_id>/', chat, name='chat'),
    path('logout/', user_logout, name='logout'),

]
