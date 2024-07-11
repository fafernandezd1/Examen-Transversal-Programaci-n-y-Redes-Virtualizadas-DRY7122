import requests
import urllib.parse

route_url = "https://graphhopper.com/api/1/route?"
key = "6380ddff-61d3-43a4-91f1-cb761bb01fdc"  # Reemplaza con tu clave de API

def geocoding(location, key):
    geocode_url = "https://graphhopper.com/api/1/geocode?"
    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})

    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code
    print("Geocoding API URL for " + location + ":\n" + url)
    
    if json_status == 200 and len(json_data["hits"]) != 0:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")

        if state and country:
            new_loc = f"{name}, {state}, {country}"
        elif state:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name

        print(f"Geocoding API URL for {new_loc} (Location Type: {value})\n{url}")
        return json_status, lat, lng, new_loc
    else:
        print(f"Error en la solicitud. Estado: {json_status}")
        if json_status == 402:
            print("**********************************************")
            print("Status Code: 402; Inputs de usuario no válidos para una o ambas ubicaciones.")
            print("**********************************************\n")
        elif json_status == 611:
            print("**********************************************")
            print("Status Code: 611; Falta una entrada para una o ambas ubicaciones.")
            print("**********************************************\n")
        else:
            print("************************************************************************")
            print(f"For Status Code: {json_status}; Refer to:")
            print("https://www.graphhopper.com/api-docs/ui/?url=https://graphhopper.com/api/1/docs/route.yaml")
            print("************************************************************************\n")
        return json_status, None, None, location

def obtener_ruta(origen, destino, key, vehicle):
    orig = geocoding(origen, key)
    dest = geocoding(destino, key)

    if orig[0] != 200 or dest[0] != 200:
        print("No se pudieron obtener las coordenadas para calcular la ruta.")
        return

    op = f"&point={orig[1]},{orig[2]}"
    dp = f"&point={dest[1]},{dest[2]}"
    vehicle_param = f"&vehicle={vehicle}"
    paths_url = route_url + urllib.parse.urlencode({"key": key}) + op + dp + vehicle_param
    paths_data = requests.get(paths_url).json()
    paths_status = requests.get(paths_url).status_code

    if paths_status == 200 and "paths" in paths_data and len(paths_data["paths"]) > 0:
        print("Routing API Status:", paths_status)
        print("Routing API URL:\n", paths_url)
        return paths_data
    else:
        print(f"No se encontraron rutas válidas entre {orig[3]} y {dest[3]}.")
        return None

def seleccionar_medio_transporte():
    while True:
        print("Seleccione el medio de transporte:")
        print("1. Coche")
        print("2. Bicicleta")
        print("3. A pie")
        choice = input("Ingrese el número correspondiente (1/2/3): ")

        if choice == "1":
            return "car"
        elif choice == "2":
            return "bike"
        elif choice == "3":
            return "foot"
        else:
            print("Opción no válida. Por favor, elija 1, 2 o 3.")

while True:
    loc1 = input("Ciudad de origen (o 'quit' para terminar): ")
    if loc1.lower() == "quit" or loc1.lower() == "q":
        break

    loc2 = input("Ciudad de destino (o 'quit' para terminar): ")
    if loc2.lower() == "quit" or loc2.lower() == "q":
        break

    vehicle = seleccionar_medio_transporte()
    paths_data = obtener_ruta(loc1, loc2, key, vehicle)

    if paths_data:
        print("=================================================")
        print(f"Directions from {loc1} to {loc2}:")
        print("=================================================")
        print("Distancia recorrida en metros:", paths_data["paths"][0]["distance"])
        print("Duración del viaje en segundos:", paths_data["paths"][0]["time"])
        print("=================================================")
        for maneuver in paths_data["paths"][0]["instructions"]:
            print(maneuver["text"], "(", maneuver["distance"], "m)")
        print("=================================================\n")
