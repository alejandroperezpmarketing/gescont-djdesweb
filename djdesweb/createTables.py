
from appdesweb.pycode.connPOO import Conn

conn = Conn()
print('Creando la tabla demo')
conn.cursor.execute('create schema d')
conn.cursor.execute('create table d.buildings (gid serial primary key, descripcion varchar, area double precision, geom geometry("polygon",25830))')
conn.cursor.execute('create table demo (gid serial primary key, descripcion varchar)')
conn.conn.commit()