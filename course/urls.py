from django.urls import path
from course import views

app_name = 'course'

urlpatterns = [
    path('index/',views.index,name='index'),
    path('base/',views.base,name='base'),
    path('delete/', views.delete, name='delete'),
    path('get_category/', views.get_category, name='get_category'),
    path('add_course/',views.add_course,name='add_course'),
    path('add_course_logic/',views.add_course_logic,name='add_course_logic'),
    path('add_article/',views.add_article,name='add_article'),
    path('add_article_logic/',views.add_article_logic,name='add_article_logic'),
    path('update/',views.update,name='update'),
    path('update_logic',views.update_logic,name='update_logic'),
]
