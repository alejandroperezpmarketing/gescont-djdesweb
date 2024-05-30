'''
Created on 21 mar. 2024

@author: vagrant
'''
from django.urls import path
from appdesweb import views, viewsUsers

urlpatterns = [
    path('not_logged_in/',viewsUsers.notLoggedIn),
    path('app_login/',viewsUsers.AppLogin.as_view()),
    path('app_logout/',viewsUsers.AppLogout.as_view()),
    
    path('hello_world/',views.HelloWord.as_view()),
    path('hola_clase/',views.HolaClase.as_view()),
    path('building_select_by_gid/',views.BuildingSelectByGid.as_view()),
    path('building_select_by_gid2/<date>/',views.BuildingSelectByGid2.as_view()),
    path('building_select_by_area/',views.BuildingSelectByArea.as_view()),
    path('building_insert/',views.BuildingInsert.as_view()),
    path('building_update/',views.BuildingUpdate.as_view()),
    path('building_delete/',views.BuildingDelete.as_view()),
    path('building/',views.Building.as_view()),
    #Stores
    path('insert_store/',views.InsertStore.as_view()),
    path('select_store_by_gid/',views.SelectStoreByGid.as_view()),
    path('delete_store_by_gid/',views.DeleteStoreByGid.as_view()),
    path('update_store/',views.UpdateStoreInformation.as_view()),
    #Streets
    path('insert_streets/',views.InsertStreets.as_view()),
    path('delete_street_by_gid/',views.DeleteStreetByGid.as_view()),
    #Clients
    path('delete_client_by_gid/',views.DeleteClientByGid.as_view()),
    path('inser_client/',views.InsertClient.as_view()),
    path('select_client_by_gid/',views.InsertClient.as_view()),

    path('h/',views.HelloWord.as_view()),

]
