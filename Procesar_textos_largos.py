#falta ajustar la orden de gpt4free para que sea mas especifica.

import os
import time
import codecs
from gpt4free import you
from tqdm import tqdm

# Función para obtener una respuesta sin "Unable to fetch the response, Please try again."
def obtener_respuesta(prompt):
    while True:
        try:
            response = you.Completion.create(prompt=prompt)
            text = response.text.strip()
            if text != "Unable to fetch the response, Please try again.":
                return text
        except Exception as e:
            print(f"Error al obtener la respuesta: {e}")
            print("Reintentando en 2 segundos...")
            time.sleep(2)  # Espera 2 segundos antes de intentar nuevamente

# Pedir al usuario la ruta del archivo .txt
archivo_txt = input("Por favor, ingresa la ruta del archivo .txt: ")

try:
    with open(archivo_txt, "r", encoding="utf-8") as archivo_entrada:
        contenido = archivo_entrada.read()
except FileNotFoundError:
    print("El archivo especificado no se encontró.")
    exit()

# Dividir el contenido en chunks de 1000 palabras
chunk_size = 1000
chunks = [contenido[i:i+chunk_size] for i in range(0, len(contenido), chunk_size)]

# Crear una variable para almacenar el texto de salida
texto_de_salida = ""

# Inicializar la barra de progreso
barra_progreso_chunks = tqdm(total=len(chunks), desc="Procesando Chunks")

# Procesar cada chunk y escribir en el archivo de respuestas
for chunk in chunks:
    # Obtener respuesta del modelo para el chunk actual
    respuesta_bot = obtener_respuesta(
        f"analiza linea a linea, frase a frase y reconoce automáticamente los roles de entrevistador y entrevistado en el siguiente texto de una entrevista y formatea el output como una entrevista sin alterar el orden del desarrollo de la misma. Etiqueta cada línea o frase o párrafo según corresponda: {chunk}"
    )

    # Formatear la respuesta utilizando codecs para mostrar caracteres Unicode
    respuesta_formateada = codecs.decode(respuesta_bot, 'unicode_escape')

    # Agregar la respuesta formateada al texto de salida
    texto_de_salida += respuesta_formateada + "\n"

    # Actualizar la barra de progreso de chunks
    barra_progreso_chunks.update(1)

# Cerrar la barra de progreso de chunks
barra_progreso_chunks.close()

# Guardar el texto de salida en el archivo de respuestas
with open("entrevistas_completa_formateada.txt", "w", encoding="utf-8") as archivo_respuestas:
    archivo_respuestas.write(texto_de_salida)

print("Proceso completado. Conversación guardada en 'entrevistas_completa_formateada.txt'")
