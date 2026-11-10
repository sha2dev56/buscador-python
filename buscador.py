import os
import re
import json

CARPETA_APUNTES = "apuntes"
ARCHIVO_INDICE = "indice.json"


def leer_lineas(ruta):
    """Devuelve las líneas del archivo, sin los saltos de línea finales."""
    with open(ruta, "r", encoding="utf-8") as archivo:
        return archivo.read().splitlines()


def buscar(palabra):
    """Busca una palabra recorriendo todos los archivos .txt de apuntes."""
    palabra = palabra.lower()
    for nombre in os.listdir(CARPETA_APUNTES):
        if nombre.endswith(".txt"):
            ruta = os.path.join(CARPETA_APUNTES, nombre)
            for numero, linea in enumerate(leer_lineas(ruta), start=1):
                palabras_linea = re.findall(r"\w+", linea.lower())
                if palabra in palabras_linea:
                    print(f"{nombre}, línea {numero}")


def crear_indice():
    """Crea un diccionario palabra -> apariciones y lo guarda en indice.json."""
    indice = {}
    for nombre in os.listdir(CARPETA_APUNTES):
        if nombre.endswith(".txt"):
            ruta = os.path.join(CARPETA_APUNTES, nombre)
            for numero, linea in enumerate(leer_lineas(ruta), start=1):
                palabras = re.findall(r"\w+", linea.lower())
                for palabra in palabras:
                    if palabra not in indice:
                        indice[palabra] = []
                    aparicion = [nombre, numero]
                    if aparicion not in indice[palabra]:
                        indice[palabra].append(aparicion)

    with open(ARCHIVO_INDICE, "w", encoding="utf-8") as archivo:
        json.dump(indice, archivo, ensure_ascii=False, indent=4)
    return indice


def cargar_indice():
    """Carga el índice guardado en indice.json."""
    with open(ARCHIVO_INDICE, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def buscar_con_indice(indice, palabra):
    """Busca una palabra en el índice y muestra dónde aparece."""
    apariciones = indice.get(palabra.lower(), [])
    if apariciones:
        for nombre, numero in apariciones:
            print(f"{nombre}, línea {numero}")
    else:
        print("No aparece")


def main():
    crear_indice() 
    indice = cargar_indice()
    while True:
        palabra = input("Palabra (o 'salir'): ").strip()
        if palabra.lower() == "salir":
            break
        buscar_con_indice(indice, palabra)


if __name__ == "__main__":
    main()
