'''
Created on 27 feb. 2024

@author: vagrant
'''
from connPOO import Conn
import buildingsPOO

#conn=Conn()
#buildingsPOO.insertBuilding(conn=conn, 
#                            descripcion='A ver si va', 
#                            geomWkt='POLYGON((0 0, 100 0, 100 100, 0 100, 0 0))' )

#buildingsPOO.updateBuilding(conn=conn, 
#                            gid = 11, 
#                            descripcion= 'Soy el  11', 
#                            geomWkt = 'POLYGON((0 0, 100 0, 150 150, 0 100, 0 0))')

conn=Conn()
b=buildingsPOO.Buildings(conn)
r=b.insert(descripcion='POO', geomWkt='POLYGON((0 0, 100 0, 100 100, 0 100, 0 0))')
gid=r['data'][0][0]
print(gid)
n=b.update(gid=88899, descripcion='Soy el 10', geomWkt='POLYGON((0 0, 100 0, 150 150, 0 100, 0 0))')
print(f'Filas actualizadas {n}')
l=b.select(565654)
print(l)
l=b.selectAsDict(5555)
print(l)
n=b.delete(gid=8880)
print(f'Filas borradas {n}')

print(b.selectAll())
print(b.selecAllAsDict())

conn.close()


print('Done')




