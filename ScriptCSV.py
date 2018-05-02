import PyQt4.Qsci 
import processing
from PyQt4.QtGui import QInputDialog
import pandas as pd

canvas = qgis.utils.iface.mapCanvas() 
allLayers = canvas.layers()

zona = QInputDialog.getText(None, 'ZONA', 'Zona')
dia = QInputDialog.getText(None, 'DIA', 'Dia')
hora = QInputDialog.getText(None, 'HORA', 'Hora')

for layer in allLayers:
    if layer.name().find("From") >=0 or layer.name().find("to v") >=0:
        QgsVectorFileWriter.writeAsVectorFormat(layer, r'/home/dani/Desktop/MonteCarlo-Simulation/Substations/'+ zona[0] +'/Puntos Aleatorios/'+ dia[0] +' '+ hora[0] +'/'+ layer.name() +'_'+ hora[0] +'.csv', "utf-8", None, "CSV",layerOptions =['GEOMETRY=AS_XY'])