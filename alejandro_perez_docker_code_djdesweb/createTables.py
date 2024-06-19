
from alejandro_perez_appdesweb.pycode.connPOO import Conn

conn = Conn()
print('Creando la tabla demo')
#conn.cursor.execute('create schema d')
#conn.cursor.execute('create table d.buildings (gid serial primary key, descripcion varchar, area double precision, geom geometry("polygon",25830))')
#conn.cursor.execute('create table demo (gid serial primary key, descripcion varchar)')
#Alejandro
#puntos
#conn.cursor.execute('create table d.especies (gid  serial PRIMARY KEY, description varchar, species_type varchar, care varchar, motivation varchar, name varchar, scientific_name varchar, species_lives_season varchar, geom geometry (POINT,25830))')
conn.cursor.execute('create table d.clients (gid  serial PRIMARY KEY, sex varchar, name varchar, last_name varchar, age integer DEFAULT 0, geom geometry (POINT,25830))')
conn.cursor.execute('create table d.stores (gid  serial PRIMARY KEY, client_segment_id integer, store_name varchar, store_description varchar,geom geometry (POLYGON,25830))')
conn.cursor.execute('create table d.streets (gid  serial PRIMARY KEY, street_name varchar, postal_code integer, municipality varchar, geom geometry (LINESTRING,25830))')
