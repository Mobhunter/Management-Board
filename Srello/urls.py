from django.conf.urls import url
from django.contrib import admin
from main_site.views import *
from django.urls import path
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', log_in),
    path('register/', register),
    path('', homepage),
    path('board/<int:year>/', board),
    path('create_card/<int:task_id>/', create_card),
    path('create_task/<board_id>', create_task),
    path('create_board/', create_board),
    path('remove_board/<int:id>/', remove_board),
    path('remove_task/<int:id>/', remove_task),
    path('remove_card/<int:id>/', remove_card),
    path('error/', error),
    path('logout/', logout),
]
