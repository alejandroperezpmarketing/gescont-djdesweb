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



####################################################





class Clients():
    """
    ################
    
    create table d.clients (
    gid  serial PRIMARY KEY, 
    client_type varchar,
    sex varchar, 
    name varchar, 
    last_name varchar, 
    age integer DEFAULT 0,   
    purchase_date date,
    client_motivation varchar,
    channel_id integer,
    geom geometry (POINT,25830));
    
    
    
    campos : 
    client_type (física o jurídica), 
    name ( si es juridica el nombre de la empresa si es  fisica el nombre de la persona
    sex (double precision valor por defecto 'NA'
    age (integrer valor por defecto (NA)
    purchase_date (date)
    client_motivation ( descripcion de que busca  el cliente con nuestro servicio o producto)
    channel_id
    """
    
    conn:Conn
    def __init__(self,conn:Conn):
        self.conn=conn

    def insert_client(self,name,last_name,age,sex,purchase_date,client_motivation,channel_id,geomWkt)->int:
        """
        d is a dictionary
        client_type,sex, name,last_name,age,purchase_date,client_motivation,channel_id, geomWkt
        """
        
        #function
        q =f"insert into d.clients (client_type,sex,name,last_name,age,purchase_date,client_motivation,channel_id,geom) values (%s,%s,%s,%s,%s,%s,%s,%s,st_geometryfromtext(%s,25830)) returning gid"
        self.conn.cursor.execute(q,[client_type,sex,name,last_name,age,purchase_date,client_motivation,channel_id,geomWkt])
        #self.conn.cursor.execute(q,[d['client_type'],d['sex'],d['name'],d['last_name'],d['age'],d['purchase_date'],d['client_motivation'],d['channel_id'],d['geomWkt'])
        self.conn.conn.commit()
        gid = self.conn.cursor.fetchall()[0][0]
        return {'ok':True,'message':f'Cliente insertado. gid: {gid}','data':[[gid]]}


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
        return {'ok':True,'message':f'Cliente insertado. gid: {gid}','data':[[gid]]}
     