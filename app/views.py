import os
import io
import time
import re
import sys
from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.
def home(request):
    return render(request, 'app/main.html')

def verdoc(request):
    doc = request.GET["Documento"]
    f = open('app/templates/files/Files/'+doc, 'r', encoding="utf8",errors='ignore')
    file_content = f.read()
    f.close()
    return HttpResponse(file_content, content_type="text/plain")
    ##return render(request, 'files/Files/'+doc)

def procesar(request):
    print("Procesando")
    palabraInput = request.GET["Palabra"]
    filesPath = "app/templates/files/Files"
    noHTMLPath = "app/templates/files/noHTML//"
    tokenized = "app/templates/files/tokenized//"

    # Itera para obtener los nombres de los archivos dentro de la carpeta Files
    for filename in os.listdir(filesPath):

        # Abre los archivos concatenando la varianble filesPath + el nombre del file en iteración
        oneFileTimeStart = time.perf_counter()
        with open(os.path.join(filesPath, filename), 'r', encoding='utf-8', errors='ignore') as f:

            # Crear nuevo archivo
            with io.open(noHTMLPath + filename, 'w', encoding="utf-8") as newFile:
                putIt = None
                # Leer linea por linea
                for line in f:
                    newLine = re.sub("\s\s+", " ", line)
                    for char in newLine:
                        if char == "<":
                            putIt = False
                        elif (char != '<') and (putIt == True):
                            if char.isalpha() or char.isspace() and char != "\t":
                                newFile.write(char)
                        elif char == ">":
                            putIt = True

                oneFileTimeEnd = time.perf_counter()
            newFile.close()
        f.close()

    stopList = []
    diccionario = []
    diccionarioGeneral = []
    lastPath = None
    listaPalabras = []

    # Ordener las palabras alfabeticamente y contar las repetidas

    for filename in os.listdir(noHTMLPath):
        diccionario = []
        with open(os.path.join(noHTMLPath, filename), 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                line = line.lower()
                words = line.split(" ")

                for word in words:
                    if len(word) > 1 and word == palabraInput:
                        word.lstrip()
                        match = any(
                            item.get('path', "NONE") == filename and item.get('palabra', "NONE PALABRA") == word for
                            item in diccionario)

                        if match:
                            matchPalabra = next(
                                l for l in diccionario if l['path'] == filename and l["palabra"] == word)
                            matchPalabra["repeticiones"] = matchPalabra["repeticiones"] + 1

                        else:
                            diccionario.append({"path": filename, "repeticiones": 1, "palabra": word})

            for index in range(len(diccionario)):
                if diccionario[index].get('palabra') == str(palabraInput):
                    listaPalabras.append(diccionario[index].get('path'))
                    break

        diccionarioGeneral.extend(diccionario)
        lastPath = filename

    diccionarioGeneral = sorted(diccionarioGeneral, key=lambda i: (i['repeticiones']), reverse=True)

    if (len(diccionarioGeneral) > 10):
        diccionarioGeneral = diccionarioGeneral[0:10]

        # Escribir el archivo de posting
        with io.open(tokenized + "retrieve.txt", 'w', encoding="utf-8") as newFile:
            newFile.write("Archivos con la(s) palabra(s): \n\n")

            newFile.write("\nTop 10 documentos: \n")

            for documento in range(len(diccionarioGeneral)):
                newFile.write(
                    str(index) + ".     " + diccionarioGeneral[documento].get('path') + " - " + diccionarioGeneral[
                        documento].get('palabra') + "\n")
                index += 1

    f = open('app/templates/files/tokenized/retrieve.txt','r')
    file_content = f.read()
    f.close()
    #return HttpResponse(file_content, content_type="text/plain")
    return render(request, "app/result.html", {"array": diccionarioGeneral, "palabra":palabraInput})