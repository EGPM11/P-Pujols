import requests
import math
from datetime import datetime

def calcular_desplazamiento_maximo(magnitud, distancia):
    return 10**(0.5 * magnitud + 1.05 * math.log10(distancia) - 3.01)

def buscar_sismo_cerca(latitud, longitud, radio_km):
    # URL de la API de USGS para obtener datos de terremotos
    url = 'https://earthquake.usgs.gov/fdsnws/event/1/query'

    # Parámetros de la solicitud
    parametros = {
        'format': 'geojson',
        'latitude': latitud,
        'longitude': longitud,
        'maxradiuskm': radio_km,
        'orderby': 'time',
        'limit': 1
    }

    # Realizar la solicitud a la API
    response = requests.get(url, params=parametros)
    data = response.json()

    # Verificar si se encontró un sismo cercano
    if 'features' in data and len(data['features']) > 0:
        # Obtener la magnitud, fecha y la distancia al epicentro del sismo
        sismo = data['features'][0]['properties']
        magnitud_terremoto = sismo['mag']
        epicentro = sismo['place']
        fecha_sismo = datetime.utcfromtimestamp(sismo['time'] / 1000).strftime('%Y%m%d')
        coordenadas_epicentro = data['features'][0]['geometry']['coordinates']
        latitud_epicentro, longitud_epicentro = coordenadas_epicentro[1], coordenadas_epicentro[0]

        # Calcular la distancia al epicentro
        distancia_epicentro_km = radio_km
        desplazamiento_maximo_metros = calcular_desplazamiento_maximo(magnitud_terremoto, distancia_epicentro_km)

        # Mostrar el resultado
        print(f"Se encontró un sismo de magnitud {magnitud_terremoto} en {epicentro} (latitud: {latitud_epicentro}, longitud: {longitud_epicentro})")
        print(f"Fecha del sismo: {fecha_sismo}")
        print(f"El desplazamiento máximo teórico es de {desplazamiento_maximo_metros:.2f} metros.")
    else:
        print("No se encontraron sismos cercanos en el radio especificado.")

# Coordenadas y radio de búsqueda
latitud = 18.65017
longitud = -68.66281
radio_km = 100  # Radio de búsqueda en kilómetros

# Buscar sismo cercano y calcular desfase
buscar_sismo_cerca(latitud, longitud, radio_km)
