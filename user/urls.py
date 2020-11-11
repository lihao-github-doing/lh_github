from django.urls import path
from user import views

app_name='user'
urlpatterns = [
    path('register_logic/', views.register_logic, name='register_logic'),
    path('register/', views.register, name='register'),
    path('login_logic/', views.login_logic, name='login_logic'),
    path('login/', views.login, name='login'),
    path('userss/', views.userss, name='userss'),
    path('get_captcha/', views.get_captcha, name='get_captcha'),
    path('active/', views.active, name='active'),
    path('register_emali/', views.register_emali, name='register_emali'),
    path('logout/',views.logout,name='logout'),
]