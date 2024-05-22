
from appdesweb.pycode.connPOO import Conn

conn = Conn()
print('Creando la tabla demo')
#conn.cursor.execute('create schema d')
#conn.cursor.execute('create table d.buildings (gid serial primary key, descripcion varchar, area double precision, geom geometry("polygon",25830))')
#conn.cursor.execute('create table demo (gid serial primary key, descripcion varchar)')
#Alejandro
#puntos
#conn.cursor.execute('create table d.especies (gid  serial PRIMARY KEY, description varchar, species_type varchar, care varchar, motivation varchar, name varchar, scientific_name varchar, species_lives_season varchar, geom geometry (POINT,25830))')
conn.cursor.execute('create table d.clients (gid  serial PRIMARY KEY, client_type varchar,sex varchar, name varchar, last_name varchar, age integer DEFAULT 0,   purchase_date date,client_motivation varchar,channel_id integer,geom geometry (POINT,25830))')
conn.cursor.execute('')
conn.cursor.execute('')
conn.cursor.execute('')
conn.conn.commit()