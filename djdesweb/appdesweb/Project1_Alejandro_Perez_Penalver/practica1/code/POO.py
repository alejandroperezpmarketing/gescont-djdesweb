'''
Created on 27 feb. 2024

@author: vagrant
'''
from connPOO import Conn
from asn1crypto._ffi import null

"""
{'ok':true,'message':f'Edificios insertados: {n}','data': [[]]}

"""

   
class Buildings():
    conn:Conn
    def __init__(self,conn:Conn):
        self.conn=conn

    def insert(self,descripcion, geomWkt)->int:
        q =f"insert into d.buildings (descripcion,area, geom) values (%s,st_area(st_geometryfromtext(%s,25830)),st_geometryfromtext(%s,25830)) returning gid"
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
    
    def select(self, gid:int)->list:
        q="select gid, descripcion, area, st_astext(geom) from d.buildings where gid = %s"
        self.conn.cursor.execute(q,[gid])
        l = self.conn.cursor.fetchall()
        n=len(l)
        return {'ok':True,'message':f'Edificios seleccionados: {n}','data':l}
        
    def selectAsDict(self, gid:int)->list:
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

    def insert_client(self,d)->int:
        """
        d is a dictionary
        client_type,sex, name,last_name,age,purchase_date,client_motivation,channel_id, geomWkt
        """
        
        q =f"insert into d.clients (client_type,sex,name,last_name,age,purchase_date,client_motivation,channel_id,geom) values (%s,%s,%s,%s,%s,%s,%s,%s,st_geometryfromtext(%s,25830)) returning gid"
        self.conn.cursor.execute(q,[d['client_type'],d['sex'],d['name'],d['last_name'],d['age'],d['purchase_date'],d['client_motivation'],d['channel_id'],d['geomWkt']])
        #self.conn.cursor.execute(q,[d['client_type'],d['sex'],d['name'],d['last_name'],d['age'],d['purchase_date'],d['client_motivation'],d['channel_id'],d['geomWkt'])
        self.conn.conn.commit()
        gid = self.conn.cursor.fetchall()[0][0]
        return {'ok':True,'message':f'Cliente insertado. gid: {gid}','data':[[gid]]}
     
     
    def update_client(self,d)->int:
        q ="update d.clients set (client_type,sex,name,last_name,age,purchase_date,client_motivation,channel_id,geom) = (%s,%s,%s,%s,%s,%s,%s,%s,st_geometryfromtext(%s,25830)) where gid = %s"
        self.conn.cursor.execute(q,[d['client_type'],d['sex'],d['name'],d['last_name'],d['age'],d['purchase_date'],d['client_motivation'],d['channel_id'],d['geomWkt'],d['gid']])
        self.conn.conn.commit()
        n = self.conn.cursor.rowcount
        if n == 0:
            return {'ok':False,'message':f'Cero clientes actualizados','data':[[0]]}
        elif n==1:
            return {'ok':True,'message':f'ubicaciones actualizadas. Filas afectadas: {n}','data':[[n]]}
        elif n > 1:
            return {'ok':False,'message':f'Demasiados puntos actualizados. Filas afectadas: {n}','data':[[n]]}
        
    def delete_client(self, gid:int)->int:
        """
        Deletes a client location point based in the gid
        """
        q="delete from d.clients where gid = %s"
        self.conn.cursor.execute(q,[gid])
        n= self.conn.cursor.rowcount
        self.conn.conn.commit()
        if n == 0:
            return {'ok':False,'message':f'Cero  ubicaciones','data':[[0]]}
        elif n==1:
            return {'ok':True,'message':f'Ubicacion borrada. Filas afectadas: {n}','data':[[n]]}
        elif n > 1:
            return {'ok':False,'message':f'Demasiadas ubicaciones borradas. Filas afectadas: {n}','data':[[n]]}
    
    def select_client(self, gid=None)->list:
        if gid is None:
            q="select * from d.clients limit 1000"
        else:
            q="select gid,client_type,sex,name,last_name,age,purchase_date,client_motivation,channel_id,st_astext(geom) from d.clients where gid = %s limit 1000"

        self.conn.cursor.execute(q,[gid])
        l = self.conn.cursor.fetchall()
        n=len(l)
        return {'ok':True,'message':f'Edificios seleccionados: {n}','data':l}
        
    def selectAsDict_client(self, gid=None)->list:
        
        if gid is None:
            print('The gid has not been selected')
            q="""
            SELECT array_to_json(array_agg(registros)) FROM (
            select * from d.clients) as registros limit 1000
            """
        else:
            q="""
            SELECT array_to_json(array_agg(registros)) FROM (
            select client_type,sex, name,last_name,age,purchase_date,client_motivation,channel_id,st_astext(geom),st_asgeojson(geom) 
            from d.clients where gid = %s) as registros limit 1000
            """
        self.conn.cursor.execute(q,[gid])
        l = self.conn.cursor.fetchall()
        r=l[0][0]
        if r is None:
            return {'ok':True,'message':f'Clients locations selected: 0','data':[]}
        else:
            n=len(r)
            return {'ok':True,'message':f'Clients locations selected: {n}','data':r}

    def selectAll(self)->list:
        q="select gid, descripcion, area, st_astext(geom) from d.clients limit 1000"
        self.conn.cursor.execute(q,)
        l = self.conn.cursor.fetchall()
        n=len(l)
        return {'ok':True,'message':f'Ubicaciones seleccionadas: {n}','data':l}

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
            return {'ok':True,'message':f'Clients locations selected: 0','data':[]}
        else:
            n=len(r)
            return {'ok':True,'message':f'Clients locations selected: {n}','data':r}




class Stores():
    """
    ################
    CREATE DOMAIN store_service_products_domain as varchar;
    CREATE TABLE d.stores (
    gid  serial PRIMARY KEY, 
    client_segment_id integer NOT NULL,
    store_id integer NOT NULL, 
    store_name varchar, 
    star_store_service store_service_products_domain,
    star_store_product store_service_products_domain,
    dog_store_service store_service_products_domain,
    dog_store_product store_service_products_domain,
    cow_store_product store_service_products_domain,
    cow_store_service store_s

class Stores():
    
    ################
    CREATE DOMAIN store_service_products_domain as varchar;
    CREATE TABLE d.stores (
    gid  serial PRIMARY KEY, 
    client_segment_id integer NOT NULL,
    store_id integer NOT NULL, 
    store_name varchar, 
    star_store_service store_service_products_domain,
    star_store_product store_service_products_domain,
    dog_store_service store_service_products_domain,
    dog_store_product store_service_products_domain,
    question_store_service store_service_products_domain,
    question_store_product store_service_products_domain,
    store_owner_name varchar,
    store_owner_last_name varchar,
    store_Description varchar,
    connection_channel_id varchar,
    geom geometry ('POLYGON',25830)
   );


d['gid'],d['client_segment_id'],d['store_id'],d['store_name'],d['star_store_service'],d['star_store_product'],d['dog_store_service'],d['dog_store_product'],d['cow_store_product'],d['cow_store_service'],d['question_store_product'],['question_store_product'],d['question_store_service'],d['store_owner_name'],d['store_owner_last_name'],d['store_Description'],d['connection_channel_id'],d['geomWkt']
    """
    class Stores():
    conn:Conn
    def __init__(self,conn:Conn):
        self.conn=conn

    def insert_store(self,d)->int:
        """
        d is a dictionary
        client_type,sex, name,last_name,age,purchase_date,client_motivation,channel_id, geomWkt
        """
        q =f"insert into d.stores (client_segment_id,store_id,store_name,star_store_service,star_store_product,dog_store_service,dog_store_product,cow_store_product,cow_store_service,question_store_product,question_store_service,store_owner_name,store_owner_last_name,store_Description,connection_channel_id,geom) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,st_geometryfromtext(%s,25830)) returning gid"
        self.conn.cursor.execute(q,[d['client_segment_id'],d['store_id'],d['store_name'],d['star_store_service'],d['star_store_product'],d['dog_store_service'],d['dog_store_product'],d['cow_store_product'],d['cow_store_service'],d['question_store_product'],['question_store_service'],d['store_owner_name'],d['store_owner_last_name'],d['store_Description'],d['connection_channel_id'],d['geomWkt']])
        #self.conn.cursor.execute(q,[d['client_type'],d['sex'],d['name'],d['last_name'],d['age'],d['purchase_date'],d['client_motivation'],d['channel_id'],d['geomWkt'])
        self.conn.conn.commit()
        gid = self.conn.cursor.fetchall()[0][0]
        return {'ok':True,'message':f'Cliente insertado. gid: {gid}','data':[[gid]]}
     
     
    def update_stores(self,d)->int:
        q ="update d.stores set (client_segment_id,store_id,store_name,star_store_service,star_store_product,dog_store_service,dog_store_product,cow_store_product,cow_store_service,question_store_product,question_store_service,store_owner_name,store_owner_last_name,store_Description,connection_channel_id,geom) = (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,st_geometryfromtext(%s,25830)) where gid = %s"
        self.conn.cursor.execute(q,[d['client_segment_id'],d['store_id'],d['store_name'],d['star_store_service'],d['star_store_product'],d['dog_store_service'],d['dog_store_product'],d['cow_store_product'],d['cow_store_service'],d['question_store_product'],['question_store_service'],d['store_owner_name'],d['store_owner_last_name'],d['store_Description'],d['connection_channel_id'],d['geomWkt'],d['gid']])
        self.conn.conn.commit()
        n = self.conn.cursor.rowcount
        if n == 0:
            return {'ok':False,'message':f'Cero tiendas actualizados','data':[[0]]}
        elif n==1:
            return {'ok':True,'message':f'ubicaciones actualizadas. Filas afectadas: {n}','data':[[n]]}
        elif n > 1:
            return {'ok':False,'message':f'Demasiados tiendas actualizados. Filas afectadas: {n}','data':[[n]]}
        
    def delete_stores(self, gid:int)->int:
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
    
    def select_stores(self, gid=None)->list:
        if gid is None:
            q="select * from d.stores limit 1000"
        else:
            q="select client_segment_id,store_id,store_name,star_store_service,star_store_product,dog_store_service,dog_store_product,cow_store_product,cow_store_service,question_store_product,question_store_service,store_owner_name,store_owner_last_name,store_Description,connection_channel_id,st_astext(geom) from d.stores where gid = %s limit 1000"

        self.conn.cursor.execute(q,[gid])
        l = self.conn.cursor.fetchall()
        n=len(l)
        return {'ok':True,'message':f'Edificios seleccionados: {n}','data':l}
        
    def selectAsDict_stores(self, gid=None)->list:
        
        if gid is None:
            print('The gid has not been selected')
            q="""
            SELECT array_to_json(array_agg(registros)) FROM (
            select * from d.stores) as registros
            """
        else:
            q="""
            SELECT array_to_json(array_agg(registros)) FROM (
            select client_segment_id,store_id,store_name,star_store_service,star_store_product,dog_store_service,dog_store_product,cow_store_product,cow_store_service,question_store_product,question_store_service,store_owner_name,store_owner_last_name,store_Description,connection_channel_id,st_astext(geom),st_asgeojson(geom) 
            from d.stores where gid = %s) as registros
            """
        self.conn.cursor.execute(q,[gid])
        l = self.conn.cursor.fetchall()
        r=l[0][0]
        if r is None:
            return {'ok':True,'message':f'Stores locations selected: 0','data':[]}
        else:
            n=len(r)
            return {'ok':True,'message':f'Stores locations selected: {n}','data':r}

    def selectAll(self)->list:
        q="select gid, descripcion, area, st_astext(geom) from d.clients limit 1000"
        self.conn.cursor.execute(q,)
        l = self.conn.cursor.fetchall()
        n=len(l)
        return {'ok':True,'message':f'Stores selected: {n}','data':l}

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
            return {'ok':True,'message':f'Clients locations selected: 0','data':[]}
        else:
            n=len(r)
            return {'ok':True,'message':f'Clients locations selected: {n}','data':r}



class Streets():
    """
    ################
    CREATE DOMAIN oneway_domain as varchar NOT NULL CONSTRAINT oneway_constraint CHECK (value in ('FT','TF','T','F','N','D'));
    create table d.streets (
    gid  serial PRIMARY KEY,
    street_type varchar DEFAULT 'calle',
    street_name varchar, 
    postal_code integer,
    municipality varchar,
    provice varchar DEFAULT 'valencia',
    region varchar DEFAULT 'valencia',
    country varchar DEFAULT 'spain',
    hierarchy integer DEFAULT 1,
    ONEWAY oneway_domain,
    street_lenght double precision,
    street_validation boolean,
    geom geometry (LINESTRING,25830));
    
    (gid,street_type,street_name,postal_code,municipality,provice,region,country,hierarchy,ONEWAY,street_lenght,street_validation,geom)
    
    campos : 
    ONEWAY (N no sentido de calle, T o FT direccion de FROM A TO, F o TF direecion de TO a FROM, D doble sentido de calle), 
    """
    
    conn:Conn
    def __init__(self,conn:Conn):
        self.conn=conn

    def insert_streets(self,d)->int:
        """
        d is a dictionary
        gid,zone_id,street_type,street_name,postal_code,municipality,provice,region,country,hierarchy,ONEWAY,street_lenght,street_validation,geomWkt
        """
        
        q =f"insert into d.streets (street_type,street_name,postal_code,municipality,provice,region,country,hierarchy,ONEWAY,street_length,street_validation,geom) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,st_length(st_geometryfromtext(%s)),st_isvalid(st_geometryfromtext(%s)),st_geometryfromtext(%s,25830)) returning gid"
        self.conn.cursor.execute(q,[d['street_type'],d['street_name'],d['postal_code'],d['municipality'],d['provice'],d['region'],d['country'],d['hierarchy'],d['ONEWAY'],d['geomWkt'],d['geomWkt'],d['geomWkt']])
        #self.conn.cursor.execute(q,[d['client_type'],d['sex'],d['name'],d['last_name'],d['age'],d['purchase_date'],d['client_motivation'],d['channel_id'],d['geomWkt'])
        self.conn.conn.commit()
        gid = self.conn.cursor.fetchall()[0][0]
        return {'ok':True,'message':f'Calle insertada. gid: {gid}','data':[[gid]]}
     
     
    def update_streets(self,d)->int:
        q ="update d.streets set (street_type,street_name,postal_code,municipality,provice,region,country,hierarchy,ONEWAY,street_length,street_validation,geom) = (%s,%s,%s,%s,%s,%s,%s,%s,%s,st_length(st_geometryfromtext(%s)),st_isvalid(st_geometryfromtext(%s)),st_geometryfromtext(%s,25830)) where gid = %s"
        self.conn.cursor.execute(q,[d['street_type'],d['street_name'],d['postal_code'],d['municipality'],d['provice'],d['region'],d['country'],d['hierarchy'],d['ONEWAY'],d['geomWkt'],d['geomWkt'],d['geomWkt'],d['gid']])
        self.conn.conn.commit()
        n = self.conn.cursor.rowcount
        if n == 0:
            return {'ok':False,'message':f'Ninguna calle actualizada','data':[[0]]}
        elif n==1:
            return {'ok':True,'message':f'Calles actualizadas. Filas afectadas: {n}','data':[[n]]}
        elif n > 1:
            return {'ok':False,'message':f'Demasiados elementos actualizados. Filas afectadas: {n}','data':[[n]]}
        
    def delete_streets(self, gid:int)->int:
        """
        Deletes a street line based in the gid
        """
        q="delete from d.streets where gid = %s"
        self.conn.cursor.execute(q,[gid])
        n= self.conn.cursor.rowcount
        self.conn.conn.commit()
        if n == 0:
            return {'ok':False,'message':f'Cero  calles','data':[[0]]}
        elif n==1:
            return {'ok':True,'message':f'Calle borrada. Filas afectadas: {n}','data':[[n]]}
        elif n > 1:
            return {'ok':False,'message':f'Demasiadas calles borradas. Filas afectadas: {n}','data':[[n]]}
    
    def select_streets(self, gid=None)->list:
        if gid is None:
            print('The gid has not been selected--RESULT: ALL COLUMNS')
            q="select * from d.streets limit 1000;"
        else:
            q="select gid,street_type,street_name,postal_code,municipality,provice,region,country,hierarchy,ONEWAY,street_length::float,street_validation,st_astext(geom) from d.streets where gid = %s limit 1000;"

        self.conn.cursor.execute(q,[gid])
        l = self.conn.cursor.fetchall()
        n=len(l)
        return {'ok':True,'message':f'Calles seleccionadas: {n}','data':l}
        
    def selectAsDict_streets(self, gid=None)->list:
        
        if gid is None:
            print('The gid has not been selected')
            q="""
            SELECT array_to_json(array_agg(registros)) FROM (
            select * from d.clients) as registros
            """
        else:
            q="""
            SELECT array_to_json(array_agg(registros)) FROM (
            select client_type,sex, name,last_name,age,purchase_date,client_motivation,channel_id,st_astext(geom),st_asgeojson(geom) 
            from d.clients where gid = %s) as registros
            """
        self.conn.cursor.execute(q,[gid])
        l = self.conn.cursor.fetchall()
        r=l[0][0]
        if r is None:
            return {'ok':True,'message':f'Clients locations selected: 0','data':[]}
        else:
            n=len(r)
            return {'ok':True,'message':f'Clients locations selected: {n}','data':r}

    
   