from django.urls import path, include
from main_app import views

app_name = 'main_app'

urlpatterns= [
    path('register/',views.register,name='register'),
    path('user_login.',views.user_login,name='user_login'),
    path('search/',views.search,name='search'),
    path('save_launch/', views.save_launch, name='save_launch'),
    path('remove_launch/',views.remove_launch,name='remove_launch'),
    path('saved_launches/',views.saved_launches,name='saved_launches')
]