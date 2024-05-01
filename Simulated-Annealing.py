import math
import random
from flask import Flask, render_template

app = Flask(__name__)

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def evalua_ruta(ruta, coord):
    total = 0
    for i in range(len(ruta)):
        ciudad1 = ruta[i]
        ciudad2 = ruta[(i + 1) % len(ruta)]
        total += distancia(coord[ciudad1], coord[ciudad2])
    return total

def simulated_annealing(ruta, coord):
    T = 20
    T_MIN = 0.1
    V_enfriamiento = len(ruta) * 10

    while T > T_MIN:
        dist_actual = evalua_ruta(ruta, coord)
        for _ in range(V_enfriamiento):
            i = random.randint(0, len(ruta)-1)
            j = random.randint(0, len(ruta)-1)
            ruta_tmp = ruta[:]
            ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
            dist = evalua_ruta(ruta_tmp, coord)
            delta = dist_actual - dist
            if delta > 0 or random.random() < math.exp(delta/T):
                ruta = ruta_tmp[:]
                dist_actual = dist
        T -= 0.005 * T
    
    return ruta

@app.route('/')
def index():
    coord = {
        'Jiloyork' :(19.916012, -99.580580),
        'Toluca':(19.289165, -99.655697),
        'Atlacomulco':(19.799520, -99.873844),
        'Guadalajara':(20.677754472859146, -103.34625354877137),
        'Monterrey':(25.69161110159454, -100.321838480256),
        'QuintanaRoo':(21.163111924844458, -86.80231502121464),
        'Michohacan':(19.701400113725654, -101.20829680213464),
        'Aguascalientes':(21.87641043660486, -102.26438663286967),
        'CDMX':(19.432713075976878, -99.13318344772986),
        'QRO':(20.59719437542255, -100.38667040246602)
    }

    # Crear una ruta inicial aleatoria
    ruta = list(coord.keys())
    random.shuffle(ruta)

    ruta_optima = simulated_annealing(ruta, coord)
    distancia_total = evalua_ruta(ruta_optima, coord)

    return render_template('index.html', ruta=ruta_optima, distancia_total=distancia_total)

if __name__ == "__main__":
    app.run(debug=True)
