import os
import time
from tqdm import tqdm
import openai

# Configurar la API key de OpenAI
openai.api_key = 'tu_api_key'  # Reemplazar 'tu_api_key' con tu clave de API de OpenAI

# Función para obtener una respuesta sin "Unable to fetch the response, Please try again."
def obtener_respuesta(prompt):
    while True:
        try:
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                max_tokens=150
            )
            text = response.choices[0].text.strip()
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
        f"No hagas comentarios de nada ni indiques secciones! limitate a hacer lo que te digo sin comentar: lee linea a linea frase a frase e identifica y reconoce los roles de entrevistador y entrevistado en el siguiente texto de una porción de entrevista y formatea la salida como esa porción de entrevista con etiquetas antecediendo cada línea, palabra o frase con etiquetas de entrevistador y entrevistado, presentando el mismo el orden del desarrollo de la porción de la entrevista, con un salto de línea de separación entre cada una. Etiqueta cada palabra o línea o frase o párrafo según corresponda: {chunk}"
    )

    # Agregar la respuesta formateada al texto de salida
    texto_de_salida += respuesta_bot + "\n"

    # Actualizar la barra de progreso de chunks
    barra_progreso_chunks.update(1)

# Cerrar la barra de progreso de chunks
barra_progreso_chunks.close()

# Guardar el texto de salida en el archivo de respuestas
with open("entrevistas_completa_formateada.txt", "w", encoding="utf-8") as archivo_respuestas:
    archivo_respuestas.write(texto_de_salida)

print("Proceso completado. Conversación guardada en 'entrevistas_completa_formateada.txt'")
