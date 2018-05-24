
# coding: utf-8

# ## Libraries to use
# 
# Import of the necessary libraries to execute the current program
# 
# *Importación de las librerías necesarias para ejecutar el programa actual*

# In[ ]:


import googlemaps #To API google
import pandas as pd #To use csv files
import numpy as np #To mathematical functions


# ## Directions API
# 
# Returns indications of several parts for a series of waypoints, indications for various means of transport are available.
# 
# *Devuelve indicaciones de varias partes para una serie de waypoints, estan disponibles indicaciones para varios medios de transporte.*

# In[ ]:


def directions_api (origin, destination):
    #Max query 2500 per day 
    key_direction = 'AIzaSyCOuWn0Ut3cIOqsYvXWkV3WwqMf18EFVWw' #Dani
    
    gmaps = googlemaps.Client(key_direction)
    directions = gmaps.directions(origin,destination,"driving") # To car
    
    # To take the duration an distance for the subpoints on the route
    list_duration = []
    list_distance = []
    list_origin = []
    list_destination=[]
    steps = directions[0]['legs'][0]['steps']

    #Add the values in a list
    for sub_steps in steps:
        list_origin.append([sub_steps['start_location']['lat'],sub_steps['start_location']['lng']])
        list_destination.append([sub_steps['end_location']['lat'],sub_steps['end_location']['lng']])
        list_duration.append(sub_steps['duration']['value']) # data in seconds
        list_distance.append(sub_steps['distance']['value']) # data in meters
        
    return list_origin,list_destination,list_distance,list_duration


# ## Elevation API
# 
# The Google Maps Elevation API provides elevation data for all locations on the Earth's surface, including deep locations on the seabed (which return negative values).
# 
# *Google Maps Elevation API proporciona datos de elevación para todas las ubicaciones sobre la superficie terrestre, incluidas ubicaciones profundas en el lecho marino (que devuelven valores negativos).*

# In[ ]:


def elevation_api(origin, destination): #2 lists with latitude and longitude
    #Max query 2500 per day 
    key_elevation='AIzaSyCOuWn0Ut3cIOqsYvXWkV3WwqMf18EFVWw' #Dani
    
    gelevation = googlemaps.Client(key_elevation)
    elevation = gelevation.elevation([origin, destination])
    return elevation[0]['elevation'],elevation[1]['elevation']

def geodesic_distance(origin,destination): #2 lists with latitude and longitude
    # https://web.archive.org/web/20090813162802/http://gorny.edu.pl/haversine.py
    earth_radius = 6371e3
    phi1 = origin[0] * np.pi / 180 # Convert to radians lat origin
    phi2 = destination[0] * np.pi / 180 # Convert to radians lat destiny
    lambda1 = origin[1] * np.pi / 180 # Convert to radians long origin
    lambda2 = destination[1] * np.pi / 180 # Convert to radians long origin
    
    delta_phi = phi2 - phi1
    delta_lambda = lambda2 - lambda1
    
    value_sqrt = np.sin(delta_phi / 2)**2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2) ** 2
    harvesine = 2 * earth_radius * np.arctan2(np.sqrt(value_sqrt), np.sqrt(1 - value_sqrt))
    return harvesine
    
def get_list_elevation_angle(list_origin, list_destination): 
    #Return the elevation angle between two points in a list
    list_elevation = []
    for i in range(len(list_origin)):
        elevation_points = elevation_api(list_origin[i], list_destination[i])
        distance = geodesic_distance(list_origin[i], list_destination[i])
        difference_elevation = elevation_points[1] - elevation_points[0]   
        list_elevation.append(np.arctan(np.abs(difference_elevation / distance)) * 180 / np.pi)
    return list_elevation


# ## Data from model
# 
# Generation of information necessary to use in the loading and unloading model of the electric vehicle, by restrictions of the API's you can not iterate over all the data at the same time
# 
# *Generacion de información necesaria para utilizar en el modelo de carga y descarga del vehiculo electrico, por restricciones de las API's no se puede iterar sobre todos los datos al tiempo*

# In[ ]:


#File path where the points are located
substations = ['Centro', 'Dosquebradas', 'Ventorrillo', 'Cuba', 'Naranjito']
days = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']
hours = ['6-9', '12-14', '18-20']

for substation in substations:
    for day in days:
        for hour in hours:
            print substation,day,hour, 'From V' + str(substations.index(substation)+1) + ' to V5_'+ hour+'.csv'
            file_path = 'Substations/' + substation + '/Puntos Aleatorios/'+ day + ' '+ hour +'/From V' + str(substations.index(substation)+1) + ' to V5_'+ hour +'.csv'
            data = pd.read_csv(file_path, header=0)
            data_routes= pd.DataFrame()
            columns = ['X1','Y1','X2','Y2','Subpoints_origin','Subpoints_destiny','Distance','Duration','Elevation']
            try:
                for row in data.itertuples():
                    route_data_list = directions_api([row[2],row[1]],[row[4],row[3]])
                    elevation_data_list = get_list_elevation_angle(route_data_list[0],route_data_list[1])
                    x1 = [None]*len(elevation_data_list)
                    y1 = [None]*len(elevation_data_list)
                    x2 = [None]*len(elevation_data_list)
                    y2 = [None]*len(elevation_data_list)
            
                    x1[0] = row[2]
                    y1[0] = row[1]
                    x2[0] = row[4]
                    y2[0] = row[3]
                    data_temp = pd.DataFrame({
                        'X1':x1,
                        'Y1':y1,
                        'X2':x2,
                        'Y2':y2,
                        'Subpoints_origin':route_data_list[0], 
                        'Subpoints_destiny':route_data_list[1], 
                        'Distance':route_data_list[2], 
                        'Duration':route_data_list[3], 
                        'Elevation':elevation_data_list
                    })
                    data_routes = pd.concat([data_routes, data_temp], ignore_index=True,keys = [[row[2],row[1]],[row[4],row[3]]])
                data_routes = data_routes[columns] # To order the columns in dataframe
                data_routes.to_csv(file_path, header=columns, index=False)
            except:
                data_routes = data_routes[columns] # To order the columns in dataframe
                data_routes.to_csv('Substations/Centro/Puntos Aleatorios/Lunes 6-9/temp.csv', header=columns, index=False)

