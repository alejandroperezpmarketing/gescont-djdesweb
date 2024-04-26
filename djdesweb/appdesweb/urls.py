'''
Created on 21 mar. 2024

@author: vagrant
'''
from django.urls import path
from appdesweb import views

urlpatterns = [
    path('hello_world/',views.HelloWord.as_view()),
    path('hola_clase/',views.HolaClase.as_view()),
    path('building_select_by_gid/',views.BuildingSelectByGid.as_view()),
    path('building_select_by_gid2/<date>/',views.BuildingSelectByGid2.as_view()),
    path('building_select_by_area/',views.BuildingSelectByArea.as_view()),
    path('building_insert/',views.BuildingInsert.as_view()),
    path('building_update/',views.BuildingUpdate.as_view()),
    path('building_delete/',views.BuildingDelete.as_view()),
    path('building/',views.Building.as_view()),
    path('h/',views.HelloWord.as_view()),

]
