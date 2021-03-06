from random import choice, random

# Nombre: generadorLPSolve
#   * Genera un texto para usarse en lp_solve dependiendo de los parametros introducidos
# Inputs:
#   * m: numero de estudiantes postulando a ayudantia
#   * n: numero de ayudantias disponibles
#   * ffact: (forzar factibilidad) determina la cantidad de horas de los estudiantes
#           0 si se quiere cantidad de horas aleatorias
#           1 si se quiere 15 horas por cada estudiante
# Returns:
#   * string: texto ASCII del modelo que se usara en lp_solve


def generadorLPSolve(m, n, ffact=0):
    # Listas de ofertas (si), demandas (dj) y preferencias (cij)
    si = []
    dj = []
    cij = []

    # Numero M "grande" que "castiga" a la funcion objetivo denotando una no preferencia
    M = 100000
    # Posibles preferencias
    p = [-M, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    # Cantidad de horas ofrecidas desde el nodo i como tupla (indice, horas)
    if ffact == 0:
        for i in range(0, m):
            si.append((i + 1, round(random() * 15, 1)))
    else:
        for i in range(0, m):
            si.append((i + 1, 15))

    # Posibles horas demandadas por cada ayudantia
    dc = [7, 8, 15]

    # Cantidad de horas demandadas por el nodo i como tupla (indice, horas)
    for i in range(0, n):
        dj.append((i + 1, choice(dc)))

    # Crear los arcos entre la oferta i y la demanda j, con su respectiva preferencia
    for i in range(0, m):
        for j in range(0, n):
            cij.append((choice(p), i + 1, j + 1))

    # -----------------------------------------------------------------------------------------------------------------
    # Factibilidad
    # Asegurarse de que la suma de ofertas >= suma de demandas
    fact = True

    SumaS = 0
    SumaD = 0
    for t in si:
        SumaS += t[1]

    for t in dj:
        SumaD += t[1]

    # crear fuente fantasma?
    if(SumaS < SumaD):
        fact = False
        print("Problema infactible: demanda menor a oferta")
    else:
        print("Problema factible: demanda mayor o igual a oferta")

    # Asegurarse de que al menos 1 estudiante tenga preferencia > 0 hacia alguna ayudantia
    # en caso contrario habra una ayudantia a la que ningun estudiante este dispuesto a postular
    for i, h in dj:
        n_pref = 0
        for c, i_si, j_dj in cij:
            if i == j_dj and c > 0:
                n_pref += 1
        if n_pref == 0:
            print("Problema infactible: Nadie quiere hacer la ayudantia " + str(i))
            fact = False
    # -----------------------------------------------------------------------------------------------------------------

    # Genera funcion objetivo con la suma de las variables de decision Xij multiplicado por su respectiva preferencia Cij
    fo = "max: "
    for c, i, j in cij:
        p = ""
        if c < 0:
            if i == 1 and j == 1:
                p = "-" + str(-c)
            else:
                p = " - " + str(-c)
        else:
            if i == 1 and j == 1:
                p = str(c)
            else:
                p = " + " + str(c)
        fo += p + " X" + str(i) + "_" + str(j)
    fo += ";\n"

    # Genera las restricciones de oferta
    const_si = ""
    for i, h in si:
        suma_xij = ""
        for j in range(1, n + 1):
            suma_xij += "X" + str(i) + "_" + str(j)
            if(j != n):
                suma_xij += " + "
        const_si += "estudiante" + \
            str(i) + ": " + suma_xij + " <= " + str(h) + ";\n"

    # Genera las restricciones de demanda
    const_dj = ""
    for i, h in dj:
        suma_xji = ""
        for j in range(1, m + 1):
            suma_xji += "X" + str(j) + "_" + str(i)
            if(j != m):
                suma_xji += " + "
        const_dj += "ayudantia" + \
            str(i) + ": " + suma_xji + " = " + str(h) + ";\n"

    #print(fo + const_si + const_dj)
    return (fo + const_si + const_dj, fact)

# Nombre: txtLPSolve
#   * Genera un archivo en la ruta especificada con el modelo LINDO escrito
# Inputs:
#   * filepath: ruta donde se escribira el archivo
#   * text: texto escrito en el archivo
# Returns:
#   * No retorna


def txtLPSolve(filepath, text):
    with open(filepath, 'w') as f:
        f.write(text)


# Definimos nuestros limites superiores y el directorio donde se guardaran los casos
M_SUP = 100
N_SUP = 100
directorio = r'C:\Users\claud\Desktop\2022-1\INF292 (opti)\proyecto1\modelos\\'

# Iteramos por cada archivo .lp mxn a crear
for m in range(1, M_SUP + 1):
    for n in range(1, N_SUP + 1):
        print(str(m) + "x" + str(n))
        texto, fact = generadorLPSolve(m, n, 0)
        strfact = "infact"
        if fact:
            strfact = "fact"
        nombre_archivo = strfact + str(m) + "x" + str(n) + ".lp"
        txtLPSolve(directorio + nombre_archivo, texto)
