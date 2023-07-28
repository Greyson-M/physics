"""
Multifold Henon Attraktor
21.12.2020
www.3d-meier.de
"""

import c4d
import math

# Variablen und Konstanten
Titel = 'Multifold Henon Attraktor' # Name

a = 4.0             # Konstane a
b = 0.9             # Konstante b


Nv = 100               # Anzahl Punkte verwerfen
N =  2000000           # Anzahl Punkte

dx = 10.0              # Kantenlaenge Quadrat

x0 = 0.1               # Startwert x
y0 = 0.1               # Startwert y

Faktor = 1000          # Skalierungsfaktor



def CreatePolygonObject():
    obj = c4d.BaseObject(c4d.Opolygon)
    obj.ResizeObject(4*N, N)
    obj.SetName(Titel)
  # Zaehler fuer Punkte setzten
    zz = 0
  # Zaehler fuer Polygone setzten
    zzz = 0
  # Startwerte _ben
    xa = x0
    y = y0
  # Punkte verwerfen
    for i in xrange(0,Nv):
      # Neuen Wert berechnen
        x=1-a*math.sin(xa)+b*y
        y=xa

      # x Werte aktualisieren
        xa=x;
  # Punkte berechnen
    for i in xrange(0,N):
      # Neuen Wert berechnen
        x=1-a*math.sin(xa)+b*y
        y=xa
      # x Werte aktualisieren
        xa=x;
      # Polygon erzeugen
        obj.SetPoint(zz, c4d.Vector((x*Faktor-dx/2.0),(y*Faktor+dx/2.0),0))
        zz=zz+1
        obj.SetPoint(zz, c4d.Vector((x*Faktor-dx/2.0),(y*Faktor-dx/2.0),0))
        zz=zz+1
        obj.SetPoint(zz, c4d.Vector((x*Faktor+dx/2.0),(y*Faktor+dx/2.0),0))
        zz=zz+1
        obj.SetPoint(zz, c4d.Vector((x*Faktor+dx/2.0),(y*Faktor-dx/2.0),0))
        zz=zz+1
        obj.SetPolygon(zzz, c4d.CPolygon(zz-1,zz-2,zz-4,zz-3))
        zzz=zzz+1

    #
    obj.Message(c4d.MSG_UPDATE)
    return obj



def main():
    plyobj = CreatePolygonObject()

    #
    doc.InsertObject(plyobj, None, None, True)

    c4d.EventAdd()



if __name__=='__main__':
    main()
