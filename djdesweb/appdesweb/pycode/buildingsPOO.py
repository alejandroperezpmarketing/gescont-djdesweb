'''
Created on 27 feb. 2024

@author: vagrant
'''
from .connPOO import Conn

"""
{'ok':true,'message':f'Edificios insertados: {n}','data': [[]]}

"""
from .geometryChecks import checkIntersection

class Buildings():
    conn:Conn
    def __init__(self,conn:Conn):
        self.conn=conn

    def insert(self,descripcion, geomWkt)->int:
        print('Iniciando')
        print(geomWkt)
        r=checkIntersection('d.buildings',geomWkt,25830)
        if r:
            return {'ok':False,'message':'El edificio intersecta con otro','data':[]}

        print('Despues del check')
        q ="insert into d.buildings (descripcion,area, geom) values (%s,st_area(st_geometryfromtext(%s,25830)),st_geometryfromtext(%s,25830)) returning gid"
        self.conn.cursor.execute(q,[descripcion,geomWkt, geomWkt])
        self.conn.conn.commit()
        gid = self.conn.cursor.fetchall()[0][0]
        return {'ok':True,'message':f'Edificio insertado. gid: {gid}','data':[[gid]]}
     
     
    def update(self,gid, descripcion, geomWkt)->int:
        q ="update d.buildings set (descripcion,area, geom) = (%s,st_area(st_geometryfromtext(%s,25830)),st_geometryfromtext(%s,25830)) where gid = %s"
        self.conn.cursor.execute(q,[descripcion,geomWkt, geomWkt, gid])
        self.conn.conn.commit()
        n = self.conn.cursor.rowcount
        if n == 0:
            return {'ok':False,'message':f'Cero edificios actualizados','data':[[0]]}
        elif n==1:
            return {'ok':True,'message':f'Edificio actualizado. Filas afectadas: {n}','data':[[n]]}
        elif n > 1:
            return {'ok':False,'message':f'Demasiados edificios actualizados. Filas afectadas: {n}','data':[[n]]}
        
    def delete(self, gid:int)->int:
        """
        Deletes a building based in the gid
        """
        q="delete from d.buildings where gid = %s"
        self.conn.cursor.execute(q,[gid])
        n= self.conn.cursor.rowcount
        self.conn.conn.commit()
        if n == 0:
            return {'ok':False,'message':f'Cero edificios borrados','data':[[0]]}
        elif n==1:
            return {'ok':True,'message':f'Edificio borrado. Filas afectadas: {n}','data':[[n]]}
        elif n > 1:
            return {'ok':False,'message':f'Demasiados edificios borrados. Filas afectadas: {n}','data':[[n]]}
    
    def select(self, gid:int)->dict:
        q="select gid, descripcion, area, st_astext(geom) from d.buildings where gid = %s"
        self.conn.cursor.execute(q,[gid])
        l = self.conn.cursor.fetchall()
        n=len(l)
        return {'ok':True,'message':f'Edificios seleccionados: {n}','data':l}
        
    def selectAsDict(self, gid:int)->dict:
        q="""
        SELECT array_to_json(array_agg(registros)) FROM (
            select gid, descripcion, area, st_astext(geom), st_asgeojson(geom) 
            from d.buildings where gid = %s
         ) as registros
        """
        self.conn.cursor.execute(q,[gid])
        l = self.conn.cursor.fetchall()
        r=l[0][0]
        if r is None:
            return {'ok':True,'message':f'Edificios seleccionados: 0','data':[]}
        else:
            n=len(r)
            return {'ok':True,'message':f'Edificios seleccionados: {n}','data':r}

    def selectAsDictByArea(self, area:int)->dict:
        q="""
        SELECT array_to_json(array_agg(registros)) FROM (
            select gid, descripcion, area, st_astext(geom), st_asgeojson(geom) 
            from d.buildings where st_area(geom) > %s
         ) as registros
        """
        self.conn.cursor.execute(q,[area])
        l = self.conn.cursor.fetchall()
        r=l[0][0]
        if r is None:
            return {'ok':True,'message':f'Edificios seleccionados: 0','data':[]}
        else:
            n=len(r)
            return {'ok':True,'message':f'Edificios seleccionados: {n}','data':r}


    def selectAll(self)->list:
        q="select gid, descripcion, area, st_astext(geom) from d.buildings limit 1000"
        self.conn.cursor.execute(q,)
        l = self.conn.cursor.fetchall()
        n=len(l)
        return {'ok':True,'message':f'Edificios seleccionados: {n}','data':l}

    def selecAllAsDict(self):
        q="""
        SELECT array_to_json(array_agg(registros)) FROM (
            select gid, descripcion, area, st_astext(geom), st_asgeojson(geom) 
            from d.buildings limit 1000
         ) as registros
        """
        self.conn.cursor.execute(q)
        l = self.conn.cursor.fetchall()
        r=l[0][0]
        n=len(r)
        if r is None:
            return {'ok':True,'message':f'Edificios seleccionados: 0','data':[]}
        else:
            n=len(r)
            return {'ok':True,'message':f'Edificios seleccionados: {n}','data':r}





    def select_stores(self, gid)->list:
        
        if gid is None:
            print('ERROR: The gid has not been selected')
        else:
            q="""
            SELECT client_segment_id,store_name,store_description,geomWkt FROM d.stores where gid = %s)
            """
        self.conn.cursor.execute(q,[gid])
        l = self.conn.cursor.fetchall()
        r=l[0][0]
        if r is None:
            return {'ok':True,'message':f'Stores locations selected: 0','data':[]}
        else:
            n=len(r)
            return {'ok':True,'message':f'Stores locations selected: {n}','data':r}
####################################################





class Clients():
    
    conn:Conn
    def __init__(self,conn:Conn):
        self.conn=conn

    def insert_client(self,name,last_name,age,sex,geomWkt):
        """
        d is a dictionary
        client_type,sex, name,last_name,age,purchase_date,client_motivation,channel_id, geomWkt
        """
        
        #function
        q =f"insert into d.clients (name,last_name,age,sex,geom) values (%s,%s,%s,%s,st_geometryfromtext(%s,25830)) returning gid"
        self.conn.cursor.execute(q,[name,last_name,age,sex,geomWkt])
        #self.conn.cursor.execute(q,[d['client_type'],d['sex'],d['name'],d['last_name'],d['age'],d['purchase_date'],d['client_motivation'],d['channel_id'],d['geomWkt'])
        self.conn.conn.commit()
        gid = self.conn.cursor.fetchall()[0][0]
        return {'ok':True,'message':f'Cliente insertado. gid: {gid}','data':[[gid]]}



    
    def delete_client_by_gid(self, gid:int)->int:
        """
        Deletes a client location point based in the gid
        """
        q="delete from d.clients where gid = %s"
        self.conn.cursor.execute(q,[gid])
        n= self.conn.cursor.rowcount
        self.conn.conn.commit()
        if n == 0:
            return {'ok':False,'message':f'Error: Ningun cliente borrada','data':[[0]]}
        elif n==1:
            return {'ok':True,'message':f'Cliete borrado. Filas afectadas: {n}','data':[[n]]}
        elif n > 1:
            return {'ok':False,'message':f'Demasiados clientes borradas. Filas afectadas: {n}','data':[[n]]}


class Stores():


    conn:Conn
    def __init__(self,conn:Conn):
        self.conn=conn

    def insert_store(self,client_segment_id,store_name,store_description,geomWkt)->int:
        """
        d is a dictionary
        client_type,sex, name,last_name,age,purchase_date,client_motivation,channel_id, geomWkt
        """
        q =f"insert into d.stores (client_segment_id,store_name,store_description,geom) values (%s,%s,%s,st_geometryfromtext(%s,25830)) returning gid"
        self.conn.cursor.execute(q,[client_segment_id,store_name,store_description,geomWkt])
        #self.conn.cursor.execute(q,[d['client_type'],d['sex'],d['name'],d['last_name'],d['age'],d['purchase_date'],d['client_motivation'],d['channel_id'],d['geomWkt'])
        self.conn.conn.commit()
        gid = self.conn.cursor.fetchall()[0][0]
        return {'ok':True,'message':f'Tienda insertada. gid: {gid}','data':[[gid]]}
    
    
    def update_store(self,gid,client_segment_id,store_name,store_description,geomWkt)->int:
        q ="update d.stores set (client_segment_id,store_name,store_description,geom) = (%s,%s,%s,st_geometryfromtext(%s,25830)) where gid = %s"
        self.conn.cursor.execute(q,[client_segment_id,store_name,store_description,geomWkt,gid])
        self.conn.conn.commit()
        n = self.conn.cursor.rowcount
        if n == 0:
            return {'ok':False,'message':f'Ninguna tienda actualizada','data':[[0]]}
        elif n==1:
            return {'ok':True,'message':f'ubicaciones actualizadas. Filas afectadas: {n}','data':[[n]]}
        elif n > 1:
            return {'ok':False,'message':f'Demasiados tiendas actualizados. Filas afectadas: {n}','data':[[n]]}
        
    def delete_store_by_gid(self, gid:int)->int:
        """
        Deletes a store location point based in the gid
        """
        q="delete from d.stores where gid = %s"
        self.conn.cursor.execute(q,[gid])
        n= self.conn.cursor.rowcount
        self.conn.conn.commit()
        if n == 0:
            return {'ok':False,'message':f'Cero  ubicaciones','data':[[0]]}
        elif n==1:
            return {'ok':True,'message':f'Ubicacion borrada. Filas afectadas: {n}','data':[[n]]}
        elif n > 1:
            return {'ok':False,'message':f'Demasiadas ubicaciones borradas. Filas afectadas: {n}','data':[[n]]}

    def select_stores(self, gid)->list:
        """ if gid is None:
            q="select * from d.stores where gid = %s"
        else:
            q="select client_segment_id,store_name,store_description,st_astext(geom) from d.stores where gid = %s"

        self.conn.cursor.execute(q,[gid])
        l = self.conn.cursor.fetchall()
        n=len(l)
        return {'ok':True,'message':f'Edificios seleccionados: {n}','data':l}


              """       

        q="""
        SELECT array_to_json(array_agg(registros)) FROM (
            select gid,client_segment_id,store_name,store_description,st_astext(geom), st_asgeojson(geom) 
            from d.stores where gid = %s
         ) as registros
        """
        self.conn.cursor.execute(q,[gid])
        l = self.conn.cursor.fetchall()
        r=l[0][0]
        if r is None:
            return {'ok':True,'message':f'Tiendas seleccionados: 0','data':[]}
        else:
            n=len(r)
            return {'ok':True,'message':f'Tiendas seleccionados: {n}','data':r}


    
    




class Streets():
    
    conn:Conn
    def __init__(self,conn:Conn):
        self.conn=conn

    def insert_streets(self,street_name,municipality,postal_code,geomWkt):
        q =f"insert into d.streets (street_name,municipality,postal_code,geom) values (%s,%s,%s,st_geometryfromtext(%s,25830)) returning gid"
        self.conn.cursor.execute(q,[street_name,municipality,postal_code,geomWkt])
        #self.conn.cursor.execute(q,[d['client_type'],d['sex'],d['name'],d['last_name'],d['age'],d['purchase_date'],d['client_motivation'],d['channel_id'],d['geomWkt'])
        self.conn.conn.commit()
        gid = self.conn.cursor.fetchall()[0][0]
        return {'ok':True,'message':f'Calle insertada. gid: {gid}','data':[[gid]]}
     
     
    
    def delete_street_by_gid(self, gid:int)->int:
        """
        Deletes a store location point based in the gid
        """
        q="delete from d.stores where gid = %s"
        self.conn.cursor.execute(q,[gid])
        n= self.conn.cursor.rowcount
        self.conn.conn.commit()
        if n == 0:
            return {'ok':False,'message':f'Error: Ninguna calle borrada','data':[[0]]}
        elif n==1:
            return {'ok':True,'message':f'Calle borrada. Filas afectadas: {n}','data':[[n]]}
        elif n > 1:
            return {'ok':False,'message':f'Demasiadas calles borradas. Filas afectadas: {n}','data':[[n]]}
