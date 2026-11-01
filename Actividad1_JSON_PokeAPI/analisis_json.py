import json
import urllib.request
from collections import Counter

from itertools import islice, groupby


def pedir(url):
    peticion = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    return json.load(urllib.request.urlopen(peticion, timeout=10))




def todas_las_paginas():
    url = "https://pokeapi.co/api/v2/pokemon?limit=100"
    lista = []
    while url:
        datos = pedir(url)
        lista = lista + datos["results"]
        url = datos["next"]
    return lista



#2
def aplanar(dato, nombre=""):
    resultado = {}
    if isinstance(dato, dict):
        for clave, valor in dato.items():
            nuevo = nombre + "." + clave if nombre else clave
            resultado.update(aplanar(valor, nuevo))
    elif isinstance(dato, list):
        for i, valor in enumerate(dato):
            nuevo = nombre + "." + str(i) if nombre else str(i)
            resultado.update(aplanar(valor, nuevo))
    else:
        resultado[nombre] = dato
    return resultado



#3
def tomar_datos(p):
    return {
        "nombre": p.get("name"),
        "peso": p.get("weight") or 0,
        "altura": p.get("height") or 0,
        "tipos": [t["type"]["name"] for t in p.get("types") or []],
    }



#4
REGLAS = {"nombre": str, "peso": int, "altura": int, "tipos": list}


def es_valido(p):
    for campo, tipo in REGLAS.items():
        if not isinstance(p[campo], tipo):
            return False
    return len(p["tipos"]) > 0





#Principal

lista = todas_las_paginas()
print("Pokemon en la lista:", len(lista))

# Detalle solo de los primeros 150 (para no hacer mas de 1300 peticiones)
crudos = [pedir(item["url"]) for item in islice(lista, 150)]
pokes = [tomar_datos(c) for c in crudos]
validos = [p for p in pokes if es_valido(p)]
print("Validos:", len(validos), "Invalidos:", len(pokes) - len(validos))

# 5. Estadisticas
pesos = [p["peso"] for p in validos]
alturas = [p["altura"] for p in validos]
conteo_tipos = Counter([t for p in validos for t in p["tipos"]])

peso_promedio_por_tipo = {}
for tipo in conteo_tipos:
    pesos_tipo = [p["peso"] for p in validos if tipo in p["tipos"]]
    peso_promedio_por_tipo[tipo] = round(sum(pesos_tipo) / len(pesos_tipo), 2)

ordenados = sorted(validos, key=lambda p: p["tipos"][0])
tipo_principal = {}
for tipo, grupo in groupby(ordenados, key=lambda p: p["tipos"][0]):
    tipo_principal[tipo] = len(list(grupo))

estadisticas = {
    "total_en_lista": len(lista),
    "total_analizados": len(validos),
    "peso_promedio": round(sum(pesos) / len(pesos), 2),
    "peso_maximo": max(validos, key=lambda p: p["peso"])["nombre"],
    "peso_minimo": min(validos, key=lambda p: p["peso"])["nombre"],
    "altura_promedio": round(sum(alturas) / len(alturas), 2),
    "conteo_por_tipo": dict(conteo_tipos),
    "peso_promedio_por_tipo": peso_promedio_por_tipo,
    "conteo_por_tipo_principal": tipo_principal,
    "ejemplo_aplanado": dict(islice(aplanar(crudos[0]).items(), 10)),
}

with open("estadisticas.json", "w", encoding="utf-8") as archivo:
    json.dump(estadisticas, archivo, indent=2, ensure_ascii=False)
print("Listo: estadisticas.json")
