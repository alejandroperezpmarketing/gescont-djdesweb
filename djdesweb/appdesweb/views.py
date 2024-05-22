import json
#Django imports
from django.http import JsonResponse
#from django.http import HttpResponse
from django.views import View

from django.contrib.auth.mixins import LoginRequiredMixin
from .pycode import buildingsPOO, connPOO

#from django.contrib.auth import logout
#from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin
#from django.views.decorators.csrf import csrf_exempt
#from django.utils.decorators import method_decorator


class HelloWord(View):
    def get(self, request):
        return JsonResponse({"ok":"true","message": "Hello world", "data":[]})


class HolaClase(View):
    def get(self, request):
        area=request.GET['area']
        return JsonResponse({"ok":"true","message": "Hola clase", "data":[{'area':area}]})


class BuildingSelectByGid(View):
    def get(self, request):
        gid=request.GET['gid']
        conn=connPOO.Conn()
        b=buildingsPOO.Buildings(conn)
        r=b.selectAsDict(gid)
        return JsonResponse(r)
    
class BuildingSelectByGid2(View):
    def get(self, request,gid):
        #gid=request.GET['gid']
        conn=connPOO.Conn()
        b=buildingsPOO.Buildings(conn)
        r=b.selectAsDict(gid)
        return JsonResponse(r)

class BuildingSelectByArea(View):
    def get(self, request):
        area=request.GET['area']
        conn=connPOO.Conn()
        b=buildingsPOO.Buildings(conn)
        r=b.selectAsDictByArea(area=area)
        return JsonResponse(r)
    
class BuildingInsert(LoginRequiredMixin, View):
    def post(self, request):
        descripcion=request.POST['descripcion']
        geomWkt=request.POST['geomWkt']
        print(descripcion,geomWkt)
        conn=connPOO.Conn()
        b=buildingsPOO.Buildings(conn)
        r=b.insert(descripcion, geomWkt)
        return JsonResponse(r)
    
class BuildingUpdate(View):
    def post(self, request):
        gid=request.POST['gid']
        descripcion=request.POST['descripcion']
        geomWkt=request.POST['geomWkt']
        print(gid,descripcion,geomWkt)
        conn=connPOO.Conn()
        b=buildingsPOO.Buildings(conn)
        r=b.update(gid, descripcion, geomWkt)
        return JsonResponse(r)

class BuildingDelete(View):
    def post(self, request):
        gid=request.POST['gid']
        print(gid)
        conn=connPOO.Conn()
        b=buildingsPOO.Buildings(conn)
        r=b.delete(gid)
        return JsonResponse(r)
    def delete(self, request):
        gid=request.POST['gid']
        print(gid)
        conn=connPOO.Conn()
        b=buildingsPOO.Buildings(conn)
        r=b.delete(gid)
        return JsonResponse(r)


class Building(View):
    def post(self, request):
        return JsonResponse({'mens':'Metodo post para insertar'})

    def put(self, request):
        return JsonResponse({'mens':'Metodo put para update'})
    
    def delete(self, request):
        return JsonResponse({'mens':'Metodo delete para borrar'})

    def get(self, request):
        return JsonResponse({'mens':'Metodo get para seleccionar'})


    

#    def get(self, request):
#        return JsonResponse({'message':'soy el método get'})


####################################################################################

###Alejandro Functions


class ClientInsert(LoginRequiredMixin, View):
    def post(self, request):


        #get the form data
        d=general.getPostFormData(request)
        name=d['name']
        last_name=d['last_name']
        age=d['age']
        sex=d['sex']
        purchase_date=d['purchase_date']
        client_motivation=d['client_motivation']
        channel_id=d['channel_id']
        geomWkt=d['geomWkt']
        print(name,last_name,age,sex,purchase_date,client_motivation,channel_id,geomWkt)

        conn=connPOO.Conn()
        b=buildingsPOO.Clients(conn)
        r=b.insert_client(name,last_name,age,sex,purchase_date,client_motivation,channel_id,geomWkt)
        return JsonResponse(r)


        # ....

        # last_name=request.POST['last_name']
        # age=request.POST['age']
        # sex=request.POST['sex']
        # purchase_date=request.POST['purchase_date']
        # client_motivation=request.POST['client_motivation']
        # channel_id=request.POST['channel_id']
        # geomWkt=request.POST['geomWkt']
        # print(name,last_name,age,sex,purchase_date,client_motivation,channel_id,geomWkt)
        # conn=connPOO.Conn()
        # b=buildingsPOO.Clients(conn)
        # r=b.insert_client(name,last_name,age,sex, purchase_date,client_motivation,channel_id,geomWkt)
        # return JsonResponse(r)
