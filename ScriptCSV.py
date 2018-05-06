import PyQt4.Qsci
import processing
from PyQt4.QtGui import QInputDialog
import pandas as pd
import os

canvas = qgis.utils.iface.mapCanvas()
allLayers = canvas.layers()

zona = QInputDialog.getText(None, 'ZONA', 'Zona')
dia = QInputDialog.getText(None, 'DIA', 'Dia')
hora = QInputDialog.getText(None, 'HORA', 'Hora')
os.makedirs("/home/vanessa/Repositorios/MonteCarlo-Simulation/Substations/"+zona[0] +'/Puntos Aleatorios/'+ dia[0] +' '+ hora[0])

for layer in allLayers:
    if layer.name().find("From") >=0 or layer.name().find("to v") >=0:
        QgsVectorFileWriter.writeAsVectorFormat(layer, r'/home/vanessa/Repositorios/MonteCarlo-Simulation/Substations/'+ zona[0] +'/Puntos Aleatorios/'+ dia[0] +' '+ hora[0] +'/'+ layer.name() +'_'+ hora[0] +'.csv', "utf-8", None, "CSV",layerOptions =['GEOMETRY=AS_XY'])
       
for layer in allLayers:
    if layer.name().find("From") >=0:
        dataf1 = pd.read_csv(r'/home/vanessa/Repositorios/MonteCarlo-Simulation/Substations/'+ zona[0] +'/Puntos Aleatorios/'+ dia[0] +' '+ hora[0] +'/'+ layer.name() +'_'+ hora[0] +'.csv', header=0)
        dataf2 = pd.read_csv(r'/home/vanessa/Repositorios/MonteCarlo-Simulation/Substations/'+ zona[0] +'/Puntos Aleatorios/'+ dia[0] +' '+ hora[0] +'/to v'+ layer.name()[-1] +'_'+ hora[0] +'.csv', header=0)

        dataf_total = dataf1.merge(dataf2,on='ID')
        dataf_total.drop(dataf_total.columns[[2,3,6]],axis = 1, inplace=True)
        dataf_total.to_csv(r'/home/vanessa/Repositorios/MonteCarlo-Simulation/Substations/'+ zona[0] +'/Puntos Aleatorios/'+ dia[0] +' '+ hora[0] +'/'+ layer.name() +'_'+ hora[0] +'.csv', header=["X1","Y1","X2","Y2"], index=False)

        os.remove( r'/home/vanessa/Repositorios/MonteCarlo-Simulation/Substations/'+ zona[0] +'/Puntos Aleatorios/'+ dia[0] +' '+ hora[0] +'/to v'+ layer.name()[-1] +'_'+ hora[0] +'.csv')
